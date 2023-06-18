from typing import Dict, Tuple
from rest_framework import serializers
from core.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated
from django.contrib.auth import authenticate


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields: Tuple[str, ...] = ("id", "username", "first_name", "last_name", "email", "password", "password_repeat",)

    def validate(self, validated_data: Dict) -> Dict:
        if validated_data.get("password") != validated_data.pop("password_repeat"):
            raise ValidationError("Password and password_repeat don't match!")
        return validated_data

    def create(self, validated_data: Dict) -> User:
        if User.objects.filter(username=validated_data["username"]).exists():
            raise ValidationError("A user with this name already exists!")
        else:
            # del validated_data["password_repeat"]
            validated_data["password"] = make_password(validated_data["password"])
            user = User.objects.create(**validated_data)
            user.save()
            return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields: Tuple[str, ...] = ("id", "username", "first_name", "last_name", "email", "password",)

    def create(self, validated_data: Dict) -> User:
        user = authenticate(username=validated_data["username"], password=validated_data["password"])
        if not user:
            raise AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields: Tuple[str, ...] = ("id", "username", "first_name", "last_name", "email",)


class PasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields: Tuple[str, ...] = ("old_password", "new_password",)

    def validate(self, validated_data: dict) -> Dict:
        if not (user := validated_data['user']):
            raise NotAuthenticated
        if not user.check_password(validated_data['old_password']):
            raise ValidationError({'old_password': 'field is incorrect'})
        return validated_data

    def update(self, instance: User, validated_data: Dict) -> User:
        instance.password = make_password(validated_data['new_password'])
        instance.save()
        return instance
