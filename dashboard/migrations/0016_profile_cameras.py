# Generated by Django 4.0.3 on 2022-04-02 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_remove_profile_device_id_camera_device_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cameras',
            field=models.CharField(default=None, max_length=600, null=True),
        ),
    ]
