from sys import settrace
from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, pagination
from .serializers import *
from .models import User, language

# Create your views here.

class UserLoginView(APIView):
    """
    Class for user login(active users)
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    # def get(self, request, *args, **kwargs):
    #     social_login_dict = {}
    #     social_login_dict['apple'] = {}
    #     social_login_dict['apple']['url'] = f''
    #     social_login_dict['facebook'] = {}
    #     social_login_dict['facebook']['url'] = f''
    #     social_login_dict['google'] = {}
    #     google_obj = SocialApp.objects.filter(provider='google').last()
    #     import pdb;pdb.set_trace()
    #     # https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=<https_callback>&prompt=consent&response_type=code&client_id=<cliend_id>&scope=email&access_type=offline
    #     social_login_dict['google']['url'] = f'https://accounts.google.com/o/oauth2/v2/auth?redirect_uri={request.scheme}://{request.get_host()}/accounts/google/login/callback/&prompt=consent&response_type=code&client_id={google_obj.client_id}&scope=email&access_type=offline'
    #     return Response({'message': 'User Login Details', 'data':social_login_dict}, status=status.HTTP_200_OK)
        
    @swagger_auto_schema(
        operation_description="Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="title: Username/Email/Phone number"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="title:Password",
                ),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "access_token": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Access token",
                            ),
                            "refresh_token": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Refresh token",
                            ),
                        },
                    ),
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Login Successfull",
                    ),
                },
            ),
            status.HTTP_404_NOT_FOUND: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(
                        type=openapi.TYPE_STRING, description="Page not found."
                    )
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'User Login Successfully', 'data':serializer.data}, status=status.HTTP_200_OK)

class UserRegistrationViewSet(viewsets.ModelViewSet):
    """
    A viewset for register and edit user instances.
    """
    serializer_class = RegistrationSerializer
    queryset = UserDetails.objects.all()
    http_method_names = ['get', 'put','post','delete']        

class languageViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    serializer_class = LanguageSerializer
    queryset = language.objects.all()
    http_method_names = ['get', 'put','post','delete'] 

class contentViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    serializer_class = ContentSerializer
    queryset = content.objects.all()
    http_method_names = ['get', 'put','post','delete'] 

class get_content_by_language(APIView): 
    queryset = content.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ContentSerializer
    @swagger_auto_schema(
        operation_description="Language",
        manual_parameters=[openapi.Parameter(
            'language_id', 
            openapi.IN_QUERY, 
            type=openapi.TYPE_STRING
            )],
    )
    def get(self,request):

        try:
            hostname = f"{ request.scheme }://{ request.get_host() }"
            lang_id = request.GET.get('language_id') 
            appts = content.objects.filter(language_id=lang_id).values()
            for item in appts:
                
                item['video']=hostname+settings.MEDIA_URL+item['video']
                item['audio']=hostname+settings.MEDIA_URL+item['audio']
               
            return Response({'results':appts})
        except Exception as e:
            return Response({'results':"Failed to get content"})