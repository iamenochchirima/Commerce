# Generated by Django 4.1 on 2022-09-03 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_rename_categories_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction_listing',
            name='categories',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
