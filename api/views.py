from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from django.contrib.auth import authenticate


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user is not None:
            if user.is_active:
                data = super().validate(attrs)
                refresh = self.get_token(self.user)
                refresh['username'] = self.user.username
                data["refresh"] = str(refresh)
                data["access"] = str(refresh.access_token)
                user = {
                    "user_id": self.user.id,
                    "username": self.user.username,
                    "email": self.user.email,
                    "name": self.user.full_name,
                    "role": self.user.role

                }

                data["user"] = user
                return data
            else:
                raise serializers.ValidationError('Account is not active')
        else:
            raise serializers.ValidationError('Incorrect username and password combination!')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



