from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from user.serializers import (
    RegistrationSerializer, 
    UserProfileSerializer, 
    EductaionSerializer, 
    ExperienceSerializer,
    TechStackSerializer,
    CertificationSerializer
)
from user.models import (
    UserProfile, 
    Education, 
    Experience, 
    TechStack, 
    Certification
)


User = get_user_model()


class UserRegistrationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = []
    serializer_class = RegistrationSerializer
    permission_classes = []

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        UserProfileSerializer = self.get_serializer_class()
        profile_serializer = UserProfileSerializer(data=request.data)
        profile_serializer.is_valid(raise_exception=True)
        return super().create(request, *args, **kwargs)


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     User Viewset for all user related operations
#     Args:
#         viewsets (_type_): _description_
#     """

#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserProfileViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        if self.request.user.is_manager:
            # TODO: once the client and projects is added, he should be able to see only his project resouces
            return UserProfile.objects.all()
        if self.request.user.is_resource:
            return UserProfile.objects.filter(user_id=self.request.user.id)
        return UserProfile.objects.all()


# class EducationViewSet(viewsets.ModelViewSet):
#     serializer_class = EductaionSerializer

#     def get_queryset(self):
#         user_id = self.request.GET.get("user", None)
#         if self.request.user.is_manager and user_id:
#             return Education.objects.filter(user_profile_id=user_id)    
#         if self.request.user.is_resource:
#             return Education.objects.filter(user_profile__user_id=self.request.user.id)
#         return Education.objects.all()
    
#     @transaction.atomic
#     def create(self, request, *args, **kwargs):
#         EductaionSerializer = self.get_serializer_class()
#         education_serializer = EductaionSerializer(data=request.data, many=True)
#         education_serializer.is_valid(raise_exception=True)
#         self.perform_create(education_serializer)
#         return Response(education_serializer.data, status=status.HTTP_201_CREATED)

class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EductaionSerializer

    def get_queryset(self):
        user_id = self.request.GET.get("user", None)
        if self.request.user.is_manager and user_id:
            return Education.objects.filter(user_profile_id=user_id)    
        if self.request.user.is_resource:
            return Education.objects.filter(user_profile__user_id=self.request.user.id)
        return Education.objects.all()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class ExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        user_id = self.request.GET.get("user", None)
        if self.request.user.is_manager and user_id:
            return Experience.objects.filter(user_profile_id=user_id)    
        if self.request.user.is_resource:
            return Experience.objects.filter(user_profile__user_id=self.request.user.id)
        return Experience.objects.all()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        ExperienceSerializer = self.get_serializer_class()
        experience_serializer = ExperienceSerializer(data=request.data, many=True)
        experience_serializer.is_valid(raise_exception=True)
        self.perform_create(experience_serializer)
        return Response(experience_serializer.data, status=status.HTTP_201_CREATED)


# class TechStackViewSet(viewsets.ModelViewSet):
#     serializer_class = TechStackSerializer

#     def get_queryset(self):
#         user_id = self.request.GET.get("user", None)
#         if self.request.user.is_manager and user_id:
#             return TechStack.objects.filter(user_profile_id=user_id)    
#         if self.request.user.is_resource:
#             return TechStack.objects.filter(user_profile__user_id=self.request.user.id)
#         return TechStack.objects.all()
    
#     @transaction.atomic
#     def create(self, request, *args, **kwargs):
#         TechStackSerializer = self.get_serializer_class()
#         techstack_serializer = TechStackSerializer(data=request.data, many=True)
#         techstack_serializer.is_valid(raise_exception=True)
#         self.perform_create(techstack_serializer)
#         return Response(techstack_serializer.data, status=status.HTTP_201_CREATED)

class TechStackViewSet(viewsets.ModelViewSet):
    serializer_class = TechStackSerializer
    queryset = TechStack.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            user_id = self.request.GET.get("user")
            if user_id:
                return TechStack.objects.filter(user_profile_id=user_id)
            else:
                return TechStack.objects.all()
        elif user.is_resource:
            return TechStack.objects.filter(user_profile__user=user)

        return TechStack.objects.none()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        TechStackSerializer = self.get_serializer(data=data, many=True)
        TechStackSerializer = self.get_serializer(data=data)
        TechStackSerializer.is_valid(raise_exception=True)
        self.perform_create(TechStackSerializer)
        return Response(TechStackSerializer.data, status=status.HTTP_201_CREATED)
    
    
class CertificationViewSet(viewsets.ModelViewSet):
    serializer_class = CertificationSerializer

    def get_queryset(self):
        user_id = self.request.GET.get("user", None)
        if self.request.user.is_manager and user_id:
            return Certification.objects.filter(user_profile_id=user_id)    
        if self.request.user.is_resource:
            return Certification.objects.filter(user_profile__user_id=self.request.user.id)
        return Certification.objects.all()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        CertificationSerializer = self.get_serializer_class()
        certification_serializer = CertificationSerializer(data=request.data, many=True)
        certification_serializer.is_valid(raise_exception=True)
        self.perform_create(certification_serializer)
        return Response(certification_serializer.data, status=status.HTTP_201_CREATED)