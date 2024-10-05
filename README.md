# dirtree
Trivial script to show biggest files and directories

```sh
python3 dirtree.py > dirtree.json
```

followed by

```sh
uv run counts-sizes.py < dirtree.json > dirtree.csv
```
