# Generated by Django 3.2.6 on 2024-10-08 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20241008_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='follower',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
