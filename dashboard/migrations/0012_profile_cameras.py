# Generated by Django 4.0.3 on 2022-04-02 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_remove_profile_cameras_alter_camera_direction'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cameras',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.camera'),
        ),
    ]
