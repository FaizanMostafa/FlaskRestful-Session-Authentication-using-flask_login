from config import app, api
from auth import Register, Login, Logout
from views import SecretResource

api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(SecretResource, "/secret")