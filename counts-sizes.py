# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "numpy",
# ]
# ///
import json
import sys
import csv

import numpy as np

"""
Turns

```
{
    "d": {
        "f1": 1,
        "f2": 2,
        "dd": {
            "f3": 4
        }
    }
}
```

into

```
path,count_total,size_total,count_1,size_1,count_2,size_2,count_3,size_3,count_4,size_4
d/f1,1,1,1,1
d/f2,1,2,1,2
d/dd/f3,1,4,1,4
d/dd/,2,4,1,0,2,4
d/,5,7,1,0,4,3,5,7
```

which as a table is:

| path    | count_total | size_total | count_1 | size_1 | count_2 | size_2 | count_3 | size_3 | count_4 | size_4 |
| ------- | ----------- | ---------- | ------- | ------ | ------- | ------ | ------- | ------ | ------- | ------ |
| d/f1    | 1           | 1          | 1       | 1      |         |        |         |        |         |        |
| d/f2    | 1           | 2          | 1       | 2      |         |        |         |        |         |        |
| d/dd/f3 | 1           | 4          | 1       | 4      |         |        |         |        |         |        |
| d/dd/   | 2           | 4          | 1       | 0      | 2       | 4      |         |        |         |        |
| d/      | 5           | 7          | 1       | 0      | 4       | 3      | 5       | 7      |         |        |
|         |             |            |         |        |         |        |         |        |         |        |

-- the columns are the counts (number of children) and sizes (bytes) at depths up to infinity, 1, 2, 3 etc.
"""


def sums(path, tree, out):
    assert isinstance(tree, dict) or isinstance(tree, int)
    if isinstance(tree, int):
        sizes = np.array([tree])
        counts = np.array([1])
    else:
        # Otherwise, `path` is a directory.
        sizes = np.array([0])
        counts = np.array([1])
        for name, value in tree.items():
            sub_sizes, sub_counts = sums(f"{path}/{name}", value, out)
            to_pad = len(sub_sizes) + 1 - len(sizes)
            if to_pad > 0:
                sizes = np.concatenate((sizes, [0] * to_pad))
                counts = np.concatenate((counts, [0] * to_pad))
            for i, v in enumerate(sub_sizes):
                sizes[i + 1] += v
            for i, v in enumerate(sub_counts):
                counts[i + 1] += v
        path += "/"
    out.append((path, sizes, counts))
    return (sizes, counts)


def main():
    tree = json.load(sys.stdin)
    assert isinstance(tree, dict)
    assert len(tree.keys()) == 1
    root = list(tree.keys())[0]
    subtree = tree[root]
    out = []
    sums(root, subtree, out)
    length = 1 + max(len(sizes) for (_path, sizes, _counts) in out)
    writer = csv.writer(sys.stdout)
    headers = ["path", "count_total", "size_total"] + [
        item for i in range(1, length + 1) for item in (f"count_{i}", f"size_{i}")
    ]
    writer.writerow(headers)
    for path, sizes, counts in out:
        sizes = np.concatenate(([sum(sizes)], np.cumsum(sizes))).tolist()
        counts = np.concatenate(([sum(counts)], np.cumsum(counts))).tolist()
        row = [path] + [x for cs in zip(counts, sizes) for x in cs]
        writer.writerow(row)


if __name__ == "__main__":
    main()
