from __future__ import division
from collections import namedtuple


__all__ = ["parse_paf"]

__version__ = "0.0.6"

try:
    import pandas as pd
except Exception as E:
    pandas = False
    e = E
else:
    pandas = True


class _PAF:
    """Base PAF methods, can't guarantee field names here so use indices"""

    def __str__(self):
        """Formats a record as a PAF line for writing to a file"""
        return "{}\t{}".format("\t".join(map(str, self[:-1])), self._fmt_tags())

    def _fmt_tags(self):
        """Format tag dict as SAM style"""
        return "\t".join(
            "{}:{}:{}".format(k, REV_TYPES.get(k), v) for k, v in self[-1].items()
        )

    def blast_identity(self):
        """BLAST identity, see:
        https://lh3.github.io/2018/11/25/on-the-definition-of-sequence-identity
        """
        return self[9] / self[10]


SAM_TYPES = {"i": int, "A": str, "f": float, "Z": str}
REV_TYPES = {
    "tp": "A",
    "cm": "i",
    "s1": "i",
    "s2": "i",
    "NM": "i",
    "MD": "Z",
    "AS": "i",
    "ms": "i",
    "nn": "i",
    "ts": "A",
    "cg": "Z",
    "cs": "Z",
    "dv": "f",
    "de": "f",
    "rl": "i",
}


def _expand_dict_in_series(df, field):
    """Convert a Series of dict to Series and add to the original DataFrame

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame with a Series of dict
    field : str
        The Series of dicts to expand

    Returns
    -------
    pd.DataFrame
        The orignal DataFrame with extra Series from the dicts
    """
    return df.join(pd.DataFrame(df.pop(field).tolist()), rsuffix="_tag")


def _parse_tags(tags):
    """Convert a list of SAM style tags, from a PAF file, to a dict

    https://samtools.github.io/hts-specs/SAMv1.pdf section 1.5

    Parameters
    ----------
    tags : list
        A list of SAM style tags

    Returns
    -------
    dict
        Returns dict of SAM style tags
    """
    _def = lambda x: x  # noqa: E731
    return {
        tag: SAM_TYPES.get(type_, _def)(val)
        for tag, type_, val in (x.split(":") for x in tags)
    }


def _paf_generator(file_like, fields=None):
    """Generator that returns namedtuples from a PAF file

    Parameters
    ----------
    file_like : file-like object
        File-like object
    fields : list
        List of field names to use for records, must have 13 entries.

    Yields
    ------
    namedtuple
        Correctly formatted PAF record and a dict of extra tags

    Raises
    ------
    ValueError
    """
    if len(fields) != 13:
        raise ValueError("{} fields provided, expected 13".format(len(fields)))
    _PAF_nt = namedtuple("PAF", fields)
    PAF = type("PAF", (_PAF, _PAF_nt), dict())
    for record in file_like:
        record = record.strip()
        if not record:
            continue
        record = record.split("\t")
        yield PAF(
            str(record[0]),
            int(record[1]),
            int(record[2]),
            int(record[3]),
            str(record[4]),
            str(record[5]),
            int(record[6]),
            int(record[7]),
            int(record[8]),
            int(record[9]),
            int(record[10]),
            int(record[11]),
            _parse_tags(record[12:]),
        )


def parse_paf(file_like, fields=None, dataframe=False):
    """Read a minimap2 PAF file as either an iterator or a pandas.DataFrame

    Parameters
    ----------
    file_like : file-like object
        Object with a read() method, such as a sys.stdin, file handler or io.StringIO.
    fields : list
        List of field names to use for records, must have 13 entries. These should
        be in the order of the fields in the PAF file and the last field will be
        used for tags.  Default:
        ["query_name", "query_length", "query_start", "query_end", "strand",
        "target_name", "target_length", "target_start", "target_end",
        "residue_matches", "alignment_block_length", "mapping_quality", "tags"]
    dataframe : bool
        Default is False. When True a pandas.DataFrame is returned with Series
        named as the `fields` parameter. SAM tags are expanded into Series as
        well and given their specified types, if any of the field names overlap
        with tags the tag column will be given the suffix `_tag`.

    Returns
    -------
    iterator or pandas.DataFrame when dataframe is True
    """
    if fields is None:
        fields = [
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
            "tags",
        ]
    if dataframe and pandas:
        return _expand_dict_in_series(
            pd.DataFrame(_paf_generator(file_like, fields=fields)), fields[-1]
        )
    elif dataframe and not pandas:
        raise ImportError(e)
    else:
        return _paf_generator(file_like, fields=fields)
