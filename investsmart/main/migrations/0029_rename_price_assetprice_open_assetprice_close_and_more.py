# Generated by Django 4.1.2 on 2022-12-19 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0028_rename_mentioned_asset_news_mentioned_assets"),
    ]

    operations = [
        migrations.RenameField(
            model_name="assetprice", old_name="price", new_name="open",
        ),
        migrations.AddField(
            model_name="assetprice", name="close", field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="assetprice", name="high", field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="assetprice", name="low", field=models.FloatField(default=0),
        ),
    ]