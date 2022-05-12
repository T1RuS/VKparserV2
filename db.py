import sqlite3


db = sqlite3.connect('data')
sql = db.cursor()


def db_start() -> None:
    sql.execute(""" CREATE TABLE IF NOT EXISTS urls(post_id TEXT, url TEXT) """)
    sql.execute(""" CREATE TABLE IF NOT EXISTS photos(post_id TEXT, photo TEXT) """)
    sql.execute(""" CREATE TABLE IF NOT EXISTS text(post_id TEXT, text TEXT) """)


def save_to_sql(data_urls: dict, data_photos: dict, data_text: dict) -> None:

    for url in data_urls.values():
        sql.execute(f"SELECT post_id FROM urls WHERE post_id = '{url[0]['id']}'")
        if sql.fetchone() is None:
            sql.execute("INSERT INTO urls VALUES (?, ?)", (url[0]['id'], url[0]['url']))
            db.commit()

    for photo in data_photos.values():
        sql.execute(f"SELECT post_id FROM photos WHERE post_id = '{photo[0]['id']}'")
        if sql.fetchone() is None:
            if isinstance(photo[0]['photo'], list):
                list_photos: str = ''
                for i in photo[0]['photo']:
                    list_photos += i
                    list_photos += '\n'

                sql.execute("INSERT INTO photos VALUES (?, ?)", (photo[0]['id'], list_photos))
                db.commit()
            else:
                sql.execute("INSERT INTO photos VALUES (?, ?)", (photo[0]['id'], photo[0]['photo']))
                db.commit()

    for text in data_text.values():
        sql.execute(f"SELECT post_id FROM text WHERE post_id = '{text[0]['id']}'")
        if sql.fetchone() is None:
            sql.execute("INSERT INTO text VALUES (?, ?)", (text[0]['id'], text[0]['text']))
            db.commit()


