from selenium import webdriver

from saveToFile import SaveToFile
from get_data import get_data
from settings import BROWSER_DATA_PATH, DRIVER_PATH, URL


options = webdriver.ChromeOptions()
options.add_argument(BROWSER_DATA_PATH)
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)


count: int = 0
try:
    driver.get(url=URL)

    while True:
        index: int = count % 4
        new_data = SaveToFile(get_data(driver), index)
        new_data.save_to_file()
        count += 1
        driver.refresh()

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
