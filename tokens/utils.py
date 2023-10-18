from rest_framework_simplejwt.tokens import AccessToken
from authentications.models import User
from .models import Token, TokenHistory
from datetime import datetime
from django.db import transaction
from rest_framework.exceptions import ParseError

def create_user_balance(user):
    current_date = datetime.now()
    new_user_balance = 1000
    is_exisiting = True

    try:
        user_token = Token.objects.get(user=user)
        return user_token
    except Token.DoesNotExist:
        is_exisiting = False

    try:
        user_token = Token.objects.create(user=user,balance=new_user_balance,paused_balance=0,created_at=current_date,updated_at=current_date)
    except:
        raise ParseError("Could not update wallet history")

    return user_token


def increase_balance(user, amount):
    try:
        user_token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        user_token = Token.objects.create(user=user,balance=new_user_balance,paused_balance=0,created_at=current_date,updated_at=current_date)

    current_date = datetime.now()
    new_balance = user_token.balance + amount
    
    with transaction.atomic():
        try:
            token_history = TokenHistory.objects.create(token=user_token,balance_before=user_token.balance,balance_after=new_balance,created_at=current_date,updated_at=current_date)
        except:
            raise ParseError("Could not update wallet history")

        try:
            user_token.balance = new_balance
            user_token.updated_at = current_date
            user_token.save()
        except:
            raise ParseError("Could not increase balance of user by " + amount)

    return {"balance": new_balance}


def decrease_balance(user, amount):
    try:
        user_token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        raise ParseError("Could not find the user wallet")

    current_date = datetime.now()
    new_balance = user_token.balance - amount
    
    with transaction.atomic():
        try:
            token_history = TokenHistory.objects.create(token=user_token,balance_before=user_token.balance,balance_after=new_balance,created_at=current_date,updated_at=current_date)
        except:
            raise ParseError("Could not update wallet history")

        try:
            user_token.balance = new_balance
            user_token.updated_at = current_date
            user_token.save()
        except:
            raise ParseError("Could not decrease balance of user by " + amount)

    return {"balance": new_balance}


def pause_balance(user, amount):
    try:
        user_token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        raise ParseError("Could not find the user wallet")

    current_date = datetime.now()
    new_balance = user_token.balance - amount
    
    with transaction.atomic():
        try:
            token_history = TokenHistory.objects.create(token=user_token,balance_before=user_token.balance,balance_after=new_balance,created_at=current_date,updated_at=current_date)
        except:
            raise ParseError("Could not update wallet history")

        try:
            user_token.balance = new_balance
            user_token.paused_balance = user_token.paused_balance + amount
            user_token.updated_at = current_date
            user_token.save()
        except:
            raise ParseError("Could not pause balance of user by " + amount)

    return {"balance": new_balance}


def reverse_pause_balance(user, amount):
    try:
        user_token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        raise ParseError("Could not find the user wallet")

    current_date = datetime.now()
    new_balance = user_token.balance + amount
    
    with transaction.atomic():
        try:
            token_history = TokenHistory.objects.create(token=user_token,balance_before=user_token.balance,balance_after=new_balance,created_at=current_date,updated_at=current_date)
        except:
            raise ParseError("Could not update wallet history")

        try:
            user_token.balance = new_balance
            user_token.paused_balance = user_token.paused_balance - amount
            user_token.updated_at = current_date
            user_token.save()
        except:
            raise ParseError("Could not resume balance of user by " + amount)

    return {"balance": new_balance}