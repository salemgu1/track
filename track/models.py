from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from datetime import datetime


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50, default='Cardiologist')
    profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/', null=True, blank=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.department)


GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),
)


class Feedback(models.Model):
    date = models.DateField(auto_now=True)
    by = models.CharField(max_length=40)
    message = models.CharField(max_length=500)
    senderType = models.CharField(max_length=40, default="user type")
    replay = models.CharField(max_length=500, default="There is no response to this message")


class Food(models.Model):
    Name = models.CharField(max_length=50)
    number = models.IntegerField(default=1)
    max_Cholesterol = models.IntegerField(default=150)
    max_Liver_function = models.IntegerField(default=55)
    max_Kidney_function = models.IntegerField(default=60)
    max_Blood_Pressure = models.IntegerField(default=80)
    pic = models.ImageField(upload_to='profile_pic/Food/', null=True, blank=True)


class Medication(models.Model):
    name = models.CharField(max_length=255)
    dosage = models.PositiveIntegerField(default=0)
    mg = models.PositiveIntegerField(default=0)


class Appointment(models.Model):
    date = models.DateField(default=now)
    name = models.CharField(default="unknown",max_length=30)
    time = models.TimeField(default=datetime.now().time())


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    age = models.IntegerField(default=15)
    symptoms = models.CharField(max_length=100, null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    profile_pic = models.ImageField(upload_to='profile_pic/PatientProfilePic/', null=True, blank=True)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    Urine_surgery = models.CharField(max_length=1000, default='u')
    Blood_Pressure = models.IntegerField(default=80)
    Fats = models.IntegerField(default=20)
    Cholesterol = models.IntegerField(default=150)
    Liver_function = models.IntegerField(default=55)
    Kidney_function = models.IntegerField(default=60)
    ECG = models.IntegerField(default=70)
    Glucose = models.IntegerField(default=80)
    food_list = models.ManyToManyField(Food)
    feedbacks = models.ManyToManyField(Feedback)
    medication_dosages = models.ManyToManyField(Medication)
    appointment=Appointment()
    # appointment = models.DateField(default=now)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name + " (" + self.symptoms + ")"


class Appointment(models.Model):
    date = models.DateField(default=now)
    name = models.CharField(default="unknown",max_length=30)
    time = models.TimeField(default=datetime.now())


class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    department = models.CharField(max_length=50, default='Cardiologist')
    profile_pic = models.ImageField(upload_to='profile_pic/NurseProfilePic/', null=True, blank=True)
    status = models.BooleanField(default=False)
    feedbacks = models.ManyToManyField(Feedback)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} ({})".format(self.user.first_name, self.department)
