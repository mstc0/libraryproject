# Generated by Django 4.2.2 on 2023-07-13 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0017_alter_userownedgames_game_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userwishlist',
            unique_together={('user', 'game')},
        ),
    ]