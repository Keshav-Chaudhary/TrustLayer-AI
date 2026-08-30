import os
import getpass
import psycopg2

print("Current System User:", getpass.getuser())
for k, v in os.environ.items():
    if "PG" in k or "POSTGRES" in k or "DB" in k:
        print(f"Env: {k} = {v}")

test_users = [getpass.getuser(), "postgres", "admin"]
test_dbs = ["postgres", "template1", "factory"]
test_ports = [5432, 5433]

success = False
for port in test_dbs:
    for u in test_users:
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=u,
                host="localhost",
                port=5432
            )
            print(f"SUCCESS: Connected without password as user '{u}'!")
            success = True
            conn.close()
            break
        except Exception as ex:
            pass

if not success:
    print("Direct connection without password did not succeed.")
