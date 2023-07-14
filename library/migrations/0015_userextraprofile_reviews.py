# Generated by Django 4.2.2 on 2023-07-13 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_remove_userextraprofile_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextraprofile',
            name='reviews',
            field=models.ManyToManyField(related_name='my_reviews', through='library.Review', to='library.userextraprofile'),
        ),
    ]