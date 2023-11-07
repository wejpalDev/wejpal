from django.shortcuts import render
from accounts.utils import get_logged_in_user
from rest_framework import generics
from rest_framework import status
from .models import Token, TokenHistory
from rest_framework.response import Response

# Create your views here.
class GetUserToken(generics.GenericAPIView):
    def get(self, request):
        user = get_logged_in_user(request)

        try:
            user_token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            user_token = ''

        content =  {
            'balance': user_token.balance if user_token != '' else 0, 
            'paused': user_token.paused_balance if user_token != '' else 0,
            }

        return Response({"status": "success","data": content}, status=status.HTTP_200_OK)


class GetUserTokenHistory(generics.GenericAPIView):
    def get(self, request):
        user = get_logged_in_user(request)

        try:
            user_token = Token.objects.get(user=user)
            user_token_histories = TokenHistory.objects.filter(token=user_token)
        except Token.DoesNotExist:
            user_token_histories = []

        token_history = []

        for history in user_token_histories:
            token_history.append({
                'balance_before': history.balance_before,
                'balance_after': history.balance_after,
                'comment': history.comment,
                'updated_at': history.updated_at
            })
            

        return Response({"status": "success","data": token_history}, status=status.HTTP_200_OK)