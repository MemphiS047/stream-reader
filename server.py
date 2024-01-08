# Function that generates dummy server log every 3 seconds

import time
import logging 
import sys
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('server.log', 'a', 'utf-8')
handler.setFormatter(logging.Formatter("%(asctime)s;%(levelname)s;%(message)s"))
logger.addHandler(handler)

def dummyServer():
    logger.info("Server started")
    i = 0
    while True:
        print("iteration " + str(i))
        logger.info("iteration " + str(i))
        i += 1
        sys.stdout.flush()
        time.sleep(3)

dummyServer()