import os
import json
import stat


def build_tree(path):
    """Returns a tree structure of the directory, with file sizes or 0 for symlinks/sockets.

    Like a JSON version of `ls -R`: Turns a directory structure like

    ```
    foo/
        file1.txt (1024 bytes)
        bar/
            file2.txt (2048 bytes)
            file3.txt (4096 bytes)
    ```

    into:

    ```
    {
        "foo": {
            "file1.txt": 1024,
            "bar": {
                "file2.txt": 2048,
                "file3.txt": 4096
            }
        }
    }
    """
    # 0 for symlinks and sockets
    if os.path.islink(path) or stat.S_ISSOCK(os.stat(path).st_mode):
        return 0
    if os.path.isfile(path):
        return os.path.getsize(path)
    if os.path.isdir(path):
        return {
            child: build_tree(os.path.join(path, child)) for child in os.listdir(path)
        }
    assert False, path


def main():
    root = "."
    tree = {os.path.basename(root): build_tree(root)}
    print(json.dumps(tree, indent=4))


if __name__ == "__main__":
    main()
