# Generated by Django 3.2.9 on 2021-12-05 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_item_watchlist_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]