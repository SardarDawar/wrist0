# Generated by Django 2.2 on 2019-10-01 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_auto_20191001_0545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='wrist_band_id',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='wrist_band',
        ),
    ]
