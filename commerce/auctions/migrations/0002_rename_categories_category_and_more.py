# Generated by Django 4.1 on 2022-09-03 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categories',
            new_name='Category',
        ),
        migrations.AlterField(
            model_name='auction_listing',
            name='categories',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
