# Generated by Django 3.1.7 on 2022-03-30 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0002_auto_20220330_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.IntegerField(choices=[('male', 'male'), ('female', 'female'), (2, 'not specified')]),
        ),
    ]