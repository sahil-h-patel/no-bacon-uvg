# Setup:

```console
python3 -m venv venv
pip install -r requirements.txt
```

# Usage:

`requirements.txt` will install the `nbuvg` pacakge which will have all the commands needed for the project, to use it follow the structure below:

```console
nbuvg [OPTION] COMMAND [ARGUMENTS]
```

use `--help` to open the help menu for package or commands for further information.

## Connecting to the Database:

Make sure you have the `.env` file setup accordingly:

```
SSH_USER=********
SSH_PASSWORD=********
SSH_HOST=********
DB_USER=********
DB_PASSWORD=********
DB_HOST=********
DB_NAME=********
DB_PORT=********
```

# Project Structure & Troubleshooting

```
root
├─ .gitignore
├─ README.md
├─ cli.py
├─ commands
│  ├─ __init__.py
│  └─ ...
├─ requirements.txt
└─ setup.py
```

This should be the general project structure, make sure `cli.py` and `setup.py` is in root dir. `setup.py` should not be edited under any circumstance during production, otherwise please use:

```console
pip install -e .
```

This should set the nbuvg package in development mode which will hot-reload any new commands or packages. *Use after every pull*


