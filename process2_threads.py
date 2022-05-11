from threading import Thread, Lock, Condition
import json
from time import sleep


class ThreadsReadData:
    def _urls_read_to_file(self) -> None:
        with self.__urls_thread_lock:
            with open(self.urls_file_name, 'r', encoding='utf-8') as outfile:
                data = outfile.read()

            data = json.loads(data)
            self.data_urls: dict = data
            self.__threads_working -= 1
            print(f'Чтение файла {self.urls_file_name}')

    def _photos_read_to_file(self) -> None:
        with self.__photos_thread_lock:
            with open(self.photos_file_name, 'r', encoding='utf-8') as outfile:
                data = outfile.read()

            data = json.loads(data)
            self.data_photos: dict = data

            self.__threads_working -= 1
            print(f'Чтение файла {self.photos_file_name}')

    def _text_read_to_file(self):
        with self.__text_thread_lock:
            with open(self.text_file_name, 'r', encoding='utf-8') as outfile:
                data = outfile.read()

            data = json.loads(data)
            self.data_text: dict = data
            self.__threads_working -= 1
            print(f'Чтение файла {self.text_file_name}')

    def __urls_thread_func(self) -> None:
        print(f'Поток на чтение файла {self.urls_file_name} запущен.')
        while True:
            with self.__urls_thread_cond:
                self.__urls_thread_cond.wait()
                if not self.__threads_started:
                    break
                self._urls_read_to_file()

    def __photos_thread_func(self) -> None:
        print(f'Поток на чтение файла {self.photos_file_name} запущен.')
        while True:
            with self.__photos_thread_cond:
                self.__photos_thread_cond.wait()
                if not self.__threads_started:
                    break
                self._photos_read_to_file()

    def __text_thread_func(self) -> None:
        print(f'Поток на чтение файла {self.text_file_name} запущен.')
        while True:
            with self.__text_thread_cond:
                self.__text_thread_cond.wait()
                if not self.__threads_started:
                    break
                self._text_read_to_file()

    def __init__(self, urls_file_name: str, photos_file_name: str, text_file_name: str) -> None:
        super().__init__()
        self.__urls_thread: Thread = Thread(target=self.__urls_thread_func, daemon=True)
        self.__photos_thead: Thread = Thread(target=self.__photos_thread_func, daemon=True)
        self.__text_thread: Thread = Thread(target=self.__text_thread_func, daemon=True)

        self.__urls_thread_lock: Lock = Lock()
        self.__photos_thread_lock: Lock = Lock()
        self.__text_thread_lock: Lock = Lock()

        self.__urls_thread_cond: Condition = Condition()
        self.__photos_thread_cond: Condition = Condition()
        self.__text_thread_cond: Condition = Condition()

        self.urls_file_name = urls_file_name
        self.photos_file_name = photos_file_name
        self.text_file_name = text_file_name
        self.__threads_started: bool = False
        self.__threads_working: int = 0

        print('Потоки успешно созданы.')

    def start_threads(self) -> None:
        if self.__threads_started:
            return print('Потоки запущены')
        print('Потоки запущены.')
        self.__threads_started = True
        self.__urls_thread.start()
        self.__photos_thead.start()
        self.__text_thread.start()

    def start_read_urls(self) -> None:
        with self.__urls_thread_cond:
            self.__urls_thread_cond.notify()
            self.__threads_working += 1

    def start_read_photos(self) -> None:
        with self.__photos_thread_cond:
            self.__photos_thread_cond.notify()
            self.__threads_working += 1

    def start_read_text(self) -> None:
        with self.__text_thread_cond:
            self.__text_thread_cond.notify()
            self.__threads_working += 1

    def stop_threads(self) -> print:
        if self.__threads_started:
            self.__threads_started = False
            with self.__urls_thread_cond:
                self.__urls_thread_cond.notify()

            with self.__photos_thread_cond:
                self.__photos_thread_cond.notify()

            with self.__text_thread_cond:
                self.__text_thread_cond.notify()

            return print('Потоки остановлены.')

        return print('Потоки не запущены.')

    def threads_working(self):
        if self.__threads_working > 0:
            return True
        return False
