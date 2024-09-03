from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

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


class Timezone(models.Model):
    name = models.CharField(max_length=100)


# class UserProfile(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     secondary_email = models.CharField(max_length=50, blank=True, null=True)
#     phone_number = models.CharField(max_length=15)
#     age = models.IntegerField()
#     sex = models.CharField(max_length=10)
#     base_location = models.CharField(max_length=100)
#     office_location = models.CharField(max_length=100)
#     timezone = models.ForeignKey(Timezone, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150, blank=True, verbose_name='first name') 
    last_name = models.CharField(max_length=150, blank=True, verbose_name='last name')
    secondary_email = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
#    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    base_location = models.CharField(max_length=100)
    office_location = models.CharField(max_length=100)
    timezone = models.ForeignKey('Timezone', on_delete=models.CASCADE)
    

class Experience(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    designation = models.CharField(max_length=50)
    skills = models.TextField()


class Education(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    percentage = models.IntegerField()
    year = models.IntegerField()


class TechStack(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=20)  # Dropdown: Basic/Intermediate/Advanced
    tools_used = models.CharField(max_length=255)
    experience_in_months = models.IntegerField()
    last_used = models.DateField()  
    # rating = models.IntegerField()


class Certification(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    provider = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    date = models.DateField()
    expiry_date = models.DateField()