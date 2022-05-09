from classes import ThreadsSaveData
from parsing_data import get_data, driver, news
from settings import URL, DICT_FILES


count: int = 0
try:
    driver.get(url=URL)
    first_process = ThreadsSaveData(news)
    first_process.start_threads()

    threads_dict = {
        '0': first_process.start_save_urls,
        '1': first_process.start_save_photos,
        '2': first_process.start_save_text,
        '3': first_process.start_read,
    }

    while True:
        get_data()
        index: int = count % 4
        for i in range(3):
            if index == i and index != 0:
                threads_dict['4'](DICT_FILES[str(i)])
            else:
                threads_dict[str(i)]()

        count += 1

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

