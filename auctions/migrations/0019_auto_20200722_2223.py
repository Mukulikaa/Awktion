# Generated by Django 3.0.8 on 2020-07-22 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20200722_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='details',
            field=models.CharField(max_length=1500),
        ),
    ]