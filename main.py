from classes import ThreadsSaveData
from parsing_data import get_data, driver, news
from settings import URL, DICT_FILES

import threading

count: int = 0
try:
    driver.get(url=URL)
    first_process = ThreadsSaveData(news)
    first_process.start_threads()
    print(threading.enumerate())

    threads_dict = {
        '0': first_process.start_save_urls,
        '1': first_process.start_save_photos,
        '2': first_process.start_save_text,
        '3': first_process.start_read,
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
                    first_process.start_read(DICT_FILES[str(i+1)])
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

