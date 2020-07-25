# Generated by Django 3.0.8 on 2020-07-22 05:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='items',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='items',
            field=models.ManyToManyField(to='auctions.Listing'),
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='user',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]