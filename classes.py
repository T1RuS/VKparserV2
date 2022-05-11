from threading import Thread, Lock, Condition
import json

from settings import URLS_FILE, PHOTOS_FILE, TEXT_FILE


class ProcessingData:
    def __init__(self) -> None:
        self.news_data: list = []

    def _cleaned_data(self, name: str, ) -> dict:
        data: dict = {}
        for i in range(len(self.news_data)):
            data["".join(['post', str(i)])] = []
            data["".join(['post', str(i)])].append({
                'id': self.news_data[i].post_id,
                name: getattr(self.news_data[i], name)
            })

        return data

    def unique_data(self, data: list) -> None:
        if len(self.news_data) == 0:
            self.news_data.append(data[0])
        for i in data:
            count: int = True
            for j in self.news_data:
                if i.post_id == j.post_id:
                    count = False
                    break

            if count:
                self.news_data.append(i)

        print(f'Всего уникальных новостей: {len(self.news_data)}.')


class ThreadsSaveData(ProcessingData):
    def _urls_save_to_file(self, data: dict) -> None:
        with self.__urls_thread_lock:
            print(f'Сохранение в файл {URLS_FILE}')
            self.__threads_working += 1
            with open(URLS_FILE, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            self.__threads_working -= 1

    def _photos_save_to_file(self, data: dict) -> None:
        with self.__photos_thread_lock:
            print(f'Сохранение в файл {PHOTOS_FILE}')
            self.__threads_working += 1
            with open(PHOTOS_FILE, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            self.__threads_working -= 1

    def _text_save_to_file(self, data: dict) -> None:
        with self.__text_thread_lock:
            print(f'Сохранение в файл {TEXT_FILE}')
            self.__threads_working += 1
            with open(TEXT_FILE, 'w', encoding='utf-8') as outfile:
                json.dump(data, outfile, indent=4, ensure_ascii=False)
            self.__threads_working -= 1

    def _read_file(self, file_name: str) -> None:
        with self.__read_thread_lock:
            self.__threads_working += 1
            with open(file_name, 'r', encoding='utf-8') as outfile:
                print(f'Файл прочитан: {file_name}.')
            self.__threads_working -= 1

    def __urls_thread_func(self) -> None:
        print(f'Поток на запись в {URLS_FILE} запущен.')
        while True:
            with self.__urls_thread_cond:
                self.__urls_thread_cond.wait()
                if not self.__threads_started:
                    break
                self._urls_save_to_file(self._cleaned_data('url'))

    def __photos_thread_func(self) -> None:
        print(f'Поток на запись в {PHOTOS_FILE} запущен.')
        while True:
            with self.__photos_thread_cond:
                self.__photos_thread_cond.wait()
                if not self.__threads_started:
                    break
                self._photos_save_to_file(self._cleaned_data('photo'))

    def __text_thread_func(self) -> None:
        print(f'Поток на запись в {TEXT_FILE} запущен.')
        while True:
            with self.__text_thread_cond:
                self.__text_thread_cond.wait()
                if not self.__threads_started:
                    break
                self._text_save_to_file(self._cleaned_data('text'))

    def __read_thread_func(self) -> None:
        print('Поток на чтение запущен.')
        while True:
            with self.__read_thread_cond:
                self.__read_thread_cond.wait()
                if not self.__threads_started:
                    break
                self._read_file(self.file_name)

    def __init__(self) -> None:
        super().__init__()
        self.__urls_thread: Thread = Thread(target=self.__urls_thread_func, daemon=True)
        self.__photos_thead: Thread = Thread(target=self.__photos_thread_func, daemon=True)
        self.__text_thread: Thread = Thread(target=self.__text_thread_func, daemon=True)
        self.__read_thread: Thread = Thread(target=self.__read_thread_func, daemon=True)

        self.__urls_thread_lock: Lock = Lock()
        self.__photos_thread_lock: Lock = Lock()
        self.__text_thread_lock: Lock = Lock()
        self.__read_thread_lock: Lock = Lock()

        self.__urls_thread_cond: Condition = Condition()
        self.__photos_thread_cond: Condition = Condition()
        self.__text_thread_cond: Condition = Condition()
        self.__read_thread_cond: Condition = Condition()

        self.__threads_working: int = 0
        self.file_name: str = None
        self.__threads_started = False

        print('Потоки успешно созданы.')

    def start_threads(self) -> None:
        if self.__threads_started:
            return print('Потоки запущены')
        print('Потоки запущены.')
        self.__threads_started = True
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

    def stop_threads(self) -> print:
        if self.__threads_started:
            self.__threads_started = False
            with self.__urls_thread_cond:
                self.__urls_thread_cond.notify()

            with self.__photos_thread_cond:
                self.__photos_thread_cond.notify()

            with self.__text_thread_cond:
                self.__text_thread_cond.notify()

            with self.__read_thread_cond:
                self.__read_thread_cond.notify()

            return print('Потоки остановлены.')

        return print('Потоки не запущены.')

    def threads_working(self):
        if self.__threads_working > 0:
            return True
        return False

