# Generated by Django 5.0.2 on 2024-04-14 00:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mag', '0012_remove_news_main_image_remove_news_thumbnail_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='likenews',
            old_name='user',
            new_name='utilisateur',
        ),
        migrations.RenameField(
            model_name='likepost',
            old_name='user',
            new_name='utilisateur',
        ),
        migrations.RenameField(
            model_name='newsseen',
            old_name='user',
            new_name='utilisateur',
        ),
        migrations.RenameField(
            model_name='postseen',
            old_name='user',
            new_name='utilisateur',
        ),
        migrations.AddField(
            model_name='news',
            name='Author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mag.author'),
        ),
        migrations.AlterField(
            model_name='news',
            name='body',
            field=models.TextField(max_length=2955),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(max_length=2995),
        ),
        migrations.AlterUniqueTogether(
            name='newsseen',
            unique_together={('utilisateur', 'news')},
        ),
        migrations.AlterUniqueTogether(
            name='postseen',
            unique_together={('utilisateur', 'post')},
        ),
    ]
