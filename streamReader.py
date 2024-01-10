import asyncio
import time
import argparse
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('streamReader.log', 'a', 'utf-8')
handler.setFormatter(logging.Formatter("%(asctime)s;%(levelname)s;%(message)s"))
logger.addHandler(handler)

# Function that cleans up the process
async def cleanup(process):
    if process:
        process.terminate()
        await process.wait()
    logging.info('Process cleaned up')

# Function that reads the output stream of the server process
async def read_stream(process, match_string, archived_buffer_size, output_buffer_size):
    output_buffer = bytearray(output_buffer_size)
    archived_buffer = bytearray(archived_buffer_size)
    try:
        while True:
            output = await process.stdout.readline()
            output_buffer += output
            archived_buffer += output
            if(match_string in output_buffer.decode('utf-8')):
                await worker()
    except asyncio.CancelledError:
        logging.exception('Exception occured')
        logging.info('Cleaning up process')
        cleanup(process)
        
# Worker function which does some operation, simulated using sleep instead
# of actual  
async def worker():
    print("Worker function called")
    time.sleep(10)
    print("Worker function completed")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--match_string', type=str)
    parser.add_argument('--process', type=str)
    parser.add_argument('--archived_buffer_size', type=int)
    parser.add_argument('--output_buffer_size', type=int)
    return parser.parse_args()

async def main():
    args = parse_args()
    if(args.match_string and args.process):
        process = await asyncio.subprocess.create_subprocess_shell(
            args.process,
            stdout=asyncio.subprocess.PIPE,
        )
        await read_stream(process, args.match_string, args.archived_buffer_size, args.output_buffer_size)
    else:
        print("No match string or process is provided --help for more options")

if __name__ == '__main__':
    asyncio.run(main())