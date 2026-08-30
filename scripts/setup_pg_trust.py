import os
import shutil
import subprocess

hba_file = r"C:\Program Files\PostgreSQL\17\data\pg_hba.conf"
bak_file = r"C:\Program Files\PostgreSQL\17\data\pg_hba.conf.bak"

if not os.path.exists(bak_file):
    shutil.copyfile(hba_file, bak_file)
    print("Backed up pg_hba.conf to pg_hba.conf.bak")

with open(hba_file, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "127.0.0.1/32" in line and "scram-sha-256" in line:
        new_lines.append("host    all             all             127.0.0.1/32            trust\n")
    elif "::1/128" in line and "scram-sha-256" in line:
        new_lines.append("host    all             all             ::1/128                 trust\n")
    else:
        new_lines.append(line)

with open(hba_file, "w") as f:
    f.writelines(new_lines)

print("Updated pg_hba.conf to allow local trust authentication.")

pg_ctl = r"C:\Program Files\PostgreSQL\17\bin\pg_ctl.exe"
pg_data = r"C:\Program Files\PostgreSQL\17\data"

res = subprocess.run([pg_ctl, "reload", "-D", pg_data], capture_output=True, text=True)
print("pg_ctl reload output:", res.stdout, res.stderr)
