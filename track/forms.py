from django import forms
from django.contrib.auth.models import User
from . import models


#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

#for doctor signup
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']


#for nurse signup
class NurseUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }



class NurseForm(forms.ModelForm):
    class Meta:
        model=models.Nurse
        fields=['address','mobile','department','status','profile_pic']



class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
    class Meta:
        model=models.Patient 
        fields=['address','status','symptoms','profile_pic','gender','age']

class DeactivateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = ['by', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 6, 'cols': 30})
        }