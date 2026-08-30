import sqlite3
import os

files = ['data/bootstrap_stage24.db', 'data/bootstrap_test_idempotency.db', 'data/test_disposable_realtime.db']

for f in files:
    if os.path.exists(f):
        print(f"=== {f} (Size: {os.path.getsize(f):,} bytes) ===")
        conn = sqlite3.connect(f)
        cur = conn.cursor()
        tables = [t[0] for t in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
        for t in tables:
            cnt = cur.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
            print(f"  Table: {t:<22} | Row Count: {cnt}")
        conn.close()
    else:
        print(f"=== {f} NOT FOUND ===")
