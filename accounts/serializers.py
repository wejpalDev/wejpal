from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from .models import User

class UpdateUserAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    def validate(self, data):
        date_of_birth = data.get('date_of_birth')
        return data