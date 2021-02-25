readpaf
=======
Scripts for reading minimap2 PAF files

Installation
===

readpaf is contained in a single module so can be installed via PyPI:

```bash
pip install readpaf
```

inlcuding pandas:

```bash
pip install readpaf[pandas]
```

Or [readpaf.py](readpaf.py) can be directly downloaded like so

using cURL

```bash
curl -O https://raw.githubusercontent.com/alexomics/read-paf/main/readpaf.py
```

or wget

```bash
wget https://raw.githubusercontent.com/alexomics/read-paf/main/readpaf.py

```

Usage
===

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
their correct types and stored in a dictionary.

If used to generate a pandas DataFrame, then each row represents a line in the PAF file and the SAM-like tags 
are expanded into individual series.
