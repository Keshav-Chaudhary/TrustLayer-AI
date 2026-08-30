import shutil
import psycopg2

conn = psycopg2.connect(dbname="postgres", user="postgres", host="127.0.0.1", port=5432)
conn.autocommit = True
cur = conn.cursor()

# Set password for postgres user
cur.execute("ALTER USER postgres WITH PASSWORD 'postgres';")
print("Successfully set password for user 'postgres' to 'postgres'!")

cur.execute("SELECT version();")
print("PostgreSQL Version:", cur.fetchone()[0])

cur.execute("SELECT datname FROM pg_database;")
dbs = [r[0] for r in cur.fetchall()]
print("Available Databases:", dbs)

conn.close()

# Restore pg_hba.conf from backup
hba_file = r"C:\Program Files\PostgreSQL\17\data\pg_hba.conf"
bak_file = r"C:\Program Files\PostgreSQL\17\data\pg_hba.conf.bak"
if shutil.os.path.exists(bak_file):
    shutil.copyfile(bak_file, hba_file)
    print("Restored original pg_hba.conf file.")
