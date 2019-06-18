from functools import wraps
from sanic.response import json

from api.settings import scoped_session
from api.models import User


def _check_request_for_authorization_status(request):
    user = None
    with scoped_session() as session:
        user = session.query(User).filter_by(token=request.token).first()
    return user is not None


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):

            is_authorized = _check_request_for_authorization_status(request)

            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({'status': 'not_authorized'}, 403)
        return decorated_function
    return decorator
