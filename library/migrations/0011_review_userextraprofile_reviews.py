# Generated by Django 4.2.2 on 2023-07-13 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_userextraprofile_friends_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_positive', models.BooleanField()),
                ('review_content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.game')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.userextraprofile')),
            ],
        ),
        migrations.AddField(
            model_name='userextraprofile',
            name='reviews',
            field=models.ManyToManyField(blank=True, related_name='reviews', to='library.review'),
        ),
    ]
