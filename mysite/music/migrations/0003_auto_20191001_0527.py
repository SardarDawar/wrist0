# Generated by Django 2.2 on 2019-10-01 00:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0002_auto_20191001_0452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wrist_band',
            name='user',
        ),
        migrations.AddField(
            model_name='information',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]