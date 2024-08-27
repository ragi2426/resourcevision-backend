from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from user.models import UserProfile, Experience, Education, Certification, TechStack, TimeZone, Documents
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile


User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=255, required=True)
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]
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


class TimezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeZone
        fields = '__all__'
         
    
class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'

    def validate(self, data):
        document_type = data.get('document_type')
        file = data.get('file')
        user_profile = data.get('user_profile')

        if not user_profile:
            raise serializers.ValidationError("User profile is required.")

        if document_type not in dict(Documents.DOCUMENT_TYPE_CHOICES).keys():
            raise serializers.ValidationError("Invalid document type") 

        allowed_extensions = []
        if document_type == Documents.RESUME:
            allowed_extensions = ['doc', 'docx', 'pdf']
        elif document_type == Documents.ONEPAGE_RESUME:
            allowed_extensions = ['ppt', 'pptx']
        # Note: `OTHERS` does not have file extension restrictions
         
        if file:
            file_extension = file.name.split('.')[-1].lower()
            if file_extension not in allowed_extensions:
                raise serializers.ValidationError(f"Invalid file format. Uplaod the file on this externsions{', '.join(allowed_extensions)}")

        existing_documents = Documents.objects.filter(user_profile=user_profile).values_list('document_type', flat=True)
        
        # Check if the document already exists
        if document_type in existing_documents:
            raise serializers.ValidationError(f"{dict(Documents.DOCUMENT_TYPE_CHOICES).get(document_type)} has already been uploaded.")
        
        mandatory_types = [Documents.RESUME, Documents.ONEPAGE_RESUME]
        missing_documents = [doc for doc in mandatory_types if doc not in existing_documents]
        if missing_documents:
            missing_docs_str = ', '.join([dict(Documents.DOCUMENT_TYPE_CHOICES).get(doc) for doc in missing_documents])
            raise serializers.ValidationError(f"upload the missing documents: {missing_docs_str}.")

        return data