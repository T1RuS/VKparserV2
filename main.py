import threading
from time import sleep

from classes import ThreadsSaveData
from parsing_data import get_data, driver
from settings import URL, DICT_FILES
from main_shar import get_indicator

count: int = 0
try:
    driver.get(url=URL)
    threads_save = ThreadsSaveData()
    threads_save.start_threads()
    print(threading.enumerate())

    indicator = get_indicator()

    THREADS_DICT = {
        '0': threads_save.start_save_urls,
        '1': threads_save.start_save_photos,
        '2': threads_save.start_save_text,
        '3': threads_save.start_read,
    }

    while True:
        # indicator.buf[0] == 1
        if True:
            print(1)
            threads_save.unique_data(get_data())
            index: int = count % 4
            if index == 0:
                for i in range(3):
                    THREADS_DICT[str(i)]()
            else:
                for i in range(3):
                    if i == index - 1:
                        threads_save.start_read(DICT_FILES[str(i+1)])
                    else:
                        THREADS_DICT[str(i)]()

            count += 1
            print('Обновление страницы.')
            driver.refresh()
            print(threading.enumerate())
            indicator.buf[0] = False
        else:
            sleep(1)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
