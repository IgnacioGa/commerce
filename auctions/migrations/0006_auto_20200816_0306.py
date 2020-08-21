# Generated by Django 3.0.8 on 2020-08-16 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20200816_0250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='characteristic',
            name='listing',
        ),
        migrations.AddField(
            model_name='listing',
            name='caract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='details', to='auctions.Characteristic'),
        ),
    ]
