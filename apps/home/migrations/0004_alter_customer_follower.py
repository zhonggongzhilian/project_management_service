# Generated by Django 3.2.6 on 2024-10-10 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_customer_follower'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='follower',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.userprofile'),
        ),
    ]
