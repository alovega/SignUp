# sign-up-portal-with-authentication
This is a simple practical exercise of a sign up page together with its authentication
this is the link of my api https://git.heroku.com/alovegasignup-api-heroku.git hosted in heroku
**What does this repository do?**
have CRUD methods for login sign out and signin

**Description of tasks completed**
have the following endpoints
api.add_resource(UserRegister, '/user/register', endpoint='userregister')
api.add_resource(UserLogin, '/user/login', endpoint='userlogin')
api.add_resource(HelloWorld, '/')
**how should it be manually tested**
after cloning cd into it and RUN run.py in your cmd
*using postman test every endpoint above  with this header:
key: Content-Type value:application/json
to test authentication, add this header
Key:Authorization value:JWT token