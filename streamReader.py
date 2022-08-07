import subprocess
import shlex
import concurrent.futures

# Reads the stream of data in this case git pull is used for an example
def read_stream():
    process = subprocess.Popen(shlex.join(['git', 'pull']), stdout=subprocess.PIPE, shell=True)
    while True:
        output = process.stdout.readline()
        if(output == '' and process.poll() is not None):
            break
        if(b'Already up to date' in output):
            print("Repository is already up to date")
            git_update()
    rc = process.poll()
    return rc
# Runs the update operation shell script which pulls repo then replaces the destinated files
def git_update():
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(subprocess.Popen(["/home/yigit/dev/github/stream-reader/updateOperation.sh"], stdin=subprocess.PIPE))

read_stream()