from flask import Flask
from flask_restful import Api
from user.user import UserRegister
from user.user import UserLogin
from flask_jwt_extended import JWTManager


app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

api.add_resource(UserRegister, '/user/register', endpoint='userregister')
api.add_resource(UserLogin, '/user/login', endpoint='userlogin')