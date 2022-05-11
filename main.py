from classes import ThreadsSaveData
from parsing_data import get_data, driver, news
from settings import URL, DICT_FILES

import threading

count: int = 0
try:
    driver.get(url=URL)
    threads_save = ThreadsSaveData(news)
    threads_save.start_threads()
    print(threading.enumerate())

    threads_dict = {
        '0': threads_save.start_save_urls,
        '1': threads_save.start_save_photos,
        '2': threads_save.start_save_text,
        '3': threads_save.start_read,
    }

    while True:
        get_data()
        index: int = count % 4
        if index == 0:
            for i in range(3):
                threads_dict[str(i)]()
        else:
            for i in range(3):
                if i == index - 1:
                    threads_save.start_read(DICT_FILES[str(i+1)])
                else:
                    threads_dict[str(i)]()

        count += 1
        print('Обновление страницы.')
        driver.refresh()
        print(threading.enumerate())

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

