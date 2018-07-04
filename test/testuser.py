import unittest
from user import app
import psycopg2


class TestUserModel(unittest.TestCase):

    def setUp(self):
            try:
                self.connection = psycopg2.connect(host='localhost', dbname='test_db', user='postgres',
                                                    password='LUG4Z1V4', port=5433)
            except:
                print ("Unable to connect to the database")

            self.client = app.test_client()

    def test_user_registration(self):
        request ={"email":"alovega@gmail.com","phone_number":"+254717316934","username":"kevin","password":"1234"}
        res = self.client.post("/user/register",json=request)
        self.assertEqual(res.status_code,202)

    def test_user_login(self):
        request = {"username":"kevin","password":"1234"}
        res = self.client.post("/user/login",json=request)
        self.assertEqual(res.status_code,202)

    def test_user_registration_with_empty_email(self):
        request = {"email":"", "username": "kevin", "password": "1234"}
        res = self.client.post ("/user/register", json=request)
        self.assertEqual (res.status_code, 500)


    def test_user_registration_with_empty_username(self):
        request = {"email": "alovegakevin@gmail.com", "username": "", "password": "1234"}
        res = self.client.post ("/user/register", json=request)
        self.assertEqual (res.status_code, 404)

    def test_user_registration_with_empty_password(self):
        request = {"email": "alovegakevin@gmail.com", "username": "kevin", "password": ""}
        res = self.client.post ("/user/register", json=request)
        self.assertEqual (res.status_code, 500)

    def test_user_registration_with_empty_data(self):
        request = {"email": "", "username": "", "password": ""}
        res = self.client.post ("/user/register", json=request)
        self.assertEqual (res.status_code, 404)

    def test_user_login_with_wrong_password(self):
        request = {"username": "kevin", "password": "1222"}
        res = self.client.post ("/auth/login", json=request)
        self.assertEqual (res.status_code, 404)

    def test_user_login_with_wrong_username(self):
        request = {"username": "kev", "password": "1234"}
        res = self.client.post ("/user/login", json=request)
        self.assertEqual (res.status_code, 404)

    s


if __name__ == '__main__':
    unittest.main()