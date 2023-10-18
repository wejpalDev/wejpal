from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UpdateUserAccountSerializer
from .utils import get_logged_in_user
from .models import UserDetail
from authentications.models import User

# Create your views here.
class GetUserProfile(generics.GenericAPIView):
    def get(self, request):
        user = get_logged_in_user(request)
        try:
            details = UserDetail.objects.get(user=user)
        except UserDetail.DoesNotExist:
            details = ''

        content =  {
            'user_id': user.id, 
            'email':user.email,
            'is_active': user.is_active,
            'first_name': details.first_name if details != '' else '',
            'last_name': details.last_name if details != '' else '',
            'date_of_birth': details.date_of_birth if details != '' else '',
            'phone_number': details.phone_number if details != '' else ''
            }

        return Response({"status": "success","data": content}, status=status.HTTP_200_OK)


class CreateUserAccount(APIView):
    def post(self, request):
        serializer = UpdateUserAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = get_logged_in_user(request)

            email = serializer.data["email"]
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            date_of_birth = serializer.data["date_of_birth"]
            phone_number = serializer.data["phone_number"]

            try:
                details = UserDetail.objects.create(user=user,first_name=first_name,last_name=last_name,date_of_birth=date_of_birth,phone_number=phone_number)
            except:
                return Response({"status": "failed","data": "Could not create profile."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": "success","data": "User Profile Updated."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserAccount(APIView):
    def put(self, request):
        serializer = UpdateUserAccountSerializer(data=request.data)
        if serializer.is_valid():
            user = get_logged_in_user(request)

            email = serializer.data["email"]
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            date_of_birth = serializer.data["date_of_birth"]
            phone_number = serializer.data["phone_number"]

            if email != user.email:
                try:
                    allowedEmail = User.objects.get(email=email)
                except UserDetail.DoesNotExist:
                    allowedEmail = False
                
                if allowedEmail == False:
                    user.email = email
                    user.save()

            try:
                details = UserDetail.objects.get(user=user)
                details.first_name = first_name
                details.last_name = last_name
                details.date_of_birth = date_of_birth
                details.phone_number = phone_number
                details.save()
            except UserDetail.DoesNotExist:
                return Response({"status": "failed","data": "Could not update profile."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": "success","data": "User Profile Updated."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)