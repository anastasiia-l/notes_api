import os
from sanic import Sanic
from sanic import Blueprint


def create_app():

    app = Sanic(__name__)

    from .controllers import UserController, Registration, Auth, NoteController

    auth_blueprint = Blueprint("auth", "/auth")
    api_blueprint = Blueprint("api", "/api")

    auth_blueprint.add_route(Registration.as_view(), "/register")
    auth_blueprint.add_route(Auth.as_view(), "/login")

    api_blueprint.add_route(UserController.as_view(), "/user")
    api_blueprint.add_route(NoteController.as_view(), "/note")

    app.blueprint(auth_blueprint)
    app.blueprint(api_blueprint)

    app.go_fast(debug=True, workers=os.cpu_count())
