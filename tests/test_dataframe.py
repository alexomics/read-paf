import os
import pandas as pd
from readpaf import parse_paf

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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


def test_read_missing_line():
    with open(MISSING_LINE, "r") as fh:
        df = parse_paf(fh, dataframe=True)
    assert df.shape == (9, 18), "Not the right shape"


def test_read_unmapped():
    with open(UNMAPPED_REC, "r") as fh:
        df = parse_paf(fh, dataframe=True)
    null = df[DEFAULT_COLS].isnull().any(axis=1).sum()
    assert null == 1, "Expected only one row with NaNs"


def test_fields():
    with open(PAF_FILE, "r") as fh:
        df = parse_paf(fh, dataframe=True)
    assert set(DEFAULT_COLS).issubset(set(df.columns)), "Fields not set correctly"


def test_tag_suffix():
    _rec = "a7208cb4-133c-4ab9-96fe-db8630f4d9bb\t373\t15\t368\t+\tEf_genome\t2845392\t586028\t586405\t103\t377\t60\ttp:A:P\n"
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
    assert set(df.columns) == set(cols + ["tp_tag"]), "Tag field not set correctly"
