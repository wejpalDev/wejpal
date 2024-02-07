import threading
import uuid
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.core.mail import EmailMessage
from django.conf import settings







class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email= email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_activation_email(user, request):
    current_site = get_current_site(request)
    subject= 'Activate your account'
    body = render_to_string('authentications/activate.html',{
        'user': user,
        'domain': current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user)
    })

    email = EmailMessage(subject=subject, body=body,from_email=settings.EMAIL_FROM_USER,
                 to=[user.email]
                 )
    EmailThread(email).start()

def send_otp_email(user, request):
    subject= 'Activate your account'
    body = "Your OTP is " + user.sub

    email = EmailMessage(subject=subject, body=body,from_email=settings.EMAIL_FROM_USER,
                 to=[user.email]
                 )
    EmailThread(email).start()



class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp))


account_activation_token = TokenGenerator()