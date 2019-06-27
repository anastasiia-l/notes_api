import os
from sanic import Sanic
from sanic import Blueprint

from api.settings import scoped_session
from api.models import User


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

    @app.middleware('request')
    async def get_requests_user(request):
        if request.token:
            user = None
            with scoped_session() as session:
                user = session.query(User).filter_by(token=request.token).first()._asdict()
            request["user"] = user

    app.go_fast(host=os.environ.get('HOST'), port=os.environ.get('PORT'), debug=True, workers=os.cpu_count())
