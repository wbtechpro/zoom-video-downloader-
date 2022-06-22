# zoom video downloader

Zoom video download script

### Install dependencies

```
pip install -r requirements.txt
```

### Command

```
 python downland.py date_from=(from what date to download records) date_from=(by what date to download records) directory=(optional, directory to save)
```
### Command example
```
python downland.py date_from=2022-05-01 date_to=2022-05-09 directory=/home/example/
```

###  Command example without directory
```
python downland.py date_from=2022-05-01 date_to=2022-05-09
```
If the directory is not specified, saving will be made in the current directory to the created videos folder.

### After running the command, enter the JWT token