# Generated by Django 4.1.2 on 2022-12-10 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='public_name',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
