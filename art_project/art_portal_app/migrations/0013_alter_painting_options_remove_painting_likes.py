# Generated by Django 4.0.3 on 2022-04-06 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('art_portal_app', '0012_alter_painting_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='painting',
            options={'ordering': ['title']},
        ),
        migrations.RemoveField(
            model_name='painting',
            name='likes',
        ),
    ]
