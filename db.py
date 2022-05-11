import sqlite3

db = sqlite3.connect('data')
sql = db.cursor()


def db_start() -> None:
    sql.execute(""" CREATE TABLE IF NOT EXISTS urls(post_id TEXT, url TEXT) """)
    sql.execute(""" CREATE TABLE IF NOT EXISTS photos(post_id TEXT, photo TEXT) """)
    sql.execute(""" CREATE TABLE IF NOT EXISTS text(post_id TEXT, text TEXT) """)


def save_to_sql(data_urls: dict, data_photos: dict, data_text: dict) -> None:

    for url in data_urls:
        sql.execute(f"SELECT post_id FROM urls WHRE post_id = {url[0]['id']}")
        if sql.fetchone() is None:
            sql.execute("INSERT INTO urls VALUES (?, ?)"), (url[0]['id'], url[0]['url'])
            db.commit()

    for photo in data_photos:
        sql.execute(f"SELECT post_id FROM photo WHRE post_id = {photo[0]['id']}")
        if sql.fetchone() is None:
            sql.execute("INSERT INTO photo VALUES (?, ?)"), (photo[0]['id'], photo['photo'])
            db.commit()

    for text in data_text:
        sql.execute(f"SELECT post_id FROM text WHRE post_id = {text[0]['id']}")
        if sql.fetchone() is None:
            sql.execute("INSERT INTO text VALUES (?, ?)"), (text[0]['id'], text['text'])
            db.commit()


