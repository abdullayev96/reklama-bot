import sqlite3 as sq

class Database:
    def __init__(self, db_name):
        self.connect = sq.connect(db_name, check_same_thread=False)
        self.cursor = self.connect.cursor()

    def create_user(self, chat_id):
        self.cursor.execute("""insert into user(chat_id) values (?)""", (chat_id, ))
        self.connect.commit()

    def update_user_data(self, chat_id, key, value):
        self.cursor.execute(f"""update user set {key} = ? where chat_id = ?""", (value, chat_id))
        self.connect.commit()

    def get_user_chat_by_id(self, chat_id):
        self.cursor.execute("""select * from user where chat_id = ?""", (chat_id, ))
        user = dict_fetchone(self.cursor)
        return user



def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

