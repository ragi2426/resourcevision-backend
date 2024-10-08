# Generated by Django 4.2.13 on 2024-07-01 10:49

from django.db import migrations


def forwards(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.bulk_create([
        Group(name=u'Resource'),
        Group(name=u'Manager'),
        Group(name=u'Admin'),
    ])

def backwords(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(
        name__in=[
            'Resource',
            'Manager',
            'Admin',
        ]
    ).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_load_timezones'),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=backwords)
    ]
