# Generated by Django 5.0.2 on 2024-02-26 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mag', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='numberView',
            field=models.IntegerField(null=True),
        ),
    ]
