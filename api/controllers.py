from hashlib import sha256
import uuid
import datetime

from sanic.response import json
from sanic.views import HTTPMethodView

from .models import User, Note
from .settings import scoped_session
from utils.auth import authorized


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


class NoteController(HTTPMethodView):
    decorators = [authorized()]

    async def get(self, request):
        with scoped_session() as session:
            notes = [ note._asdict() for note in session.query(Note).filter_by(user_id=request['user']['id']) ]

        return json({'notes': notes})

    async def post(self, request):

        title = request.json.get('title')
        text = request.json.get('text')
        current_datetime = datetime.datetime.now()

        with scoped_session() as session:
            note = Note(user_id=request['user']['id'], title=title, text=text, datetime=current_datetime)
            session.add(note)

        return json({'msg': 'Successfully created'})

    async def patch(self, request):
        note_id = request.json.get('id')
        data = request.json.get('data')

        if "id" in data:
            data.pop("id")

        with scoped_session() as session:
            updated_notes = session.query(Note).filter(Note.user_id == request['user']['id'] and Note.id == note_id).update(data)

        return json({'updated': updated_notes})

    async def delete(self, request):
        title = request.json.get('title')

        with scoped_session() as session:
            deleted_notes = session.query(Note).filter(Note.user_id == request['user']['id'] and Note.title == title).delete()

        return json({'deleted': deleted_notes})
