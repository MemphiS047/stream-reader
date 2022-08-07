import subprocess
import shlex

def update_jar():
    process = subprocess.Popen(shlex.join(['git', 'pull']), stdout=subprocess.PIPE, shell=True)
    while True:
        output = process.stdout.readline()
        if(output == '' and process.poll() is not None):
            break
        if(b'Already up to date' in output):
            print("Repository is already up to date")  
    rc = process.poll()
    return rc


