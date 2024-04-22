# Generated by Django 5.0.2 on 2024-04-15 02:52

import django.db.models.deletion
import mag.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mag', '0016_alter_author_unique_together_author_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='author',
            name='phone',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='news',
            name='Author',
            field=models.ForeignKey(blank=True, default=mag.models.get_default_author_id, null=True, on_delete=django.db.models.deletion.CASCADE, to='mag.author'),
        ),
    ]