import os
from sanic import Sanic


def create_app():

    app = Sanic(__name__)

    from .controllers import UserController, Registration, Auth
    app.add_route(UserController.as_view(), '/api/user')
    app.add_route(Registration.as_view(), '/auth/register')
    app.add_route(Auth.as_view(), '/auth/login')

    app.go_fast(debug=True, workers=os.cpu_count())
