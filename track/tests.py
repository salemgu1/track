from django.test import TestCase
from django.test import TestCase, tag
from django.urls import reverse


class AppointmentTest(TestCase):

    @tag('unit-test')
    def test_appointment_access_url(self):
        response = self.client.get('appointment')
        self.assert_(response.status_code, 200)


class BookAppointmentTest(TestCase):

    @tag('unit-test')
    def test_Book_Appointment_access_url(self):
        response = self.client.get('bookappointment')
        self.assert_(response.status_code, 200)
     
    @tag('unit-test')
    def test_Show_Appointment_access_url(self):
        response = self.client.get('My-Appointment')
        self.assert_(response.status_code, 200)

class AdminAppointment(TestCase):
    @tag('unit-test')
    def test_Bookappointment_access_url(self):
        response = self.client.get('admin-appointment')
        self.assert_(response.status_code, 200)
