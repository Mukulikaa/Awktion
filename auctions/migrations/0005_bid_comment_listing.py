# Generated by Django 3.0.8 on 2020-07-18 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200718_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minbid', models.IntegerField()),
                ('curbid', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('details', models.CharField(max_length=240)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myitems', to=settings.AUTH_USER_MODEL)),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auctions.Bid')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=240)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.Listing')),
            ],
        ),
    ]