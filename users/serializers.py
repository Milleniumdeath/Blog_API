from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'password',   # ✅ qo‘shildi
        )
        required_fields = ['first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password')  # parolni alohida ajratamiz
        user = User.objects.create_user(**validated_data)  # create_user parolsiz ishlaydi
        user.set_password(password)  # ✅ parolni hashlash
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=3, max_length=32)

