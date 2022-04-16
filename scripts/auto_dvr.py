#!/usr/bin/env python3
from dronekit import connect

import click
from datetime import datetime
from pathlib import Path
import signal
import subprocess
import time

@click.command()
@click.option('-c', '--connection', default='tcp:127.0.0.1:5760')
@click.option('-o', '--output_dir', default='.')
@click.option('-w', '--width', default=1280)
@click.option('-h', '--height', default=720)
@click.option('-r', '--fps', default=30)
def main(connection, output_dir, width, height, fps):
    print("Connecting to mavlink")
    vehicle = connect(connection, wait_ready=True)

    while True:

        print("Waiting for armed")

        while not vehicle.armed:
            time.sleep(1)

        print("Starting stream")
        now = datetime.now()
        t_stamp = now.strftime("%Y%m%d_%H%M%S")
        output_path = Path(output_dir) / f"{t_stamp}.mp4"
        output_path = str(output_path)
        print(f"Saving DVR to {output_path:s}")

        cmd = [
            "gst-launch-1.0",
            "-v",
            "-e",
            "v4l2src",
            "device=/dev/video0",
            "!",
            "video/x-h264,",
            f"width={width:d},",
            f"height={height:d},",
            f"framerate={fps:d}/1",
            "!",
            "h264parse",
            "!",
            "mp4mux",
            "!",
            "filesink",
            f"location={output_path:s}"
        ]
        print(f"Running: {' '.join(cmd)}")
        proc = subprocess.Popen(cmd)

        while vehicle.armed:
            time.sleep(1)

        print("Terminating recording")

        proc.send_signal(signal.SIGINT)
        proc.wait()


if __name__ == '__main__':
    main()
