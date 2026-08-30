import os
import psycopg2

appdata = os.getenv("APPDATA")
pgpass_path = os.path.join(appdata, "postgresql", "pgpass.conf") if appdata else None

print("Checking pgpass.conf path:", pgpass_path)

if pgpass_path and os.path.exists(pgpass_path):
    print("Found pgpass.conf file!")
    with open(pgpass_path, "r") as f:
        content = f.read()
    print("Content:", content)
else:
    print("pgpass.conf not found at APPDATA.")

home_pgpass = os.path.expanduser("~/.pgpass")
if os.path.exists(home_pgpass):
    print("Found ~/.pgpass!")
    with open(home_pgpass, "r") as f:
        print(f.read())
