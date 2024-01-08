import logging
import asyncio
import sys
import argparse
import time
import contextlib

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('streamReader.log', 'a', 'utf-8')
handler.setFormatter(logging.Formatter("%(asctime)s;%(levelname)s;%(message)s"))
logger.addHandler(handler)

async def cleanup(process):
    if process:
        process.terminate()
        await process.wait()
    logging.info('Process cleaned up')

async def read_stream(process, buffer, match_string='iteration 2'):
    while True: 
        print("!")
        print("Buffer size is: " + str(buffer))
        output = await process.stdout.read(buffer)
        print("THE SUBPROCESS OUTPUT $$$$$$$$$$")
        print(output)
        if(output):
            decoded_output = output.decode('utf-8')
            if(match_string in decoded_output):
                await worker(decoded_output)
        else:
            logging.info("Stream ended")
            break
    # except asyncio.CancelledError:
    #     logging.exception('Exception occured')
    #     logging.info('Cleaning up process')
    #     cleanup(process)

async def worker(decoded_output):
    logging.info('Stream fragmenet is: ' + decoded_output[:5])
    # print(output.decode('utf-8'))
    # if(b'iteration 2' in output):
    #     logging.info('Found the target string doing some other operation')
    #     logging.info('Stream fragmenet is: ' + output.decode('utf-8')[:10])

async def is_running(process):
    print("Async process is running")
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(process.wait(), 1e-6)
    return process.returncode is None

def parse_args():
    parser = argparse.ArgumentParser(description="""Reads process standard output stream asynchronosuly
                                                    and depending on some matching condition does an operation, 
                                                    program has two options either provide the process as an argument
                                                    or pipe the process standard output to the program""",
                                    usage='\n%(prog)s [options] \n<stream> | %(prog)s [options]')
    parser.add_argument('--log', type=str, default='INFO',
                        help='Log level')
    parser.add_argument('--process', type=str, default='INFO',
                        help='Stream to read')
    parser.add_argument('--buffer', type=int, default=1024,
                        help='Buffer size')
    return parser.parse_args()

async def main():
    args = parse_args()
    if(len(sys.argv) > 1 and '--process' in sys.argv):
        process = await asyncio.subprocess.create_subprocess_shell(
            args.process,
            stdout=asyncio.subprocess.PIPE,
        )
        await read_stream(process, args.buffer)
    else:
        process = await asyncio.subprocess.create_subprocess_shell(
            sys.stdin.readline().strip(),
            stdout=asyncio.subprocess.PIPE,
        )
        await read_stream(process, args.buffer)

if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    logging.info(f"{__file__} executed in {elapsed:0.2f} seconds.")
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

