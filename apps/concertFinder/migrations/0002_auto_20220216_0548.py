# Generated by Django 3.0 on 2022-02-16 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concertFinder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concertinfo',
            name='year',
            field=models.IntegerField(default=2022),
        ),
    ]
