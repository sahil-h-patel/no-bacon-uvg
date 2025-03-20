# Setup:

```console
python3 -m venv venv
pip install -r requirements.txt
```

## Adding Commands

1. Create your command file `commands/` (`commands/mycommand.py`)

2. Create your command function(s). Here's an example:

``` python
import psycopg
from typing import Any

def mycommand(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    print(f"args: {args}")
    print(f"ctx: {ctx}")
    print(f"conn: {conn}")
```

3. Then export the function(s) in `commands/__init__.py`

``` python
from .mycommand import mycommand
```

4. Finally, add the function to the commands dictionary at the top of `cli.py`

``` python
CMDS: dict[str, Callable[[psycopg.Connection, list[str]], None]] = {
    # ...
    "mycommand": mycommand
    # ...
}
```

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
