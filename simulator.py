import random

voltage = 12.8
encoder_position = 0
telemetry = []

for time in range(60):

    # Robot's commanded power changes throughout the run
    if time < 5:
        motor_command = time / 10
    elif time < 45:
        motor_command = random.uniform(0.4, 1.0)
    else:
        motor_command = random.uniform(0.1, 0.5)

    # Most of the time load is moderate
    load = random.uniform(0.15, 0.4)

    # Simulate a heavy load / obstruction from seconds 25-30
    if 25 <= time <= 30:
        load = random.uniform(0.8, 0.95)

    # Motor behavior
    rpm = motor_command * 1800 * (1 - load)
    rpm += random.uniform(-30, 30)
    rpm = max(0, rpm)

    current = motor_command * 4 + load * 3
    current += random.uniform(-0.2, 0.2)
    current = max(0, current)

    # Battery slowly drains, with extra voltage drop under high current
    voltage -= 0.003 + current * 0.001

    # Pretend encoder has 1000 ticks per revolution
    rotations_per_second = rpm / 60
    encoder_position += rotations_per_second * 1000

    reading = {
        "time": time,
        "motor_command": round(motor_command, 2),
        "load": round(load, 2),
        "rpm": round(rpm, 1),
        "current": round(current, 2),
        "voltage": round(voltage, 2),
        "encoder_position": round(encoder_position)
    }

    telemetry.append(reading)

for reading in telemetry:
    print(reading)