from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', GetUserProfile.as_view(), name='account-profile'),
    path('profile/update/', UpdateUserAccount.as_view(), name='account-profile-update'),
]