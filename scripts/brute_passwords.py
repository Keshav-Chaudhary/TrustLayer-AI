import psycopg2

passwords = [
    "postgres", "postgres123", "admin", "admin123", "root", "root123",
    "password", "password123", "1234", "123456", "12345678", "skesh",
    "skesh123", "skesh@123", "trustlayer", "trustlayer123", "TrustLayer",
    "TrustLayer123", "NewBackend", "NewBackend123", "database", "sql"
]

found = None
for p in passwords:
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password=p,
            host="127.0.0.1",
            port=5432
        )
        print(f"MATCH FOUND! Password is: '{p}'")
        found = p
        conn.close()
        break
    except Exception as ex:
        pass

if not found:
    print("None of the common developer candidate passwords matched.")
