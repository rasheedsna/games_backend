from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserDetails, content, language



class UserLoginSerializer(serializers.Serializer):
    """
    Serializer class for validating the user from the user email and password. Also will send the otp
    """
    username = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get("username", None), password=data.get("password", None))
        if user is None:
            raise serializers.ValidationError(
                'User login failed'
            )
        # {"username":"admin","password":"testpass"}
        return user
        
    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        refresh = RefreshToken.for_user(instance)
        response_data['access_token'] = str(refresh.access_token)
        response_data['refresh_token'] = str(refresh)
        response_data['id'] = instance.id
        return response_data

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'phone_number']
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}, 
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = UserDetails.objects.create_user(**validated_data)
        return user

class LanguageSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = language
        fields = '__all__'
        extra_kwargs = {'id': {"read_only": True}}

class ContentSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = content
        fields = '__all__'
        extra_kwargs = {'id': {"read_only": True}}

        def create(self, validated_data):
            content = content.objects.create_user(**validated_data)
            return content