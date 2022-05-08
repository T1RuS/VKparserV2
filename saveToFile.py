from threading import Thread, Lock
import json

from settings import URLS_FILE, PHOTOS_FILE, TEXT_FILE

DICT_FILES = {
    '1': URLS_FILE,
    '2': PHOTOS_FILE,
    '3': TEXT_FILE,
}


class SaveToFile:
    def __init__(self, news_data: list, num: int) -> None:
        self.urls_thread_lock: Lock = Lock()
        self.photos_thread_lock: Lock = Lock()
        self.text_thread_lock: Lock = Lock()
        self.news_data = news_data
        self.read_file_num = num

    def _get_data(self, name: str, ) -> dict:
        data: dict = {}
        for i in range(len(self.news_data)):
            data["".join(['post', str(i)])] = []
            data["".join(['post', str(i)])].append({
                'id': self.news_data[i].post_id,
                name: getattr(self.news_data[i], name)
            })

        return data

    def save_to_file(self) -> None:
        def thread_urls():
            with self.urls_thread_lock:
                print('Сохранение в файл data_urls.json')
                with open(URLS_FILE, 'w', encoding='utf-8') as outfile:
                    json.dump(self._get_data('url'), outfile, indent=4, ensure_ascii=False)

        thread_1: Thread = Thread(target=thread_urls)

        def thread_photo():
            with self.text_thread_lock:
                print('Сохранение в файл data_photos.json')
                with open(PHOTOS_FILE, 'w', encoding='utf-8') as outfile:
                    json.dump(self._get_data('photo'), outfile, indent=4, ensure_ascii=False)

        thread_2: Thread = Thread(target=thread_photo)

        def thread_text():
            with self.photos_thread_lock:
                print('Сохранение в файл data_text.json')
                with open(TEXT_FILE, 'w', encoding='utf-8') as outfile:
                    json.dump(self._get_data('text'), outfile, indent=4, ensure_ascii=False)

        thread_3: Thread = Thread(target=thread_text)

        def read(name_file: str):
            with open(name_file, 'r', encoding='utf-8') as outfile:
                print(f'Файл прочитан: {name_file}')

        if self.read_file_num == 0:
            thread_1.start()
            thread_2.start()
            thread_3.start()
        elif self.read_file_num == 1:
            thread_4 = Thread(target=read, args=(DICT_FILES['1'],))
            thread_4.start()
            thread_2.start()
            thread_3.start()
        elif self.read_file_num == 2:
            thread_4 = Thread(target=read, args=(DICT_FILES['2'],))
            thread_4.start()
            thread_1.start()
            thread_3.start()
        elif self.read_file_num == 3:
            thread_4 = Thread(target=read, args=(DICT_FILES['3'],))
            thread_4.start()
            thread_1.start()
            thread_2.start()


