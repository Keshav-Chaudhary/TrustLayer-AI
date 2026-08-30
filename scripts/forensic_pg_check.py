import psycopg2
from psycopg2 import sql

conn_params = [
    {"dbname": "postgres", "user": "postgres", "password": "", "host": "localhost", "port": 5432},
    {"dbname": "postgres", "user": "postgres", "password": "postgres", "host": "localhost", "port": 5432},
    {"dbname": "factory", "user": "postgres", "password": "postgres", "host": "localhost", "port": 5432},
]

connected = False
for params in conn_params:
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print(f"=== CONNECTED TO POSTGRESQL ({params['dbname']}) ===")
        connected = True
        
        # Check databases
        cur.execute("SELECT datname FROM pg_database;")
        dbs = [r[0] for r in cur.fetchall()]
        print("Available Databases:", dbs)
        
        # Check extensions
        cur.execute("SELECT extname FROM pg_extension;")
        exts = [r[0] for r in cur.fetchall()]
        print("Installed Extensions:", exts)
        
        # Check available vector extension
        cur.execute("SELECT name, default_version, installed_version FROM pg_available_extensions WHERE name = 'vector';")
        vec_ext = cur.fetchall()
        print("pgvector Availability:", vec_ext)
        
        conn.close()
        break
    except Exception as ex:
        print(f"Connection attempt failed ({params['dbname']}):", str(ex))

if not connected:
    print("Could not connect to local PostgreSQL with default credentials.")
