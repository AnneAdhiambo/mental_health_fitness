# Generated by Django 5.0.7 on 2024-12-04 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wellness', '0002_alter_mood_mood_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=10)),
                ('content', models.TextField()),
            ],
        ),
    ]
