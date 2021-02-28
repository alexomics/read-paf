"""test_readpaf.py

These are the main tests for the readpaf module, these are executed with 
the expectation that pandas is not available. 
"""
import os
import io
import pytest
from readpaf import parse_paf

try:
    import pandas as pd
except ImportError:
    PANDAS_AVAILABLE = False
else:
    PANDAS_AVAILABLE = True

STATIC_FILES = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static_files")
PAF_FILE = os.path.join(STATIC_FILES, "test.paf")
MISSING_LINE = os.path.join(STATIC_FILES, "test_blank_line.paf")


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
    PAF_IO = io.StringIO(_rec)
    for rec in parse_paf(PAF_IO):
        assert str(rec) == _rec.strip(), "record didn't match"


@pytest.mark.skipif(PANDAS_AVAILABLE, reason="pandas can't be installed for this test")
def test_request_dataframe():
    with pytest.raises(ImportError):
        with open(PAF_FILE, "r") as fh:
            _ = parse_paf(fh, dataframe=True)
