# Generated by Django 4.0.3 on 2022-04-13 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['last_name']},
        ),
    ]
