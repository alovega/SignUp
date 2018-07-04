import psycopg2

try:
    conn = psycopg2.connect(host='localhost',dbname='flask_api',user='postgres',password='LUG4Z1V4', port=5432)
    print('Established')

    def create_table():

        commands = (
            """
            CREATE TABLE IF NOT EXISTS users(id SERIAL PRIMARY KEY,email VARCHAR NOT NULL UNIQUE,
            phone_number INT NOT NULL,username VARCHAR NOT NULL UNIQUE, password VARCHAR NOT NULL)""",
            """CREATE TABLE IF NOT EXISTS 
             revoked_tokens(id SERIAL PRIMARY KEY, jti VARCHAR(256) )""")
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
        conn.close()

except:

    print("I am unable to connect to the database")


if __name__ == '__main__':
    create_table()