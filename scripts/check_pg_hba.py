import os

paths = [
    r"C:\Program Files\PostgreSQL\17\data\pg_hba.conf",
    r"C:\ProgramData\PostgreSQL\17\data\pg_hba.conf"
]

for p in paths:
    if os.path.exists(p):
        print(f"Found pg_hba.conf at {p}")
        try:
            with open(p, "r") as f:
                print(f.read()[:500])
        except Exception as ex:
            print("Could not read:", str(ex))
