# Generated by Django 3.1.1 on 2020-10-21 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authAPI', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile',
            new_name='image',
        ),
    ]
