from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from user.models import UserProfile, Experience, Education, Certification, TechStack

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    
class RegistrationSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer()
    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):
        # save user details first before user profile
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        validated_data["user_id"] = user.id
        # attached Resource group to the user
        user.groups.add(Group.objects.get(name="Resource"))
        return super(RegistrationSerializer, self).create(validated_data)

        
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class EductaionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = '__all__'


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'
