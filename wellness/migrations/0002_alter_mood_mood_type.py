# Generated by Django 5.1.2 on 2024-12-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wellness', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mood',
            name='mood_type',
            field=models.CharField(max_length=100),
        ),
    ]
