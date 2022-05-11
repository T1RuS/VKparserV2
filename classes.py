from threading import Thread, Lock, Condition
import json

from settings import URLS_FILE, PHOTOS_FILE, TEXT_FILE, DICT_FILES


class GetData:
    def __init__(self, news_data: list) -> None:
        self.news_data = news_data

    def _cleaned_data(self, name: str, ) -> dict:
        data: dict = {}
        for i in range(len(self.news_data)):
            data["".join(['post', str(i)])] = []
            data["".join(['post', str(i)])].append({
                'id': self.news_data[i].post_id,
                name: getattr(self.news_data[i], name)
            })

        return data


class ThreadsSaveData(GetData):
    def _urls_save_to_file(self, data: dict) -> None:
        with self.__urls_thread_lock:
            print('Сохранение в файл data_urls.json')
            with open(URLS_FILE, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)

    def _photos_save_to_file(self, data: dict) -> None:
        with self.__photos_thread_lock:
            print('Сохранение в файл data_photos.json')
            with open(PHOTOS_FILE, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)

    def _text_save_to_file(self, data: dict) -> None:
        with self.__text_thread_lock:
            print('Сохранение в файл data_text.json')
            with open(TEXT_FILE, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)

    def _read_file(self, file: str) -> None:
        with self.__read_thread_lock:
            with open(file, 'r', encoding='utf-8') as outfile:
                print(f'Файл прочитан: {file}.')

    def __urls_thread_func(self) -> None:
        print('Поток на запись в data_urls.json запущен.')
        while True:
            with self.__urls_thread_cond:
                self.__urls_thread_cond.wait()
                self._urls_save_to_file(self._cleaned_data('url'))

    def __photos_thread_func(self) -> None:
        print('Поток на запись в data_photos.json запущен.')
        while True:
            with self.__photos_thread_cond:
                self.__photos_thread_cond.wait()
                self._photos_save_to_file(self._cleaned_data('photo'))

    def __text_thread_func(self) -> None:
        print('Поток на запись в data_text.json запущен.')
        while True:
            with self.__text_thread_cond:
                self.__text_thread_cond.wait()
                self._text_save_to_file(self._cleaned_data('text'))

    def __read_thread_func(self) -> None:
        print('Поток на чтение запущен.')
        while True:
            with self.__read_thread_cond:
                self.__read_thread_cond.wait()
                self._read_file(self.file_name)

    def __init__(self, news_data: list) -> None:
        super().__init__(news_data)
        self.__urls_thread: Thread = Thread(target=self.__urls_thread_func)
        self.__photos_thead: Thread = Thread(target=self.__photos_thread_func)
        self.__text_thread: Thread = Thread(target=self.__text_thread_func)
        self.__read_thread: Thread = Thread(target=self.__read_thread_func)

        self.__urls_thread_lock: Lock = Lock()
        self.__photos_thread_lock: Lock = Lock()
        self.__text_thread_lock: Lock = Lock()
        self.__read_thread_lock: Lock = Lock()

        self.__urls_thread_cond: Condition = Condition()
        self.__photos_thread_cond: Condition = Condition()
        self.__text_thread_cond: Condition = Condition()
        self.__read_thread_cond: Condition = Condition()

        self.file_name: str = None

        print('Потоки успешно созданыю.')

    def start_threads(self) -> None:
        print('Потоки запущены.')
        self.__urls_thread.start()
        self.__photos_thead.start()
        self.__text_thread.start()
        self.__read_thread.start()

    def start_save_urls(self) -> None:
        with self.__urls_thread_cond:
            self.__urls_thread_cond.notify()

    def start_save_photos(self) -> None:
        with self.__photos_thread_cond:
            self.__photos_thread_cond.notify()

    def start_save_text(self) -> None:
        with self.__text_thread_cond:
            self.__text_thread_cond.notify()

    def start_read(self, file_name: str) -> None:
        self.file_name = file_name
        with self.__read_thread_cond:
            self.__read_thread_cond.notify()
