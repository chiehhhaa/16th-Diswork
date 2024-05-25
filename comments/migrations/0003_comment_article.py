# Generated by Django 5.0.6 on 2024-05-25 04:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
        ('comments', '0002_rename_like_sender_likecomment_like_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='articles.article'),
        ),
    ]