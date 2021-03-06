from django.contrib import messages

from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate

from . import forms, models
from django.core.mail import send_mail

from django.shortcuts import get_object_or_404


def home_view(request):
    if request.user.is_authenticated:  # check if the user is authenticated
        return HttpResponseRedirect('afterlogin')
    return render(request, 'index.html')  # home page


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  # after login for the admin
    return render(request, 'adminclick.html')


def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  # after login for the doctor
    return render(request, 'doctorclick.html')


def nurseclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  # after login for the nurse
    return render(request, 'nurseclick.html')


# for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  # after login for the patient
    return render(request, 'patientclick.html')


# admin signup
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


# doctor signup
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


# nurse signup
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


# patient signup
def patient_signup_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        print(patientForm.is_valid())
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


# check the type of the user
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


# ---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,PATIENT OR NURSE
def afterlogin_view(request):
    if request.user.is_authenticated == False:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user.is_staff:
                auth.login(request, user)
                return redirect('admin-dashboard')
            elif user is not None and user.groups.filter(name='NURSE').exists():
                auth.login(request, user)
                return redirect('nurse-dashboard')
            elif user is not None and user.groups.filter(name='PATIENT').exists():
                auth.login(request, user)
                return redirect('patient-dashboard')
            else:
                messages.info(request, 'user not found')
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
    mydict = {}
    user = models.User.objects.get(pk=request.user.pk)
    for i in models.Patient.objects.all():
        if i.user.id == user.id:
            mydict['user'] = i
    return render(request, 'patient_dashboard.html', context=mydict)


# @login_required(login_url='adminlogin')
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
def admin_add_patient(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm': userForm, 'patientForm': patientForm}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)

        if userForm.is_valid() and patientForm.is_valid() and not is_patient(request) and not is_admin(
                request) and not is_nurse(request):
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
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
def admin_page(request):
    return render(request, 'adminPage.html')


# @login_required(login_url='adminlogin')
@user_passes_test(is_admin)
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


@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients = models.Patient.objects.all()
    return render(request, 'admin_view_patient.html', {'patients': patients})


@user_passes_test(is_admin)
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


def profile(request):
    mydict = {}
    user = models.User.objects.get(pk=request.user.pk)
    for i in models.Patient.objects.all():
        if i.user.id == user.id:
            mydict['user'] = i
    return render(request, 'profile.html', mydict)


@user_passes_test(is_patient)
def edit_patient_profile(request):
    patient = models.Patient.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=patient.user_id)
    userForm = forms.PatientUserForm(instance=user)
    patientForm = forms.PatientForm(request.FILES, instance=patient)
    mydict = {'userForm': userForm, 'patientForm': patientForm, 'patient': patient}
    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST, instance=user)
        patientForm = forms.PatientForm(request.POST, instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patientForm.save()
            return HttpResponseRedirect('profile')
    return render(request, 'edit_patient_profile.html', context=mydict)


@user_passes_test(is_nurse)
def nurse_feedback(request):
    nurse = models.Nurse.objects.get(user_id=request.user.id)
    feedback = forms.FeedbackForm()
    if request.method == 'POST':
        feedback = forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request, 'feedback_for_nurse.html', {'nurse': nurse})
    return render(request, 'nurse_feedback.html', {'feedback': feedback, 'nurse': nurse})


@user_passes_test(is_admin)
def admin_feedbacks(request):
    feedback = models.Feedback.objects.all().order_by('-id')
    return render(request, 'admin_feedbacks.html', {'feedback': feedback})


@user_passes_test(is_nurse)
def nurse_view_patient(request):
    patients = models.Patient.objects.all()
    return render(request, 'nurse_view_patients.html', {'patients': patients})


@user_passes_test(is_nurse)
def nurse_add_food(request):
    if request.method == 'POST':
        food = models.Food()
        food.Name = request.POST['Name']
        food.number = request.POST['num']
        food.max_Cholesterol = request.POST['max_Cholesterol']
        food.max_Liver_function = request.POST['max_Liver_function']
        food.max_Kidney_function = request.POST['max_Kidney_function']
        food.max_Blood_Pressure = request.POST['max_Blood_Pressure']
        food.pic = request.FILES['pic']
        food.save()
        return HttpResponseRedirect('nurse-dashboard')
    return render(request, 'nurse_add_food.html')


@user_passes_test(is_nurse)
def nurse_food(request):
    return render(request, 'nurse_food.html')


@user_passes_test(is_nurse)
def nurse_view_food(request):
    food = models.Food.objects.all()
    return render(request, 'nurse_view_food.html', {'food': food})


def food_list(request, food_id):
    patient = models.Patient.objects.get(user=request.user)
    food = models.Food.objects.get(pk=food_id)
    check = patient.Cholesterol > food.max_Cholesterol or patient.Liver_function > food.max_Liver_function or patient.Kidney_function > food.max_Kidney_function or patient.Blood_Pressure > food.max_Blood_Pressure
    if request.user.is_authenticated and not request.user.is_anonymous:
        food = models.Food.objects.get(pk=food_id)
        if models.Patient.objects.filter(user=request.user, food_list=food).exists() or check == True:
            messages.error(request, '\t')
        elif check != True:
            user = models.Patient.objects.get(user=request.user)
            user.food_list.add(food)
            messages.success(request, '\t')
    else:
        redirect('')
    return redirect('patient-view-food')


@user_passes_test(is_patient)
def patient_view_food(request):
    food = models.Food.objects.all()
    return render(request, 'patient_view_food.html', {'food': food})


@user_passes_test(is_nurse)
def delete_food(request, pk):
    food = models.Food.objects.get(id=pk)
    food.delete()
    return HttpResponseRedirect('/nurse-view-food')


@user_passes_test(is_patient)
def patient_details(request):
    patient = models.Patient.objects.get(id=request.user.id)
    return render(request, 'patient_details.html', {'patient': patient})


def add_medication(request, id_patient):
    if request.method == 'POST':
        medication = models.Medication()
        medication.name = request.POST['name']
        medication.dosage = request.POST['dosage']
        medication.mg = request.POST['mg']
        medication.save()
        patient = models.Patient.objects.get(pk=id_patient)
        patient.medication_dosages.add(medication)
        return render(request, 'admin_view_patient.html', context={'patients': models.Patient.objects.all()})
    return render(request, 'admin_add_medication.html')


def upadateUrineSurgery(request, id):
    for i in models.Patient.objects.all():
        if i.id == id:
            if request.method == 'POST':
                i.Urine_surgery = request.POST['UrineSurgery']
                i.save()
    return render(request, 'updateUrineSurgery.html')


def upadateECG(request, id):
    for i in models.Patient.objects.all():
        if i.id == id:
            if request.method == 'POST':
                i.ECG = request.POST['ECG']
                i.save()
    return render(request, 'updateECG.html')


@user_passes_test(is_patient)
def patient_feedback(request):
    if request.method == 'POST':
        feedback = models.Feedback()
        feedback.by = request.user.username
        feedback.message = request.POST['message']
        feedback.senderType = request.POST['senderType']
        feedback.save()
        patient = models.Patient()
        for i in models.Patient.objects.all():
            if request.user == i.user:
                patient = i
                patient.feedbacks.add(feedback)
                return render(request, 'feedback_for_patient.html')
    return render(request, 'patient_feedback.html')


def feedback_list(request):
    context = {}
    patient = models.Patient()
    if request.user.is_authenticated and not request.user.is_anonymous:
        for i in models.Patient.objects.all():
            if request.user == i.user:
                patient = i
                context['feedbacks'] = patient.feedbacks
                feedbacks = patient.feedbacks.all()
        return render(request, 'patient_feedbacks.html', {'feedbacks': feedbacks})


def show_food_list(request):
    context = {}
    if request.user.is_authenticated and not request.user.is_anonymous:
        for i in models.Patient.objects.all():
            if request.user == i.user:
                patient = i
                context['food'] = patient.food_list.all()
    return render(request, 'show_food_list.html', context)


@user_passes_test(is_admin)
def admin_replay(request, pk):
    feedback = models.Feedback.objects.all().get(id=pk)
    if request.method == 'POST':
        feedback.replay = request.POST['replay']
        feedback.save()
        return render(request, 'replay_for_admin.html')
    return render(request, 'admin_replay.html')


def nurseMessage(request, pk):
    patient = models.Patient.objects.all().get(id=pk)
    print(patient)
    if request.method == 'POST':
        message = models.Feedback()
        message.by = request.user.username
        message.message = request.POST['message']
        message.senderType = request.POST['senderType']
        message.save()
        patient.feedbacks.add(message)
        return render(request, 'message_for_nurse.html')
    return render(request, 'nurseMessage.html', {'user': request.user})


def updateGlucose(request, id):
    # print(pk)
    # if request.method == "GET":
    user = models.User.objects.get(pk=id)
    for i in models.Patient.objects.all():
        if i.user.id == user.id:
            if request.method == 'POST':
                i.Glucose = request.POST['Glucose']
                i.save()
    return render(request, 'updateGlucose.html')


def updateBloodPressure(request, id):
    user = models.User.objects.get(pk=id)
    for i in models.Patient.objects.all():
        if i.user.id == user.id:
            if request.method == 'POST':
                i.Blood_Pressure = request.POST['BloodPressure']
                i.save()
    return render(request, 'updateBloodPressure.html')


def updateLiverFunction(request, id):
    if request.method == 'POST':
        user = models.Patient.objects.get(pk=id)
        user.Liver_function = request.POST['LiverFunction']
        user.save()
    return render(request, 'updateLiverFunction.html')


def Appointment(request):
    return render(request, 'patient_appointment.html')


def AdminBookAppointment(request):
    patient = models.Patient()
    if request.method == 'POST':
        c = False
        for i in models.Patient.objects.all():
            if i.user.username == request.POST['patientName']:
                c = True
                patient = i
        if c:
            patient.appointment.date = request.POST['appointment']
            patient.appointment.time = request.POST['time']
            patient.appointment.name = patient.user
            ap = models.Appointment()
            ap.date = request.POST['appointment']
            ap.time = request.POST['time']
            ap.name = patient.user
            flag = True
            for i in models.Appointment.objects.all():
                # print(str(i.time)[0:5])
                # print(str(patient.appointment.time))
                # print(str(patient.appointment.date))
                if (str(i.date) == str(patient.appointment.date) and str(i.time)[0:5] == str(patient.appointment.time)):
                    flag = False
                    messages.error(request, "The role is already booked")
            if flag:
                patient.save()
                ap.save()
                messages.success(request, "Book Success")
    return render(request, 'AdminBookAppointment.html', {'patients': models.Patient.objects.all()})


def BookAppointment(request):
    if request.method == 'POST':
        user = models.Patient.objects.get(user=request.user)
        print(user)
        user.appointment.date = request.POST['appointment']
        user.appointment.time = request.POST['time']
        user.appointment.name = request.user.username
        ap = models.Appointment()
        ap.date = request.POST['appointment']
        ap.time = request.POST['time']
        ap.name = user.appointment.name
        flag = True
        for i in models.Appointment.objects.all():
            print(str(i.time)[0:5])
            print(str(user.appointment.time))
            print(str(user.appointment.time))
            if (str(i.date) == str(user.appointment.date) and str(i.time)[0:5] == str(user.appointment.time)):
                flag = False
                messages.error(request, "The role is already booked")
        if flag:
            user.save()
            ap.save()
            messages.success(request, "Book Success")
    return render(request, 'BookAppointment.html')


def MyAppointment(request):
    user = models.Patient.objects.get(user=request.user)
    print(user.appointment.name)
    return render(request, 'MyAppointment.html', {'appointment': user.appointment})


def Admin_Appointment(request):
    return render(request, 'admin_appointment.html')


def adminAppointments(request):
    appointments = models.Appointment.objects.all()
    return render(request, 'adminAppointments.html', {'appointments': appointments})


def updateKidneyFunction(request, id):
    if request.method == 'POST':
        user = models.Patient.objects.get(pk=id)
        user.Kidney_function = request.POST['KidneyFunction']
        user.save()
    return render(request, 'updateKidneyFunction.html')


def updateCholesterol(request, id):
    if request.method == 'POST':
        user = models.Patient.objects.get(pk=id)
        user.Cholesterol = request.POST['Cholesterol']
        user.save()
    return render(request, 'updateCholesterol.html')


def updateFats(request, id):
    if request.method == 'POST':
        user = models.Patient.objects.get(pk=id)
        user.Fats = request.POST['Fats']
        user.save()
    return render(request, 'updateFats.html')


def show_medication_list(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        userInfo = models.Patient.objects.get(user=request.user)
        print(userInfo.food_list)
        medication = userInfo.medication_dosages.all()
        context = {'medication': medication}
    return render(request, 'show_medication_list.html', context)


from django.shortcuts import render, redirect, reverse
from django.conf import settings

from track import mixin

'''
Basic view for routing 
'''


def route(request):
    context = {
        "google_api_key": settings.GOOGLE_API_KEY,
        "base_country": settings.BASE_COUNTRY}
    return render(request, 'main/route.html', context)


'''
Basic view for displaying a map 
'''


def map(request):
    return render(request, 'map.html')


def contact(request):
    print("contact")
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            # try:x
            send_mail(subject, message, 'salemgode@gmail.com', ['salemgode@gmail.com'])
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found.')
        return redirect('')

    form = forms.ContactForm()
    return render(request, "contactus.html", {'form': form})


def map(request):
    return render(request, 'map.html')
