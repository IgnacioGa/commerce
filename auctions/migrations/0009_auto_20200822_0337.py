# Generated by Django 3.0.8 on 2020-08-22 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200822_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='item',
        ),
        migrations.AddField(
            model_name='watchlist',
            name='item',
            field=models.ManyToManyField(related_name='watched', to='auctions.Listing'),
        ),
    ]
