# Generated by Django 3.1.7 on 2022-05-05 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('by', models.CharField(max_length=40)),
                ('message', models.CharField(max_length=500)),
                ('senderType', models.CharField(default='user type', max_length=40)),
                ('replay', models.CharField(default='Replay', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('number', models.IntegerField(default=1)),
                ('max_Cholesterol', models.IntegerField(default=150)),
                ('max_Liver_function', models.IntegerField(default=55)),
                ('max_Kidney_function', models.IntegerField(default=60)),
                ('max_Blood_Pressure', models.IntegerField(default=80)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/Food/')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=40)),
                ('gender', models.IntegerField(choices=[(0, 'male'), (1, 'female'), (2, 'not specified')])),
                ('age', models.IntegerField(default=15)),
                ('symptoms', models.CharField(max_length=100)),
                ('assignedDoctorId', models.PositiveIntegerField(null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/PatientProfilePic/')),
                ('admitDate', models.DateField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('Urine_surgery', models.CharField(default='u', max_length=1000)),
                ('Blood_Pressure', models.IntegerField(default=80)),
                ('Fats', models.IntegerField(default=20)),
                ('Cholesterol', models.IntegerField(default=150)),
                ('Liver_function', models.IntegerField(default=55)),
                ('Kidney_function', models.IntegerField(default=60)),
                ('Glucose', models.IntegerField(default=80)),
                ('feedbacks', models.ManyToManyField(to='track.Feedback')),
                ('food_list', models.ManyToManyField(to='track.Food')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('department', models.CharField(default='Cardiologist', max_length=50)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/NurseProfilePic/')),
                ('status', models.BooleanField(default=False)),
                ('feedbacks', models.ManyToManyField(to='track.Feedback')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dosage', models.PositiveIntegerField(default=0)),
                ('mg', models.PositiveIntegerField(default=0)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='track.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=40)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('department', models.CharField(default='Cardiologist', max_length=50)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pic/DoctorProfilePic/')),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
