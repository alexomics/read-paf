from collections import namedtuple
try:
    import pandas as pd
except Exception as E:
    pandas = False
    e = E
else:
    pandas = True


SAM_TYPES = {"i": int, "A": str, "f": float, "Z": str}


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
    return df.join(pd.DataFrame(df.pop(field).tolist()))


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
    return {
        tag: _conv_type(val, SAM_TYPES.get(type_))
        for tag, type_, val in (x.split(":") for x in tags)
    }


def _conv_type(s, func):
    """Generic converter, to change strings to other types

    Parameters
    ----------
    s : str
        A string that represents another type
    func : function
        Function to apply to s, should take a single parameter

    Returns
    -------
    The type of func, otherwise str
    """
    if func is not None:
        try:
            return func(s)
        except ValueError:
            return s
    return s


def _format_records(records):
    """Helper function to make fields the right type
    """
    return (_conv_type(x, int) for x in records)


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
    PAF = namedtuple("PAF", fields)
    for record in file_like:
        record = record.strip()
        if not record:
            continue
        record = record.split("\t")
        yield PAF(*_format_records(record[:12]), _parse_tags(record[12:]))


def parse_paf(file_like, fields=None, dataframe=False):
    """Read a minimap2 PAF file as either an iterator or a pandas.DataFrame

    Parameters
    ----------
    file_like : file-like object
        Object with a read() method, such as a sys.stdin, file handler or io.StringIO.
    fields : list
        List of field names to use for records, must have 13 entries. Default:
        ["query_name", "query_length", "query_start", "query_end", "strand",
        "target_name", "target_length", "target_start", "target_end",
        "residue_matches", "alignment_block_length", "mapping_quality", "tags"]
    dataframe : bool
        Default is False. When True a pandas.DataFrame is returned with Series
        named as the `fields` parameter. SAM tags are expanded into Series as
        well and given their specified types.

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
