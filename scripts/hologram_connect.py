#!/usr/bin/env python3
import time, sys
from Hologram.CustomCloud import CustomCloud

PRE_DELAY = 10
RETRY_DELAY = 10

print("Starting connect script")
print("Waiting {:d} seconds".format(PRE_DELAY))
time.sleep(PRE_DELAY)

cloud = CustomCloud(None, network='cellular')
cloud.network.disable_at_sockets_mode()

while cloud.network.getConnectionStatus() == 0:
    print("Cloud is not connected")
    res = cloud.network.connect()
    print("Connection success: {}".format(res))
    if res:
        sys.exit(0)
    else:
        time.sleep(RETRY_DELAY)
