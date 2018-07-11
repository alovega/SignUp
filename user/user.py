from flask_restful import fields, abort
from flask_restful import Resource
from flask_restful import reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required)
from passlib.hash import pbkdf2_sha256 as sha256
from models.models import UserDb
import africastalking


#defines database
userdao = UserDb()


class UserApi(Resource):

    def __init__(self, email, phone_number, username, password):
        self.email = email
        self.phone_number = phone_number
        self.username = username
        self.password = password

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password,hash):
        return sha256.verify(password, hash)


user_fields = {
    'email': fields.String,
    'phone_number': fields.Integer,
    'username': fields.String,
    'password': fields.String
}

reqparse = reqparse.RequestParser()
reqparse.add_argument('email', type=str, required=True, help='please input email', location='json')
reqparse.add_argument('phone_number', type=str, required=True, help='please input phone_No', location='json')
reqparse.add_argument('username', type=str, required=True,help='please input username',location='json')
reqparse.add_argument('password', type=str, required=True, help='please input password', location='json')

reqparse_copy = reqparse.copy()
reqparse_copy.remove_argument('email')
reqparse_copy.remove_argument('phone_number')
reqparse_copy.add_argument('username', type=str, required=True, help='Invalid username', location='json')
reqparse_copy.add_argument('password', type=str, required=True, help='Invalid password', location='json')


class UserRegister(Resource):
    def post(self):
        args = reqparse.parse_args()
        username = args['username']
        phone_number = args['phone_number']
        password = args['password']

        if not username:
            return {"message":"username not valid"}
        elif not phone_number:
            return {"message":"input phone number"}
        elif not password:
            return {"message":"input password"}

        user = UserApi(
            email=args['email'],
            phone_number=args['phone_number'],
            username=args['username'],
            password=args['password']
        )
        if userdao.check_user_exist_by_username(user.username):
            return {"message":"username already used"}
        else:
            user.password = user.generate_hash(user.password)
            userdao.insert_user(user)
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            return {
                'message': 'User{0} was created'.format(user.username),
                'acess_token':access_token,
                'refresh_token':refresh_token
            }

    def get(self):
        result = userdao.get_all()
        return result


class UserLogin(Resource):

    def sms(self):
        args = reqparse_copy.parse_args()
        user = userdao.get_user_by_username(args['username'])
        print (user)
        username = 'sandbox'#user[0]['username']
        apikey ='6302beb1703ac932cd86bcbed82ae52fb5727731d75aaa62f41c32ea314a00a0'
        to = str(user[0]['phone_number']).format(10)

        message = "to complete your login process input this code: 1234567"

        # Initialize SDK
        africastalking.initialize (username, apikey)

        # Initialize a service e.g. SMS
        sms = africastalking.SMS

        sms.send (message, [to], callback=self.on_finish)

    # Or use it asynchronously
    def on_finish(error, response):
            if error is not None:
                raise error
            print (response)


    def post(self):
        args = reqparse_copy.parse_args()
        user = userdao.get_user_by_username(args['username'])
        if not user:
            return {"message": 'User{} doesn\'t exist'.format(args['username'])}

        if UserApi.verify_hash(args.password, user[0]['password']):
            UserLogin.sms(self)
            access_token = create_access_token (identity=user[0]['username'])
            refresh_token = create_refresh_token (identity=user[0]['username'])
            return {
                'message': 'Logged in as {}'.format (user[0]['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {
                'message': 'Wrong credentials provided'
            }

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}