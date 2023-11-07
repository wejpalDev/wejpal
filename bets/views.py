from django.shortcuts import render
from accounts.utils import get_logged_in_user
from rest_framework import generics
from rest_framework import status
from .models import Bet, BetUser
from rest_framework.response import Response
from .serializers import BetSerializer, UpdateBetChoiceSerializer, PlaceUserBetSerializer, WithdrawUserPlacedBetSerializer
from .utils import format_bet
from datetime import datetime

# Get All Available Bets
class GetAvailableBet(generics.GenericAPIView):
    def get(self, request):
        bets = Bet.objects.filter(start_at__lt=datetime.now(), end_at__gt=datetime.now())
        available_bets = []

        try:
            user = get_logged_in_user(request)
        except:
            user = None

        for bet in bets:
            available_bets.append(format_bet(bet, user))

        return Response({"status": "success","data": available_bets}, status=status.HTTP_200_OK)

# Create Bet
class CreateUserBet(generics.GenericAPIView):
    serializer_class = BetSerializer

    def post(self, request):
        data = request.data
        user = get_logged_in_user(request)
        serializer = self.serializer_class(data=data, context={'user': user})
        if serializer.is_valid():
            bet = serializer.save()
            return Response({"status": "success","data": format_bet(bet)}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get Bets Created by user
class GetUserCreatedBet(generics.GenericAPIView):
    def get(self, request):
        user = get_logged_in_user(request)
        bets = Bet.objects.filter(user=user, start_at__gt=datetime.now(), end_at__gt=datetime.now())
        available_bets = []
        for bet in bets:
            available_bets.append(format_bet(bet))

        return Response({"status": "success","data": available_bets}, status=status.HTTP_200_OK)

# Update Bet: Change selected winner
class UpdateUserBetChoice(generics.GenericAPIView):
    serializer_class = UpdateBetChoiceSerializer

    def put(self, request):
        data = request.data
        user = get_logged_in_user(request)
        serializer = self.serializer_class(data=data, context={'user': user})
        if serializer.is_valid():
            bet = serializer.save()
            return Response({"status": "success","data": format_bet(bet)}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Place Bet: Change selected winner
class placeUserBet(generics.GenericAPIView):
    serializer_class = PlaceUserBetSerializer

    def post(self, request):
        data = request.data
        user = get_logged_in_user(request)
        serializer = self.serializer_class(data=data, context={'user': user})
        if serializer.is_valid():
            bet = serializer.save()
            return Response({"status": "success","data": format_bet(bet)}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get Bets Placed by user
class GetUserPlacedBet(generics.GenericAPIView):
    def get(self, request):
        user = get_logged_in_user(request)
        bet_users = BetUser.objects.filter(user=user)
        available_bets = []
        for bet_user in bet_users:
            available_bets.append(
                {
                    "id": bet_user.id,
                    "amount": bet_user.token_on_bet,
                    "choice": bet_user.bet_option.name,
                    "choice_id": bet_user.bet_option.id,
                    "bet": format_bet(bet_user.bet)
                })

        return Response({"status": "success","data": available_bets}, status=status.HTTP_200_OK)

# Withdraw Bet Placed by user
class WithdrawUserPlacedBet(generics.GenericAPIView):
    serializer_class = WithdrawUserPlacedBetSerializer

    def delete(self, request):
        data = request.data
        user = get_logged_in_user(request)
        serializer = self.serializer_class(data=data, context={'user': user})

        if serializer.is_valid():
            bet = serializer.save()
            return Response({"status": "success","data": "Bet has been withdrawn"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)