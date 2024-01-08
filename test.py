import asyncio
import time


async def read_stream(process):
    buffer = 8
    match_string = 'iteration 2'
    output_buffer = b''
    archived_buffer = b''
    count = 0
    while True:
        print('\n')
        output = await process.stdout.readline()
        output_buffer += output
        archived_buffer += output
        print(output_buffer)
        # print(archived_buffer)
        if(match_string in output_buffer.decode('utf-8')):
            # output_buffer = b''
            if(count == 0):
                await worker()
            count += 1
        # print("THE SUBPROCESS OUTPUT $$$$$$$$$$")
        # print(output)
        # if(output):
        #     decoded_output = output.decode('utf-8')
        #     if(match_string in decoded_output):
        #         print("Math found")
        # else:
        #     break
# Worker function which does some operation, simulated using sleep instead
# of actual operation
async def worker():
    print("Worker function called")
    time.sleep(6)
    print("Worker function completed")

async def main():
    process = await asyncio.subprocess.create_subprocess_shell(
        "python3 server.py",
        stdout=asyncio.subprocess.PIPE,
    )

    await read_stream(process)

if __name__ == '__main__':
    asyncio.run(main())