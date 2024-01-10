## Purpose
A simple script that reads the output of a process and depending on a matched string it does some work, the work is simulated by `work()` function, it simply simulates it by `time.sleep()` and at the same time it continues to read the output of the process and writing it into the buffer. There are two different buffers output buffer and archive buffer, output buffer holds the amount of bytes where the match_string will be looked in, if match_string found buffer will be flushed, if not found it will be archived into archive buffer. Archive buffer will be flushed when it reaches the maximum size of the buffer. 

## Usage
There is no dependency for this project. Just run the streamRead.py as shown below, bare minimum arguments are required to run the script are as follows

```bash
python streamRead.py --match_string "ERROR" --process "python3 server.py"
```

