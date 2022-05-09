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
    def __urls_save_to_file(self) -> None:
        print('Поток на запись в data_urls.json запущен.')
        while True:
            with self.__urls_thread_cond:
                self.__urls_thread_cond.wait()
                with self.__urls_thread_lock:
                    print('Сохранение в файл data_urls.json')
                    with open(URLS_FILE, 'w', encoding='utf-8') as outfile:
                        json.dump(self._cleaned_data('url'), outfile, indent=4, ensure_ascii=False)

    def __photos_save_to_file(self) -> None:
        print('Поток на запись в data_photos.json запущен.')
        while True:
            with self.__photos_thread_cond:
                self.__photos_thread_cond.wait()
                with self.__photos_thread_lock:
                    print('Сохранение в файл data_photos.json')
                    with open(PHOTOS_FILE, 'w', encoding='utf-8') as outfile:
                        json.dump(self._cleaned_data('photo'), outfile, indent=4, ensure_ascii=False)

    def __text_save_to_file(self) -> None:
        print('Поток на запись в data_text.json запущен.')
        while True:
            with self.__text_thread_cond:
                self.__text_thread_cond.wait()
                with self.__text_thread_lock:
                    print('Сохранение в файл data_text.json')
                    with open(TEXT_FILE, 'w', encoding='utf-8') as outfile:
                        json.dump(self._cleaned_data('text'), outfile, indent=4, ensure_ascii=False)

    def __read_file(self) -> None:
        print('Поток на чтение запущен.')
        while True:
            with self.__read_thread_cond:
                self.__read_thread_cond.wait()
                with self.__read_thread_lock:
                    with open(self.file_name, 'r', encoding='utf-8') as outfile:
                        print(f'Файл прочитан: {self.file_name}.')

    def __init__(self, news_data: list) -> None:
        super().__init__(news_data)
        self.__urls_thread: Thread = Thread(target=self.__urls_save_to_file)
        self.__photos_thead: Thread = Thread(target=self.__photos_save_to_file)
        self.__text_thread: Thread = Thread(target=self.__text_save_to_file)
        self.__read_thread: Thread = Thread(target=self.__read_file)

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

    def __start_to_save_file_urls(self) -> None:
        with self.__urls_thread_cond:
            self.__urls_thread_cond.notify()

    def __start_to_save_file_photos(self) -> None:
        with self.__photos_thread_cond:
            self.__photos_thread_cond.notify()

    def __start_to_save_file_text(self) -> None:
        with self.__text_thread_cond:
            self.__text_thread_cond.notify()

    def __start_read_file(self, file_name: str) -> None:
        self.file_name = file_name
        with self.__read_thread_cond:
            self.__read_thread_cond.notify()

    def start_save_urls(self) -> None:
        Thread(target=self.__start_to_save_file_urls).start()

    def start_save_photos(self) -> None:
        Thread(target=self.__start_to_save_file_photos).start()

    def start_save_text(self) -> None:
        Thread(target=self.__start_to_save_file_text).start()

    def start_read(self, file_name: str) -> None:
        Thread(target=self.__start_read_file, args=(file_name,)).start()
