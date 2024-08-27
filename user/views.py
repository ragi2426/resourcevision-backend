from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, mixins, parsers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.serializers import (
    RegistrationSerializer, 
    UserProfileSerializer, 
    EductaionSerializer, 
    ExperienceSerializer,
    TechStackSerializer,
    CertificationSerializer,
    TimezoneSerializer,
    DocumentsSerializer,
)
from user.models import (
    UserProfile, 
    Education, 
    Experience, 
    TechStack, 
    Certification,
    TimeZone,
    Documents,
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

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    http_method_names = ['get', 'patch']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_manager:
            # TODO: once the client and projects is added, he should be able to see only his project resouces
            return UserProfile.objects.all()
        if self.request.user.is_resource:
            return UserProfile.objects.filter(user_id=self.request.user.id)
        return UserProfile.objects.all()

    def update(self, request, *args, **kwargs):
        if 'user' in request.data:
            return Response({"Error": "Changing User is not allowed"}, status=status.HTTP_400_BAD_REQUEST) 
        return super(UserProfileViewSet, self).update(request, *args, **kwargs)


class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EductaionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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


class TechStackViewSet(viewsets.ModelViewSet):
    serializer_class = TechStackSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_manager:
            user_id = self.request.GET.get("user")
            if user_id:
                return TechStack.objects.filter(user_profile_id=user_id)
        elif user.is_resource:
            return TechStack.objects.filter(user_profile__user=user)
        return TechStack.objects.all()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data
        TechStackSerializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        TechStackSerializer.is_valid(raise_exception=True)
        self.perform_create(TechStackSerializer)
        return Response(TechStackSerializer.data, status=status.HTTP_201_CREATED)

class CertificationViewSet(viewsets.ModelViewSet):
    serializer_class = CertificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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

# class TimezoneViewSet(viewsets.ModelViewSet):
#     """Timezone viewset which returns the timezone list.
#     It also support search by providing search=string in request 
#     query paramerter

#     Returns:
#         List: timezones
#     """
#     serializer_class = TimezoneSerializer
#     permission_classes = []
#     http_method_names = ['get']

#     def get_queryset(self):
#         search = self.request.GET.get("search", None)
#         if search:
#             return Timezone.objects.filter(name__contains=search)
#         return Timezone.objects.all()
    
class TimezoneViewSet(viewsets.ModelViewSet):
    """Timezone viewset which returns the timezone list.
    It also supports search by providing search=string in the request 
    query parameter.

    Returns:
        List: timezones
    """
    serializer_class = TimezoneSerializer
    permission_classes = [AllowAny]  # Or use another permission class if needed
    http_method_names = ['get']

    def get_queryset(self):
        search = self.request.GET.get("search", None)
        if search:
            return TimeZone.objects.filter(label__icontains=search)
        return TimeZone.objects.all()


   
class DocumentsViewSet(viewsets.ModelViewSet):
    queryset = Documents.objects.all()
    serializer_class = DocumentsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        DocumentsSerializer = self.get_serializer(data=request.data)
        DocumentsSerializer.is_valid(raise_exception=True)
        self.perform_create(DocumentsSerializer)
        return Response(DocumentsSerializer.data, status=status.HTTP_201_CREATED)
