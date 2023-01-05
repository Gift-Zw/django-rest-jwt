from rest_framework import serializers, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializerGoat(TokenObtainPairSerializer):
    def validate(self, attrs):
        print('in')
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user is not None:
            if user.is_active:
                data = super().validate(attrs)
                refresh = self.get_token(self.user)
                refresh['username'] = self.user.username
                refresh['role'] = self.user.role
                data["refresh"] = str(refresh)
                data["access"] = str(refresh.access_token)
                data["user_id"] = self.user.id
                data['username'] = self.user.username
                data["name"] = self.user.full_name
                return data
            else:
                raise serializers.ValidationError('Account is Blocked')
        else:
            raise serializers.ValidationError('Incorrect userid/email and password combination!')
