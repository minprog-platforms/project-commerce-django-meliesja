# Generated by Django 3.2.9 on 2021-12-05 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_comment_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='item',
            new_name='listing',
        ),
    ]
