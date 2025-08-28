from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

class UserUpdateAPIView(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

class UserDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

class UserChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            if not self.request.user.check_password(data['old_password']):
                return Response(
                    {
                        "success" : False,
                        "error_message" : "Old password is incorrect"
                    }, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                self.request.user.set_password(data['new_password'])
                self.request.user.save()
                return Response(
                    {
                        "success": True,
                        "message": "Password changed successfully",
                    }
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


