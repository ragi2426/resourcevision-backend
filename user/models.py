from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from enum import Enum
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator,FileExtensionValidator

# Create your models here.

class User(AbstractUser):
    pass

    @property
    def is_resource(self):
        if 'Resource' in self.groups.values_list('name', flat=True):
            return True
        return False

    @property
    def is_manager(self):
        if 'Manager' in self.groups.values_list('name', flat=True):
            return True
        return False
    
    @property
    def is_admin(self):
        if 'Admin' in self.groups.values_list('name', flat=True):
            return True
        return False


class TimeZone(models.Model):
    value = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secondary_email = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    sex = models.CharField(max_length=10)
    base_location = models.CharField(max_length=100)
    office_location = models.CharField(max_length=100)
    timezone = models.ForeignKey(TimeZone, on_delete=models.CASCADE)


class Experience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    designation = models.CharField(max_length=50)
    roles_responsibilities = models.TextField()


class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    grade = models.CharField(max_length=10, blank=True, null=True)
    percentage = models.IntegerField()
    year = models.IntegerField()

class TechStack(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
    last_used = models.IntegerField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class Certification(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    provider = models.CharField(max_length=100)
    certification_id = models.CharField(max_length=50, validators=[RegexValidator(r'^[a-zA-Z0-9]*$', 'Only alphanumeric characters are allowed.')])
    name = models.CharField(max_length=100)
    issued_date = models.DateField()
    expiry_date = models.DateField()   
        
           
class Documents(models.Model):
    RESUME = 'resume'
    ONEPAGE_RESUME = 'onepage_resume'
    OTHERS = 'others'
    DOCUMENT_TYPE_CHOICES = [
        (RESUME, 'Resume'),
        (ONEPAGE_RESUME, 'One Page Resume'),
        (OTHERS, 'Others'),
    ]
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    file = models.FileField(upload_to='documents/')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.document_type} - {self.user_profile.user.username}'s document"