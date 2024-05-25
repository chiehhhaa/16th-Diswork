# Generated by Django 5.0.6 on 2024-05-22 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
        ('members', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='like_sender',
            field=models.ManyToManyField(related_name='like_sender', through='comments.LikeComment', to='comments.comment'),
        ),
    ]