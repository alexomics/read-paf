readpaf
=======
[![Build](https://github.com/alexomics/read-paf/actions/workflows/main.yml/badge.svg)](https://github.com/alexomics/read-paf/actions/workflows/main.yml)
[![PyPI](https://img.shields.io/pypi/v/readpaf)](https://pypi.org/p/readpaf)

readpaf is a fast parser for [minimap2](https://github.com/lh3/minimap2) PAF (**P**airwise m**A**pping **F**ormat) files. It is 
pure python with no dependencies (unless you want a DataFrame).


Installation
===
```bash
pip install readpaf
```

<details>
  <summary>Other install methods</summary>
    
   ### Install with pandas:
   This is only needed if you want to manipulate the PAF file as a `pandas.DataFrame`

   ```bash
   pip install readpaf[pandas]
   ```

   ### Direct download:
   using cURL

   ```bash
   curl -O https://raw.githubusercontent.com/alexomics/read-paf/main/readpaf.py
   ```

   or wget

   ```bash
   wget https://raw.githubusercontent.com/alexomics/read-paf/main/readpaf.py
   ```
</details>

Usage
===

readpaf only has one user function, `parse_paf` that accepts of file-like object; this 
is any object in python that has a file-oriented API (`sys.stdin`, `stdout` from subprocess, 
`io.StringIO`, open files from `gzip` or `open`).  

The following script demonstrates how minimap2 output can be piped into read-paf 

```python
from readpaf import parse_paf
from sys import stdin

for record in parse_paf(stdin):
    print(record.query_name, record.target_name)
```

read-paf can also generate a pandas DataFrame:

```python
from readpaf import parse_paf

with open("test.paf", "r") as handle:
    df = parse_paf(handle, dataframe=True)

```

Functions
===

read-paf has a single user function

parse_paf
---

```python
parse_paf(file_like=file_handle, fields=list, dataframe=bool)
```
Parameters:

 - **file_like:** A file like object, such as `sys.stdin`, a file handle from open or io.StringIO objects
 - **fields:** A list of 13 field names to use for the PAF file, default:
    ```python
    "query_name", "query_length", "query_start", "query_end", "strand",
    "target_name", "target_length", "target_start", "target_end",
    "residue_matches", "alignment_block_length", "mapping_quality", "tags"
    ```
    These are based on the [PAF specification](https://github.com/lh3/miniasm/blob/master/PAF.md).
 - **dataframe:** bool, if True, return a pandas.DataFrame with the tags expanded into separate Series
 
If used as an iterator, then each object returned is a named tuple representing a single line in the PAF file. 
Each named tuple has field names as specified by the `fields` parameter. The SAM-like tags are converted into 
their correct types and stored in a dictionary. When `print` or `str` are called on `PAF` record (named tuple) 
a formated PAF string is returned, which is useful for writing records to a file. The `PAF` record also has a 
method `blast_identity` which calculates the [blast identity](https://lh3.github.io/2018/11/25/on-the-definition-of-sequence-identity) for
that record.

If used to generate a pandas DataFrame, then each row represents a line in the PAF file and the SAM-like tags 
are expanded into individual series.
