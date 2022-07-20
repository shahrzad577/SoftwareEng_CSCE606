from django.test import TestCase, Client
from django.urls import reverse, resolve
from program_coordinator.views import pc_view
from program_coordinator.models import Program_Coordinator
from django.contrib.auth.models import User
from django.test import Client


class TestUrls (TestCase):
    def test_pc_view_url_resolves(self):
        url = reverse('program_coordinator')
        self.assertEquals(resolve(url).func, pc_view)


class TestViews (TestCase):

    def setUp(self):
        self.client = Client()
        self.pc_view_url = reverse('program_coordinator')

        user = User.objects.create(username='coordinator')
        user.set_password('systempassword')
        user.save()

        self.client.login(username='coordinator', password='systempassword')


    def test_program_coordinator_view_Get (self):
        response = self.client.get(self.pc_view_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'coordinator.html')

class TestModels(TestCase):
    def setUp(self):
        self.pc1 = Program_Coordinator.objects.create(
            pc_name='pc_1'
        )

    def test_Program_Coordinator_name_is_assinged (self):
        self.assertEquals(self.pc1.pc_name,'pc_1')
