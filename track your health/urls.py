"""track your health URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from track import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name=''),


    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('nurseclick', views.nurseclick_view),
    path('patientclick', views.patientclick_view),


    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view, name='doctorsignup'),
    path('nursesignup', views.nurse_signup_view, name='nursesignup'),
    path('patientsignup', views.patient_signup_view),


    path('adminlogin', LoginView.as_view(template_name='loginPage.html')),
    path('login',views.afterlogin_view,name='login'),
    path('doctorlogin', LoginView.as_view(template_name='loginPage.html')),
    path('nurselogin', LoginView.as_view(template_name='loginPage.html')),
    path('patientlogin', LoginView.as_view(template_name='loginPage.html')),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('admin-patient', views.admin_patient_view, name='admin-patient'),
    path('admin-doctor', views.admin_doctor_view, name='admin-doctor'),
    path('admin-nurse', views.admin_nurse_view, name='admin-nurse'),
 
    path('admin-view-doctor', views.admin_view_doctor_view, name='admin-view-doctor'),
    path('admin-view-nurses', views.admin_view_nurse_view, name='admin-view-nurse'),
    path('admin-view-patient', views.admin_view_patient_view, name='admin-view-patient'),

    path('nurse-patient', views.nurse_view_patient, name='nurse-patient'),
    path('update-Urine-surgery/<int:pk>', views.upadateUrineSurgery, name='update-Urine-surgery'),
    path('update-Glucose/<int:id>', views.updateGlucose, name='update-Glucose'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),


    path('admin-dashboard', views.admin_page, name='admin-dashboard'),
    path('patient-dashboard', views.patient_dashboard, name='patient-dashboard'),
    path('doctor-dashboard', views.doctor_dashboard, name='doctor-dashboard'),
    path('nurse-dashboard', views.nurse_dashboard, name='nurse-dashboard'),

    path('delete-doctor/<int:pk>', views.delete_doctor_view, name='delete-doctor'),
    path('delete-nurse/<int:pk>', views.delete_nurse_view, name='delete-nurse'),
    path('delete-patient/<int:pk>', views.delete_patient_view, name='delete-patient'),



    path('admin-add-nurse', views.admin_add_nurse, name='admin-add-nurse'),
    path('admin-view-nurse', views.admin_view_nurse, name='admin-view-nurse'),
    path('admin-add-patient', views.admin_add_patient, name='admin-add-patient'),
    path('admin-view-patient', views.admin_view_patient_view, name='admin-view-patient'),
    path('admin-add-doctor', views.admin_add_doctor, name='admin-add-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view, name='admin-view-doctor'),



    path('aboutus', views.about, name='aboutus'),
    path('contactus', views.contactus, name='contactus'),
    path('nurse-feedback', views.nurse_feedback, name='nurse-feedback'),
    path('admin-feedbacks', views.admin_feedbacks, name='admin-feedbacks'),
    path('patient-feedback', views.patient_feedback, name='patient-feedback'),
    path('send-replay/<int:pk>', views.admin_replay, name='send-replay'),
    path('patient-replays', views.feedback_list, name='patient-replays'),

    # path('delete-patient-user/<int:pk>', views.delete_patient, name='delete-patient-user'),

    path('profile/', views.profile, name='users-profile'),
     # for the nurse to setup food
    path('nurse-add-food', views.nurse_add_food, name='nurse-add-food'),
    path('nurse-food', views.nurse_food, name='nurse-food'),
    path('nurse-view-food', views.nurse_view_food, name='nurse-view-food'),
    path('delete-food/<int:pk>', views.delete_food, name='delete-food'),

    #for the patient to add food to food_list
    path('food-favorite/<int:food_id>',views.food_list,name='food-favorite'),
    path('show-food-list', views.show_food_list, name='show-food-list'),
    path('patient-view-food', views.patient_view_food, name='patient-view-food'),
    path('show-medication-list', views.show_medication_list, name='show-medication-list'),

    path('patient-details', views.patient_details, name='patient-details'),
    path('add-medication/<int:id_patient>', views.add_medication, name='add-medication'),


    path('logout', views.logoutUser,name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
