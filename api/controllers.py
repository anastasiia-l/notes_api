from sanic.response import json
from sanic.views import HTTPMethodView

from .models import User
from .settings import scoped_session


class UserController(HTTPMethodView):

    async def get(self, request):

        with scoped_session() as session:
            stmt = User.__table__.select()
            users = [dict(u) for u in session.execute(stmt)]
        return json({'users': users})

    async def post(self, request):

        email = request.json.get('email')

        with scoped_session() as session:
            user = User(email=email)
            session.add(user)

        return json({'msg': 'Successfully created {}'.format(email)})