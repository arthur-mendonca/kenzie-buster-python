from rest_framework import serializers
from users.models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=127)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, required=False)
    is_employee = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already taken.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        return self.create_user(validated_data, password)

    def create_user(self, validated_data, password):
        User = get_user_model()
        user = User.objects.create_user(**validated_data, password=password)
        user.is_employee = validated_data.get("is_employee", False)
        user.is_superuser = user.is_employee
        user.save()
        return user

    def update(self, instance: User, validated_data: dict):
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(write_only=True)
