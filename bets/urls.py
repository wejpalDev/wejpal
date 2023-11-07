from django.urls import path
from .views import *

urlpatterns = [
    path('', GetAvailableBet.as_view(), name='all-bets'),
    path('create', CreateUserBet.as_view(), name='create-bet'),
    path('user/records', GetUserCreatedBet.as_view(), name='user-created-bets'),
    path('user/update/choice', UpdateUserBetChoice.as_view(), name='update-user-bet-choice'),
    path('user/create/wedger', placeUserBet.as_view(), name='create-user-bet-wedger'),
    path('user/placed/wedger', GetUserPlacedBet.as_view(), name='user-placed-bet-wedger'),
    path('user/withdraw/wedger', WithdrawUserPlacedBet.as_view(), name='user-placed-bet-wedger'),
]