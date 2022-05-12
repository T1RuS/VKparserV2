from multiprocessing import shared_memory
from settings import NAME_INDICATOR, DICT_FILES


def get_indicator():
    try:
        indicator = shared_memory.SharedMemory(create=True, name=NAME_INDICATOR, size=5)
        indicator.buf[0] = True
        indicator.buf[1] = 1
        indicator.buf[2] = 2
        indicator.buf[3] = 3
        indicator.buf[4] = 1

    except:
        indicator = shared_memory.SharedMemory(name=NAME_INDICATOR)
        indicator.buf[4] += 1
    return indicator
