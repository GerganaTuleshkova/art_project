# Generated by Django 4.0.3 on 2022-04-04 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('art_portal_app', '0002_style_technique_painting_photo_painting_style_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='technique',
            old_name='style_name',
            new_name='technique_name',
        ),
    ]
