# Generated by Django 4.2.13 on 2024-07-24 10:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_techstack_proficiency_level'),
    ]

    operations = [
        migrations.RenameField(
            model_name='certification',
            old_name='date',
            new_name='issued_date',
        ),
        migrations.RenameField(
            model_name='experience',
            old_name='skills',
            new_name='roles_responsibilities',
        ),
        migrations.RemoveField(
            model_name='techstack',
            name='proficiency_level',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='age',
        ),
        migrations.AddField(
            model_name='certification',
            name='certification_id',
            field=models.CharField(default=0, max_length=50, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9]*$', 'Only alphanumeric characters are allowed.')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='techstack',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='education',
            name='grade',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
