import os
import sys
import math
import pandas as pd
import pytest
from readpaf import parse_paf

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    from importlib import reload
except ImportError:
    pass

STATIC_FILES = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static_files")
PAF_FILE = os.path.join(STATIC_FILES, "test.paf")
MISSING_LINE = os.path.join(STATIC_FILES, "test_blank_line.paf")
UNMAPPED_REC = os.path.join(STATIC_FILES, "test_unmapped.paf")

DEFAULT_COLS = [
    "query_name",
    "query_length",
    "query_start",
    "query_end",
    "strand",
    "target_name",
    "target_length",
    "target_start",
    "target_end",
    "residue_matches",
    "alignment_block_length",
    "mapping_quality",
]


def test_read_to_dataframe():
    with open(PAF_FILE, "r") as fh:
        df = parse_paf(fh, dataframe=True)
    assert isinstance(df, pd.DataFrame), "Not a DataFrame"
    assert df.shape == (10, 18), "Not the right shape {}".format(df.shape)


def test_read_missing_line_dataframe():
    with open(MISSING_LINE, "r") as fh:
        df = parse_paf(fh, dataframe=True)
    assert df.shape == (9, 18), "Not the right shape"


def test_read_unmapped_dataframe():
    with open(UNMAPPED_REC, "r") as fh:
        df = parse_paf(fh, dataframe=True, na_rep=float("nan"))
    null = df[DEFAULT_COLS].isnull().any(axis=1).sum()
    assert null == 1, "Expected only one row with NaNs"


def test_fields_dataframe():
    with open(PAF_FILE, "r") as fh:
        df = parse_paf(fh, dataframe=True)
    assert set(DEFAULT_COLS).issubset(set(df.columns)), "Fields not set correctly"


def test_tag_suffix_dataframe():
    _rec = "a7208cb4-133c-4ab9-96fe-db8630f4d9bb\t373\t15\t368\t+\tEf_genome\t2845392\t586028\t586405\t103\t377\t60\ttp:A:P\tcs:Z::6-ata:10+gtc:4*at:3\n"
    PAF_IO = StringIO(_rec)
    cols = [
        "query_name",
        "query_length",
        "query_start",
        "query_end",
        "strand",
        "tp",
        "target_length",
        "target_start",
        "target_end",
        "residue_matches",
        "alignment_block_length",
        "mapping_quality",
    ]
    df = parse_paf(PAF_IO, fields=cols + ["tags"], dataframe=True)
    assert set(df.columns) == set(cols + ["cs", "tp_tag"]), "Tag field not set correctly"


def test_read_uncompressed():
    c = 0
    with open(PAF_FILE, "r") as fh:
        for record in parse_paf(fh):
            c += 1
    assert c == 10, "Incorrect number of records"


def test_read_missing_line():
    c = 0
    with open(MISSING_LINE, "r") as fh:
        for record in parse_paf(fh):
            c += 1
    assert c == 9, "Incorrect number of records"


def test_custom_fields():
    f = ["qn", "ql", "qs", "qe", "s", "tn", "tl", "ts", "te", "rm", "abl", "mq", "tags"]
    with open(PAF_FILE, "r") as fh:
        for record in parse_paf(fh, fields=f):
            assert set(record._fields) == set(f), "Fields not set correctly"


def test_wrong_number_of_fields():
    f = ["qn", "ql", "qs", "qe", "s", "tn", "tl", "ts", "te", "rm", "abl", "mq"]
    with pytest.raises(ValueError):
        with open(PAF_FILE, "r") as fh:
            for record in parse_paf(fh, fields=f):
                pass


def test_blast_identity():
    with open(PAF_FILE, "r") as fh:
        for record in parse_paf(fh):
            assert isinstance(record.blast_identity(), float), "Expected a float"


def test_get_paf_line():
    _rec = "a7208cb4-133c-4ab9-96fe-db8630f4d9bb\t373\t15\t368\t+\tEf_genome\t2845392\t586028\t586405\t103\t377\t60\ttp:A:P\n"
    PAF_IO = StringIO(_rec)
    for rec in parse_paf(PAF_IO):
        assert str(rec) == _rec.strip(), "record didn't match"


def test_read_unmapped():
    c = 0
    with open(UNMAPPED_REC, "r") as fh:
        for record in parse_paf(fh):
            c += 1
    assert c == 10, "Incorrect number of records"


def test_request_dataframe_without_pandas(monkeypatch):
    monkeypatch.setitem(sys.modules, "pandas", None)
    reload(sys.modules["readpaf"])
    with open(PAF_FILE, "r") as fh:
        with pytest.raises(ImportError):
            _ = parse_paf(fh, dataframe=True)


def test_nan_rep():
    _rec = "2a708733-5e95-49e3-8806-e181e9380cd9\t3715\t*\t*\t*\t*\t*\t*\t*\t*\t*\t61\n"
    PAF_IO = StringIO(_rec)
    for rec in parse_paf(PAF_IO, na_rep=float("nan")):
        assert math.isnan(rec.query_start)


def test_multiple_nan_values():
    _rec = (
        "2a708733-5e95-49e3-8806-e181e9380cd9\t3715\t*\tnan\t*\t*\t*\t*\t*\t*\t*\t61\n"
    )
    PAF_IO = StringIO(_rec)
    for rec in parse_paf(PAF_IO, na_values=["nan"]):
        assert rec.query_start == 0 and rec.query_end == 0


def test_wrong_nan_rep():
    with pytest.raises(ValueError):
        with open(UNMAPPED_REC, "r") as fh:
            _ = parse_paf(fh, na_rep="nan")


def test_write_unmapped_line():
    _rec = "2a708733-5e95-49e3-8806-e181e9380cd9\t3715\t*\t*\t*\t*\t*\t*\t*\t*\t*\t61\txx:A:X"
    _out = "2a708733-5e95-49e3-8806-e181e9380cd9\t3715\t0\t0\t*\t*\t0\t0\t0\t0\t0\t61\txx:A:X"
    PAF_IO = StringIO(_rec)
    for rec in parse_paf(PAF_IO):
        assert str(rec) == _out.strip(), "record didn't match"
