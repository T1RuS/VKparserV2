from time import sleep
from settings import DICT_FILES
from threading import Thread

from process2_shar import get_indicator
from process2_threads import ThreadsReadData


indicator = get_indicator()
threads_read = ThreadsReadData(DICT_FILES[str(indicator.buf[1])],
                               DICT_FILES[str(indicator.buf[2])],
                               DICT_FILES[str(indicator.buf[3])])
threads_read.start_threads()

THREADS_DICT = {
        '0': threads_read.start_read_urls,
        '1': threads_read.start_read_photos,
        '2': threads_read.start_read_photos,
    }

i = True


def pr():
    threads_read.start_read_urls()
    threads_read.start_read_photos()
    threads_read.start_read_text()
    sleep(1)


while i:
    if True:
        Thread(target=pr).start()
        # сделать в main.py
        while threads_read.threads_working():
            print(threads_read.threads_working())
            sleep(0.2)
        data_urls = threads_read.data_urls
        data_photos = threads_read.data_photos
        data_text = threads_read.data_text

        print(data_urls['post0'][0]['id'])

        for i in data_urls:
            print(type(i))

        indicator.buf[0] = True
        i = False
    else:
        sleep(1)
