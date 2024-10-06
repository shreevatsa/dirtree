# How I use it for cleanup (Google Drive cruft synced into `FromGoogleDrive` on `athenas`)
ssh athenas "cd FromGoogleDrive; python3 ../dirtree.py > ../dirtree.json" 
scp athenas:/home/dirtree.json . 
uv run counts-sizes.py < dirtree.json > dirtree.csv 
open -a /Applications/DB\ Browser\ for\ SQLite-v3.13.1-rc2.app dirtree.csv
