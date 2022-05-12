from time import sleep
from settings import DICT_FILES
from threading import Thread
import threading

from process2_shar import get_indicator
from process2_threads import ThreadsReadData
from db import save_to_sql


indicator = get_indicator()
threads_read = ThreadsReadData(DICT_FILES[str(indicator.buf[1])],
                               DICT_FILES[str(indicator.buf[2])],
                               DICT_FILES[str(indicator.buf[3])])
threads_read.start_threads()
print(threading.enumerate())

THREADS_DICT = {
        '0': threads_read.start_read_urls,
        '1': threads_read.start_read_photos,
        '2': threads_read.start_read_photos,
    }


def pr():
    threads_read.start_read_urls()
    threads_read.start_read_photos()
    threads_read.start_read_text()


while True:
    if not indicator.buf[0]:
        Thread(target=pr).start()

        while threads_read.threads_working():
            sleep(0.2)

        data_urls = threads_read.data_urls
        data_photos = threads_read.data_photos
        data_text = threads_read.data_text

        save_to_sql(data_urls, data_photos, data_text)

        if indicator.buf[4] == 2:
            print('Управление передано процессу main')
            indicator.buf[0] = True
        print(threading.enumerate())
    else:
        sleep(1)
