from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout, get_user_model
from .serializers import RegisterUserWithOtp, SetPasswordSerializer, RegisterUserOTPValid, UserRegisterSerializer, RegisterUserThroughSocialSerializer, GetGoogleAuthSerializer, UserLoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, PasswordResetSerializer
from .utils import send_activation_email, TokenGenerator, send_otp_email
from django.utils.encoding import force_bytes
from .models import User
from accounts.models import UserDetail
from tokens.utils import create_user_balance
from django.contrib.auth.hashers import make_password, check_password

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_verified = False
            user.save()
            # send_activation_email(user, request)
            token = create_user_balance(user) # create wallet with default 1000 tokens
            return Response({"msg": "Registration successful. Please check your email for verification instructions."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            if user.check_password(serializer.validated_data['password']):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)





class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            email = serializer.data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            # Generate a password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Send an email with the reset link (use your email sending logic)
            send_activation_email(user, request)

            return Response({"msg": "Password reset email has been sent"}, status=status.HTTP_200_OK)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class VerifyEmailView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and TokenGenerator().check_token(user, token)(user, token):
            user.is_verified = True
            user.save()
            return Response({"msg": "Email verification successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)




class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            email = serializer.data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)


            send_activation_email(user, request)

            return Response({"msg": "Password reset email has been sent"}, status=status.HTTP_200_OK)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# views.py

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and TokenGenerator().check_token(user, token):
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                new_password = serializer.data["new_password"]
                user.set_password(new_password)
                user.save()
                return Response({"msg": "Password reset successful."}, status=status.HTTP_200_OK)
            else:

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid password reset link."}, status=status.HTTP_400_BAD_REQUEST)


class GetGoogleAuthCredentials(APIView):
    def post(self, request):
        data = request.data
        serializer = GetGoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            secret = serializer.validated_data['secret']

            if secret == 'dddds':
                return Response({
                    'client_id': 'google-client-id',
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'key is invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserThroughGoogleView(APIView):
    def post(self, request):
        serializer = RegisterUserThroughSocialSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_verified = True
            user.save()
            token = create_user_balance(user) # create wallet with default 1000 tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterUserFirstStage(APIView):
    def post(self, request):
        serializer = RegisterUserWithOtp(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_verified = True
            user.save()
            token = create_user_balance(user) # create wallet with default 1000 tokens
            details = UserDetail.objects.create(user=user,first_name=request.data['first_name'],last_name=request.data['last_name'])
            
            send_otp_email(user, request)
            return Response({
                'detail': 'otp has been sent to the registered email address'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterUserVerifyOTP(APIView):
    def post(self, request):
        serializer = RegisterUserOTPValid(data=request.data)
        if serializer.is_valid():
            
            try:
                user = User.objects.get(email=serializer.validated_data['email'])
            except User.DoesNotExist:
                return Response({'detail': 'provided email does not exist'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if (user.sub != serializer.validated_data['otp']):
                return Response({'detail': 'provided otp is incorrect'}, status=status.HTTP_401_UNAUTHORIZED)
            
            user.is_verified = True
            user.save()

            return Response({
                'detail': 'otp is verified'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterUserSetPassword(APIView):
    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.password = make_password(serializer.validated_data['password'])
            user.save()

            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)