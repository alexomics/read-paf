import os
import pytest
from readpaf import parse_paf

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
