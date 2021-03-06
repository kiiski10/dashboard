# Generated by Django 4.0.3 on 2022-04-02 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_rename_marker_type_location_location_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_type',
            field=models.CharField(choices=[('WAYPOINT', 'Waypoint'), ('SIGHTS', 'Sight seeing'), ('CAMP', 'Camp site'), ('HOME', 'Home')], default='WAYPOINT', max_length=200),
        ),
    ]
