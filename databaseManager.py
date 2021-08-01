import sqlite3
from sqlite3 import Error
from cryptography.fernet import  Fernet

KEY = b'J1la7UmGEikSFvLlCRBWJPnUQr1iViDP5rzH4dH5q9s='
CIPHER_SUITE = Fernet(KEY)


class DatabaseManager:

    def __init__(self,id="",pwd="",msg=""):

        self.id = id
        pwd = pwd.encode('ascii')
        self.pwd =CIPHER_SUITE.encrypt(pwd).decode('ascii')
        self.msg = msg

    def create_connection(self,file):
        conn = None
        try:
            conn = sqlite3.connect(file)
        except Error as e:
            print(e)
        return  conn

    def insert_credential_db(self,conn,task):
        sql = f"INSERT INTO user_credentials(user_id,password,comment)" \
               f"VALUES(?,?,?)"
        cur = conn.cursor()
        cur.execute(sql,task)
        conn.commit()

    def prepare_credentials(self):
        connect = self.create_connection('./bin/data.db')
        credential = (self.id,self.pwd,self.msg)
        self.insert_credential_db(connect,credential)

    def fetch_all(self):
        conn = self.create_connection('./bin/data.db')
        with conn:
            sql = '''SELECT * FROM user_credentials'''
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

        return rows

    def fetch_message(self,id):
        conn = self.create_connection('./bin/data.db')
        with conn:
            sql = '''SELECT comment FROM user_credentials WHERE user_id = ?'''
            cur = conn.cursor()
            cur.execute(sql,(id,))
            rows = cur.fetchall()
            conn.commit()
        return rows

    def update_message(self,msg,usr_id):
        conn = self.create_connection('./bin/data.db')
        with conn:
            sql = '''UPDATE user_credentials
                     SET comment = ?
                     WHERE user_id = ?'''
            cur = conn.cursor()
            cur.execute(sql, (msg,usr_id))
            conn.commit()

    def delete_data(self,usr_id):
        conn = self.create_connection('./bin/data.db')
        with conn:
            sql = 'DELETE FROM user_credentials WHERE user_id=?'
            cur = conn.cursor()
            cur.execute(sql, (usr_id,))
            conn.commit()

    def collect_password(self,id):
        conn = self.create_connection('./bin/data.db')
        with conn:
            sql = '''SELECT password FROM user_credentials WHERE user_id = ?'''
            cur = conn.cursor()
            cur.execute(sql, (id,))
            rows = cur.fetchall()
            conn.commit()
        return rows

    def insert_in_curr_id(self,id):
        conn = self.create_connection('./bin/data.db')
        with conn:
            sql = f"INSERT INTO current_id(insta_id)" \
                  f"VALUES(?)"
            cur = conn.cursor()
            cur.execute(sql, (id,))
            conn.commit()

    def select_from_curr_id(self):
        conn = self.create_connection('./bin/data.db')
        with conn:
            sql = f"SELECT * FROM current_id"
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            conn.commit()
        return rows

    def delete_from_curr_id(self,usr_id):
        conn = self.create_connection('./bin/data.db')
        with conn:
            sql = 'DELETE FROM current_id WHERE insta_id=?'
            cur = conn.cursor()
            cur.execute(sql, (usr_id,))
            conn.commit()