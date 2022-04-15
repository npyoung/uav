from dronekit import connect
import subprocess
import time

vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)

while True:

    print("Waiting for armed")

    while not vehicle.armed:
        time.sleep(1)

    print("Starting stream")

    cmd = []
    proc = subprocess.Popen(cmd)

    while vehicle.armed:
        sleep(1)

    print("Terminating recording")

    proc.terminate()
    proc.wait()
