import json
import psycopg2
from psycopg2.extras import RealDictCursor


class UserDb:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(host='localhost', dbname='flask_api', user='postgres',
                                                password='LUG4Z1V4', port=5432)
        except:
            print("Unable to connect to the database")

    def getConnection(self):
        return self.connection

    # User
    def insert_user(self, UserApi):
        sql = """INSERT INTO users(email, phone_number, username, password) 
        VALUES (%s,%s,%s,%s)"""
        # get connection
        cur = self.connection.cursor()
        # insert into database
        cur.execute(sql, (UserApi.email, UserApi.phone_number,UserApi.username,UserApi.password))
        self.connection.commit()
        cur.close()

    def get_user_by_username(self, username):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("""SELECT email, phone_number,username,password from users 
                      where username = %(username)s """,
                     {'username': username})
        rows = cur.fetchall()
        return rows

    def get_all(self):
        cur = self.connection.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, email, phone_number, username,password  from users")
        rows = cur.fetchall ()
        return rows

    def check_user_exist_by_username(self, username):
        cur = self.connection.cursor (cursor_factory=RealDictCursor)
        cur.execute ("SELECT id, username, password from users where username = %(username)s", {'username':
                                                                                                username})
        rows = cur.fetchone ()
        if rows:
            return True
        else:
            return False
        cur.close ()