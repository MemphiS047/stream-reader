import subprocess
import concurrent.futures
import logging
import datetime


# Logging configuration
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('MobileControllerJarUpdate.log', 'a', 'utf-8')
handler.setFormatter(logging.Formatter("%(asctime)s;%(levelname)s;%(message)s"))
logger.addHandler(handler)

# Reads the stream of data in this case git pull is used for an example
def read_stream():
    process = subprocess.Popen(["/home/yigit/dev/github/stream-reader/dummyServer.sh"], stdout=subprocess.PIPE, shell=True)
    while True:
        output = process.stdout.readline()
        if(output == '' and process.poll() is not None):
            break
        if(b'iteration 2' in output):
            logging.info('MobileController.jar updated running updateOperation.sh')
            git_update()
    rc = process.poll()
    return rc
# Runs the update operation shell script which pulls repo then replaces the destinated files
def git_update():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(subprocess.Popen(["/home/yigit/dev/github/stream-reader/updateOperation.sh"], stdin=subprocess.PIPE, shell=True))

read_stream()