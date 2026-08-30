import psycopg2

passwords = ["postgres", "admin", "root", "123456", "1234", "password", "skesh", "trustlayer", ""]

found_password = None
for p in passwords:
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=p,
            host="localhost",
            port=5432
        )
        print(f"SUCCESS: Connected to PostgreSQL server using password: '{p}'")
        found_password = p
        
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print("Version:", cur.fetchone()[0])
        
        cur.execute("SELECT datname FROM pg_database;")
        dbs = [r[0] for r in cur.fetchall()]
        print("Databases:", dbs)
        
        cur.execute("SELECT name, default_version, installed_version FROM pg_available_extensions WHERE name = 'vector';")
        vec = cur.fetchall()
        print("pgvector available extension:", vec)
        
        conn.close()
        break
    except Exception as ex:
        pass

if not found_password:
    print("Could not connect with standard candidate passwords.")
