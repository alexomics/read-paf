read-paf
========
Scripts for reading minimap2 PAF files

Installation
===

Either copy and paste the contents of [readpaf.py](readpaf.py) or cURL the file like so:

```bash
curl -O https://raw.githubusercontent.com/alexomics/read-paf/master/readpaf.py
```

If you need to open the PAF file as a DataFrame then [pandas](https://pandas.pydata.org/)
will need to be installed:

```python
pip install pandas
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