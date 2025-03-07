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

This should set the nbuvg package in development mode which will hot-reload any new commands or packages.


