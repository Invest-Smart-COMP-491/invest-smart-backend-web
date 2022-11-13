# Generated by Django 4.1.2 on 2022-11-13 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_alter_asset_market_size"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="asset_name",
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name="asset",
            name="photo_link",
            field=models.URLField(blank=True, null=True),
        ),
    ]
