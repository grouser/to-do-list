# Generated by Django 2.1 on 2018-08-19 17:31

from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_default_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    user = User.objects.create(
        username='novastone',
        first_name='Novastone',
        last_name='Media',
        password=make_password('test')
    )
    user.save()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_default_user)
    ]
