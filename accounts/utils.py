import threading
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from authentications.models import User
from rest_framework.exceptions import ParseError

def get_logged_in_user(request):
    auth = request.headers.get('Authorization');

    if auth is None:
        raise ParseError("Invalid auth token provided")

    access_token_obj = AccessToken((auth.split(' '))[1])
    user_id=access_token_obj['user_id']
    user=User.objects.get(id=user_id)

    return user