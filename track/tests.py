from django.test import TestCase
from django.test import TestCase, tag
from django.urls import reverse
# Create your tests here.


class NurseMessageTest(TestCase):

    @tag('unit-test')
    def test_message_access_url(self):
        response = self.client.get('nurse-message')
        self.assert_(response.status_code, 200)

    @tag('unit-test')
    def test_message_access_template(self):
        response = self.client.get(('nurse-message'))
        self.assert_(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'nurseMessage.html')





