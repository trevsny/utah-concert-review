# Generated by Django 2.1 on 2018-09-11 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concertFinder', '0002_auto_20180830_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='concertinfo',
            name='year',
            field=models.IntegerField(default=2018),
        ),
    ]