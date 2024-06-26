# Generated by Django 5.0.2 on 2024-04-14 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mag', '0015_alter_news_author'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='author',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='author',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$720000$BSG2SbE3SiEhAsPAiDD1mx$Ztyo0apGMzoZpUMui7cAekKJvNsyGNhvQgbJE0mI3CM=', max_length=255),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='author',
            unique_together={('email', 'name')},
        ),
    ]
