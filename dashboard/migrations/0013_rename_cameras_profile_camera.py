# Generated by Django 4.0.3 on 2022-04-02 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_profile_cameras'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='cameras',
            new_name='camera',
        ),
    ]
