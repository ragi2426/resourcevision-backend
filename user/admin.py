from django.contrib import admin
from user.models import User, UserProfile, Education, Experience, TechStack, Certification

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(TechStack)
admin.site.register(Certification)