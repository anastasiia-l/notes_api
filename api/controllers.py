from sanic.response import json
from sanic.views import HTTPMethodView

from .models import User
from .settings import scoped_session

from hashlib import sha256
import uuid


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


class Registration(HTTPMethodView):

    async def post(self, request):
        email = request.json.get('email')
        password = sha256(request.json.get('password').encode()).hexdigest()
        birthday = request.json.get('birthday')
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')

        with scoped_session() as session:
            user = User(email=email, birthday=birthday, first_name=first_name, last_name=last_name, password=password)
            session.add(user)

        return json({'msg': 'Successfully created {}'.format(email)})


class Auth(HTTPMethodView):

    async def post(self, request):
        email = request.json.get('email')
        password = sha256(request.json.get('password').encode()).hexdigest()
        token = uuid.uuid4().hex

        with scoped_session() as session:
            user = session.query(User).filter_by(email=email).first()

            if not (user and user.password == password):
                return json({
                    "valid": False,
                    "data": 'Wrong email or password'
                }, status=401)

            user.token = token

        return json({"valid": True, "data": {"access_token": token}})
