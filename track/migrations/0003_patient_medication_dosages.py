# Generated by Django 3.1.7 on 2022-05-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0002_remove_medication_patient'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='medication_dosages',
            field=models.ManyToManyField(to='track.Medication'),
        ),
    ]
