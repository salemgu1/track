# Generated by Django 3.1.7 on 2022-03-30 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0003_auto_20220330_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.IntegerField(choices=[(0, 'male'), (1, 'female'), (2, 'not specified')]),
        ),
    ]
