from selenium import webdriver
from selenium.webdriver.common.by import By

from models import Feed
from settings import BROWSER_DATA_PATH, DRIVER_PATH


options = webdriver.ChromeOptions()
options.add_argument(BROWSER_DATA_PATH)
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)


def get_data() -> list:
    news: list = []

    try:
        elements: webdriver = driver.find_elements(By.CLASS_NAME, "feed_row ")

        for i in range(11):
            count = 0
            for j in elements[i].find_elements(By.TAG_NAME, "a"):
                if j.text == 'Рекламная запись':
                    count = 1
                    break

            if elements[i].find_element(By.TAG_NAME, "div").get_attribute("id").find('post-') or count == 1:
                continue

            try:
                news.append(Feed())
                news[-1].post_id = elements[i].find_element(By.TAG_NAME, "div").get_attribute("id")
                news[-1].url = elements[i].find_element(By.CLASS_NAME, "post_link").get_attribute("href")
                try:
                    photo = elements[i].find_element(By.CLASS_NAME, "PagePostLimitedThumb")
                    photo = photo.get_attribute("src")
                    news[-1].photo = photo

                except:
                    imgs = elements[i].find_element(By.CLASS_NAME, "wall_text").find_elements(By.TAG_NAME, "a")

                    photos: list = []
                    x: int = 0
                    for img in imgs:
                        if img.get_attribute("aria-label") == "фотография":
                            x = 1
                            s = img.get_attribute("style")
                            res = s[s.find('(') + 1:s.find(')')]
                            photos.append(res)

                    if x == 1:
                        news[-1].photo = photos

                try:
                    news[-1].text = elements[i].find_element(By.CLASS_NAME, "wall_post_text").text
                except:
                    pass

            except:
                pass

        print(f'Новости собраны.')

    except Exception as ex:
        print(ex)

    return news
