with open(r"C:\Program Files\PostgreSQL\17\data\pg_hba.conf", "r") as f:
    for line in f:
        line_s = line.strip()
        if line_s and not line_s.startswith("#"):
            print(line_s)
