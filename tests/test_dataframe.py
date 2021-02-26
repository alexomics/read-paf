import os
import pytest
import pandas as pd
from readpaf import parse_paf

STATIC_FILES = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static_files")
PAF_FILE = os.path.join(STATIC_FILES, "test.paf")
MISSING_LINE = os.path.join(STATIC_FILES, "test_blank_line.paf")


def test_read_to_dataframe():
    with open(PAF_FILE, "r") as fh:
        df = parse_paf(fh, dataframe=True)
    assert isinstance(df, pd.DataFrame), "Not a DataFrame"
    assert df.shape == (10, 18), "Not the right shape {}".format(df.shape)


def test_read_missing_line():
    with open(MISSING_LINE, "r") as fh:
        df = parse_paf(fh, dataframe=True)
    assert df.shape == (9, 18), "Not the right shape"


def test_fields():
    cols = [
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
    with open(PAF_FILE, "r") as fh:
        df = parse_paf(fh, dataframe=True)
    assert set(cols).issubset(set(df.columns)), "Fields not set correctly"
