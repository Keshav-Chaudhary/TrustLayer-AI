import psycopg2

conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost", port=5432)
cur = conn.cursor()

cur.execute("SELECT version();")
ver = cur.fetchone()[0]

cur.execute("SELECT current_database(), current_user;")
db, user = cur.fetchone()

cur.execute("SELECT datname FROM pg_database ORDER BY datname;")
dbs = [r[0] for r in cur.fetchall()]

cur.execute("SELECT extname, extversion FROM pg_extension ORDER BY extname;")
installed_exts = cur.fetchall()

cur.execute("SELECT name, default_version, installed_version, comment FROM pg_available_extensions WHERE name = 'vector';")
available_vec = cur.fetchall()

print("=== PHASE 1 POSTGRESQL INSPECTION ===")
print("Version:", ver)
print("Database / User:", db, "/", user)
print("Databases:", dbs)
print("Installed Extensions:", installed_exts)
print("pgvector Available:", available_vec)

conn.close()
