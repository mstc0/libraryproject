# Generated by Django 4.2.2 on 2023-07-13 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_userextraprofile_reviews_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userextraprofile',
            name='reviews',
        ),
    ]
