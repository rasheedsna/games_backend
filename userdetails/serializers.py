from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserDetails, content, language
import json
from django.conf import settings


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
        response_data['username'] = instance.username
        response_data['first_name'] = instance.first_name
        response_data['last_name'] = instance.last_name
        response_data['email'] = instance.email
        try:
            user_details = UserDetails.objects.get(id=instance.id)
            response_data['phone_number'] = user_details.phone_number
        except:
            pass 
        return response_data

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id','first_name', 'last_name', 'email', 'username', 'password', 'phone_number']
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}, 
            'password': {'write_only': True,'required':False},
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
    language_name = serializers.CharField(source='language.name', read_only=True)
    native_name = serializers.CharField(source='language.native_name', read_only=True)
    video_name = serializers.CharField(source='language.video_name', read_only=True)
    audio_name = serializers.CharField(source='language.audio_name', read_only=True)
    text_name = serializers.CharField(source='language.text_name', read_only=True)
   


    class Meta:
        model = content
        fields = ['id','language','language_name','text_content','title','video_link','short_video_link','html_content','more_info','meeting_link','native_name','video_name','audio_name','text_name']
        extra_kwargs = {'id': {"read_only": True},'speciality':{"required":False}}

        def create(self, validated_data):
            content = content.objects.create_user(**validated_data)
            return content

    def to_representation(self, instance):
            rep = super().to_representation(instance)
        
            appts = content.objects.filter(id=rep['id']).values('id','language','language__name','video','audio','text_content','title',
                                                                    'speciality','video_link','short_video','short_video_link','html_content','more_info',
                                                                    'meeting_link','language__native_name','language__video_name','language__audio_name',
                                                                    'language__text_name','language__home_name','language__meeting_name','language__reviews_name','short_video_thumbnail_desktop','short_video_thumbnail_mobile','video_thumbnail_mobile','video_thumbnail_desktop').first()
            
            
                
            rep['video']=settings.HOST_ADDRESS+settings.MEDIA_URL+appts['video'] if appts['video'] else ''
            rep['audio']=settings.HOST_ADDRESS+settings.MEDIA_URL+appts['audio'] if appts['audio'] else ''
            rep['short_video'] = settings.HOST_ADDRESS+settings.MEDIA_URL+appts['short_video'] if appts['short_video'] else ''
            rep['short_video_thumbnail_desktop'] = settings.HOST_ADDRESS+settings.MEDIA_URL+appts['short_video_thumbnail_desktop'] if appts['short_video_thumbnail_desktop'] else ''
            rep['short_video_thumbnail_mobile'] = settings.HOST_ADDRESS+settings.MEDIA_URL+appts['short_video_thumbnail_mobile'] if appts['short_video_thumbnail_mobile'] else ''
            rep['video_thumbnail_mobile'] = settings.HOST_ADDRESS+settings.MEDIA_URL+appts['video_thumbnail_mobile'] if rep['video_thumbnail_mobile'] else ''
            rep['video_thumbnail_desktop'] = settings.HOST_ADDRESS.HOST_ADDRESS+settings.MEDIA_URL+appts['video_thumbnail_desktop'] if appts['video_thumbnail_desktop'] else ''
        
            
            return rep