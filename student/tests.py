from django.test import TestCase, Client
from django.urls import reverse, resolve
from student.views import student_view
from student.models import Student, generate_form
from programs.models import Programs
from forms.models import Forms
from django.contrib.auth.models import User
from django.test import Client

class TestUrls (TestCase):
    def test_student_view_url_resolves(self):
        url = reverse('student_view', args=[1])
        self.assertEquals(resolve(url).func, student_view)


class TestViews (TestCase):

    def setUp(self):
        self.client = Client()

        self.program1 = Programs.objects.create(program_name='program1')
        program_id = self.program1.id

        self.student1 = Student.objects.create(student_name='student1', program_id = program_id, supervisor_id =2)
        idd = self.student1.id
        self.student_view_url = reverse('student_view', args=[idd])

        user = User.objects.create(username='student1')
        user.set_password('systempassword')
        user.save()

        self.client.login(username='student1', password='systempassword')


    def test_student_view_Get (self):
        response = self.client.get(self.student_view_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'student.html')

class TestModels(TestCase):
    def setUp(self):
        self.program1 = Programs.objects.create(
            program_name='pr_1'
        )
        pr1Id = self.program1.id

        self.st1 = Student.objects.create(
            student_name='st_1',
            program_id=pr1Id,
            supervisor_id = 2
        )
        self.form1 = Forms.objects.create(
            form_name='form_1',
            program_id=pr1Id,
            completed_by_coordinator = False,
            completed_by_supervisor = False,
            user_id=0,
            form_num = 2
        )

    def test_Student_is_assinged (self):
        self.assertEquals(self.st1.student_name,'st_1')

    def test_get_program(self):
        self.assertEquals(self.st1.get_program(),  self.program1.program_name)

    def test_get_student_forms(self):
        self.assertEquals(self.st1.get_student_forms(), [self.form1.form_num])

    def test_get_coorcomp_forms (self):
        self.assertEquals(self.st1.get_coorcomp_forms(), [self.form1.form_num])

    def test_get_sprvcomp_forms(self):
        self.assertEquals(self.st1.get_sprvcomp_forms(), [self.form1.form_num])

    #def test_generate_form(self):
        #self.assertEquals(generate_form(studentid=self.form1.user_id , form_num = self.form1.form_num), "saved")
