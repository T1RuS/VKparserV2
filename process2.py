from multiprocessing import shared_memory
from time import sleep

buf = shared_memory.SharedMemory(create=True, name='q', size=3)

for i in range(100):
    print(i)
    buf.buf[0] = i
    sleep(2)