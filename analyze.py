import sqlite3

conn = sqlite3.connect("telemetry.db")
cursor = conn.cursor()

cursor.execute("""
SELECT AVG(rpm)
FROM telemetry
WHERE run_id = 1
""")

average_rpm = cursor.fetchone()[0]
print(average_rpm)

conn.close()