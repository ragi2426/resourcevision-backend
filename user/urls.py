"""
URL configuration for ResourceVision project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import (
    UserRegistrationViewSet, 
    UserProfileViewSet,
    EducationViewSet,
    ExperienceViewSet,
    TechStackViewSet,
    CertificationViewSet
)
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='register')
# router.register(r'user', UserViewSet, basename='user')
router.register(r'profile', UserProfileViewSet, basename='user-profile')
router.register(r'education', EducationViewSet, basename='user-education')
router.register(r'experience', ExperienceViewSet, basename='user-experience')
router.register(r'techstack', TechStackViewSet, basename='user-techstack')
router.register(r'certification', CertificationViewSet, basename='user-certification')

urlpatterns = router.urls
