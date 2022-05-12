# Generated by Django 3.2.2 on 2022-05-08 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0004_auto_20220507_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='ECG',
            field=models.IntegerField(default=70),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='replay',
            field=models.CharField(default='There is no response to this message', max_length=500),
        ),
    ]