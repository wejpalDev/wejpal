from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from .models import User

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'provider', 'sub')

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'provider', 'sub')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            provider=validated_data.get('provider', 'wejpal-user'),
            sub=validated_data.get('sub', None)
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class GetGoogleAuthSerializer(serializers.Serializer):
    secret = serializers.CharField(write_only=True, required=True)

class RegisterUserThroughSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'provider', 'sub')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=get_random_string(length=32),
            provider=validated_data.get('provider', 'wejpal-user'),
            sub=validated_data.get('sub', None)
        )
        return user


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data




class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data



class RegisterUserWithOtp(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'provider', 'sub', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=get_random_string(length=32),
            provider=validated_data.get('provider', 'wejpal-user'),
            sub=get_random_string(length=4, allowed_chars='0123456789'),
        )
        return user
    
class RegisterUserOTPValid(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=True)
    otp = serializers.CharField(write_only=True, required=True)

class SetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data