from django.urls import path
from .views import *

urlpatterns = [
    path('info/', GetUserToken.as_view(), name='token-info'),
    path('history/', GetUserTokenHistory.as_view(), name='token-history'),
]