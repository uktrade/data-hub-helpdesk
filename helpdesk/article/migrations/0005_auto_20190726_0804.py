# Generated by Django 2.2.3 on 2019-07-26 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20190718_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleindexpage',
            name='intro',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
