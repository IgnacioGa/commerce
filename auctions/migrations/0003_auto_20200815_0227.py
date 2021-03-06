# Generated by Django 3.0.8 on 2020-08-15 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_category_comments_listing_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='estate',
            new_name='active',
        ),
        migrations.AlterField(
            model_name='listing',
            name='actualBid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8),
        ),
    ]
