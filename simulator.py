import random
import sqlite3


# --------------------
# DATABASE SETUP
# --------------------

conn = sqlite3.connect("telemetry.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    time INTEGER,
    motor_command REAL,
    rpm REAL,
    current REAL,
    voltage REAL,
    encoder_position INTEGER,
    FOREIGN KEY (run_id) REFERENCES runs(id)
)
""")


# --------------------
# CREATE A NEW RUN
# --------------------

cursor.execute("INSERT INTO runs DEFAULT VALUES")
run_id = cursor.lastrowid

print("Starting run:", run_id)


# --------------------
# SIMULATION
# --------------------

voltage = 12.8
encoder_position = 0

for time in range(60):

    # Motor command changes throughout the run
    if time < 5:
        motor_command = time / 10
    elif time < 45:
        motor_command = random.uniform(0.4, 1.0)
    else:
        motor_command = random.uniform(0.1, 0.5)

    # Normal mechanical load
    load = random.uniform(0.15, 0.4)

    # Simulate heavy load / obstruction
    if 25 <= time <= 30:
        load = random.uniform(0.8, 0.95)

    # Calculate motor RPM
    rpm = motor_command * 1800 * (1 - load)
    rpm += random.uniform(-30, 30)
    rpm = max(0, rpm)

    # Calculate current draw
    current = motor_command * 4 + load * 3
    current += random.uniform(-0.2, 0.2)
    current = max(0, current)

    # Battery voltage slowly decreases
    voltage -= 0.003 + current * 0.001

    # Calculate encoder movement
    rotations_per_second = rpm / 60
    encoder_position += rotations_per_second * 1000

    # Save telemetry reading to database
    cursor.execute("""
    INSERT INTO telemetry
    (run_id, time, motor_command, rpm, current, voltage, encoder_position)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        run_id,
        time,
        motor_command,
        rpm,
        current,
        voltage,
        encoder_position
    ))


# --------------------
# SAVE AND CLOSE
# --------------------

conn.commit()
conn.close()

print("Run complete.")