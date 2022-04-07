from django.contrib import messages

from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate

from . import forms, models


def home_view(request):
    if request.user.is_authenticated:           #check if the user is authenticated
        return HttpResponseRedirect('afterlogin')
    return render(request, 'index.html')        #home page



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')       #after login for the admin
    return render(request, 'adminclick.html')



def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')       #after login for the doctor
    return render(request, 'doctorclick.html')


def nurseclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')       #after login for the nurse
    return render(request, 'nurseclick.html')


# for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')   #after login for the patient
    return render(request, 'patientclick.html')

#admin signup
def admin_signup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request, 'adminsignup.html', {'form': form})

#doctor signup
def doctor_signup_view(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorForm.save(commit=False)
            doctor.user = user
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            doctor = doctor.save()
            # my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('doctorlogin')
    return render(request, 'doctorsignup.html', context=mydict)

#nurse signup
def nurse_signup_view(request):

    userForm = forms.NurseUserForm()
    nurseForm = forms.NurseForm()
    mydict = {'userForm': userForm, 'nurseForm': nurseForm}
    if request.method == 'POST':
        userForm = forms.NurseUserForm(request.POST)
        nurseForm = forms.NurseForm(request.POST, request.FILES)
        if userForm.is_valid() and nurseForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            nurse = nurseForm.save(commit=False)
            nurse.user = user
            nurse = nurse.save()
            my_nurse_group = Group.objects.get_or_create(name='NURSE')
            my_nurse_group[0].user_set.add(user)
        return HttpResponseRedirect('nurselogin')
    return render(request, 'nursesignup.html', context=mydict)

#patient signup
def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient = patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request, 'patientsignup.html', context=mydict)

#check the type of the user
def is_admin(user):
    return user.is_staff


def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()


def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def is_nurse(user):
    return user.groups.filter(name='NURSE').exists()

def logoutUser(request):
    logout(request)
    return redirect('login')

# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR,PATIENT OR NURSE
def afterlogin_view(request):
    if request.user.is_authenticated == False:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            print(user.is_staff)
            if user.is_staff:
                print("Asdasdasd")
                auth.login(request, user)
                return redirect('admin-dashboard')
            elif user is not None and user.groups.filter(name='DOCTOR').exists():
                auth.login(request, user)
                return redirect('doctor-dashboard')
            elif user is not None and user.groups.filter(name='NURSE').exists():
                auth.login(request, user)
                return redirect('nurse-dashboard')
            elif user is not None and user.groups.filter(name='PATIENT').exists():
                auth.login(request, user)
                return redirect('patient-dashboard')
            else:
                messages.info(request,'user not found')
                return redirect('login')
        else:
            return render(request, 'loginPage.html')
    else:
        if request.user.is_staff:
            return redirect('admin-dashboard')
        if request.user.groups.filter(name='DOCTOR'):
            return redirect('doctor-dashboard')
        if request.user.groups.filter(name='NURSE'):
            return redirect('nurse-dashboard')
        if request.user.groups.filter(name='PATIENT'):
            return redirect('patient-dashboard')



# @login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    mydict = {
    }
    return render(request, 'admin_dashboard.html', context=mydict)


# @login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    mydict = {
    }
    return render(request, 'doctor_dashboard.html', context=mydict)

# @login_required(login_url='nurselogin')
@user_passes_test(is_nurse)
def nurse_dashboard(request):
    mydict = {
    }
    return render(request, 'nurse_dashboard.html', context=mydict)



# @login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard(request):
    mydict = {
    }
    return render(request, 'patient_dashboard.html', context=mydict)


# @login_required(login_url='adminlogin')
def admin_add_nurse(request):
    userForm = forms.NurseUserForm()
    nurseForm = forms.NurseForm()
    mydict = {'userForm': userForm, 'nurseForm': nurseForm}
    if request.method == 'POST':
        print("add nurse")
        userForm = forms.NurseUserForm(request.POST)
        nurseForm = forms.NurseForm(request.POST, request.FILES)
        print(userForm.is_valid())
        print(nurseForm.is_valid())
        if userForm.is_valid() and nurseForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            nurse = nurseForm.save(commit=False)
            nurse.user = user
            nurse.save()
            my_nurse_group = Group.objects.get_or_create(name='NURSE')
            my_nurse_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-nurse')
    return render(request, 'admin_add_nurse.html', context=mydict)

# @login_required(login_url='adminlogin')
def admin_add_patient(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        print(userForm.is_valid())
        print(patientForm.is_valid())
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-patient')
    return render(request, 'admin_add_patient.html', context=mydict)



# @login_required(login_url='adminlogin')
def admin_add_doctor(request):
    userForm = forms.DoctorUserForm()
    doctorForm = forms.DoctorForm()
    mydict = {'userForm': userForm, 'doctorForm': doctorForm}
    if request.method == 'POST':
        userForm = forms.DoctorUserForm(request.POST)
        doctorForm = forms.DoctorForm(request.POST, request.FILES)
        print(userForm.is_valid())
        print(doctorForm.is_valid())
        if userForm.is_valid() and doctorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            nurse = doctorForm.save(commit=False)
            nurse.user = user
            nurse.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-doctor')
    return render(request, 'admin_add_doctor.html', context=mydict)

# @login_required(login_url='adminlogin')
def admin_page(request):
    return render(request, 'adminPage.html')

# @login_required(login_url='adminlogin')
def admin_view_nurse(request):
    nurses = models.Nurse.objects.all()
    return render(request, 'admin_view_nurse.html', {'nurses': nurses})


# @login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        'doctor': models.Doctor.objects.get(user_id=request.user.id),  # for profile picture of doctor in sidebar
    }
    return render(request, 'doctor_patient.html', context=mydict)


# @login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request, 'admin_patient.html')

# @login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request, 'admin_doctor.html')

# @login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_nurse_view(request):
    return render(request, 'admin_nurse.html')


# @login_required(login_url='adminlogin')
def admin_view_doctor_view(request):
    doctors = models.Doctor.objects.all()
    return render(request, 'admin_view_doctor.html', {'doctors': doctors})



# @login_required(login_url='adminlogin')
def delete_doctor_view(request, pk):
    doctor = models.Doctor.objects.get(id=pk)
    user = models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete() 
    return HttpResponseRedirect('/admin-view-doctor')

# @login_required(login_url='adminlogin')
def admin_view_nurse_view(request):
    nurses = models.Nurse.objects.all()
    return render(request, 'admin_view_doctor.html', {'nurses': nurses})


# @login_required(login_url='adminlogin')
def delete_nurse_view(request, pk):
    nurse = models.Nurse.objects.get(id=pk)
    user = models.User.objects.get(id=nurse.user_id)
    user.delete()
    nurse.delete()
    return HttpResponseRedirect('/admin-view-nurse')

# @login_required(login_url='adminlogin')
def admin_view_patient_view(request):
    patients = models.Patient.objects.all()
    return render(request, 'admin_view_patient.html', {'patients': patients})

# @login_required(login_url='adminlogin')
def delete_patient_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    user = models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return HttpResponseRedirect('/admin-view-patient')

def about(request):
    return render(request, 'aboutus.html')


def contactus(request):
    return render(request, 'contactus.html')
