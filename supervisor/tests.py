from django.test import TestCase, Client
from django.urls import reverse, resolve
from supervisor.views import supervisor_view
from supervisor.models import SuperVisor
from student.models import Student
import json

class TestUrls (TestCase):
    def test_supervisor_view_url_resolves(self):
        url = reverse('supervisor_view', args=[1])
        self.assertEquals(resolve(url).func, supervisor_view)


class TestViews (TestCase):

    def setUp(self):
        self.client = Client()

        self.student1 = Student.objects.create(student_name='student1', program_id=1, supervisor_id =1)
        id1 = self.student1.id

        self.student2 = Student.objects.create(student_name='student2', program_id=2, supervisor_id =1)
        id2 = self.student2.id

        self.supervisor1 = SuperVisor.objects.create(
            supervisor_name='supervisor1', student1_id=id1, student2_id=id2)
        idd = self.supervisor1.id
        self.supervisor_view_url = reverse('supervisor_view', args=[idd])


    def test_supervisor_view_Get (self):
        response = self.client.get(self.supervisor_view_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'supervisor.html')

class TestModels(TestCase):
    def setUp(self):
        self.student1 = Student.objects.create(
            student_name='st1',
            program_id=123,
            supervisor_id =1
        )
        self.student2 = Student.objects.create(
            student_name='st2',
            program_id=567,
            supervisor_id=1
        )

        self.superVisor1 = SuperVisor.objects.create(
            supervisor_name='sp_1',
            student1_id=self.student1.id,
            student2_id=self.student2.id
        )

    def test_Supervisor_name_is_assinged (self):
        self.assertEquals(self.superVisor1.supervisor_name,'sp_1')

    def test_get_students(self):
        self.assertEquals(self.superVisor1.get_students(), [self.student1, self.student2])