from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet)
router.register(r'language', languageViewSet)
router.register(r'content', contentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginView.as_view(), name="user_login"),   
    path('get_content_by_language/',get_content_by_language.as_view())
    ]