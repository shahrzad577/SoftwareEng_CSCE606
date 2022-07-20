from django.test import TestCase, Client
from django.urls import reverse, resolve
from programs.views import program_view, program_create_view
from programs.models import Programs, get_forms, get_forms_cc, get_forms_cs
from forms.models import Forms
from django.contrib.auth.models import User
from django.test import Client


class TestUrls (TestCase):
    def test_program_view_url_resolves(self):
        url = reverse('program_view', args=[1])
        self.assertEquals(resolve(url).func, program_view)

    def test_program_create_view_url (self):
        url = reverse('create_program')
        self.assertEquals(resolve(url).func, program_create_view)

        
class TestViews (TestCase):

    def setUp(self):
        self.client = Client()

        user = User.objects.create(username='user')
        user.set_password('systempassword')
        user.save()
        self.client.login(username='user', password='systempassword')

        self.program1 = Programs.objects.create(program_name='program1')
        idd = self.program1.id
        self.program_view_url = reverse('program_view', args=[idd])

        self.program_create_view_url = reverse('create_program')

    def test_forms_view_Get (self):
        response = self.client.get(self.program_view_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'program.html')

    def test_program_create_view(self):
        response = self.client.get(self.program_create_view_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'program_create.html')


class TestModels(TestCase):
    def setUp(self):
        self.program1 = Programs.objects.create(
            program_name='program_1',
        )

    def test_Program_is_assinged (self):
        self.assertEquals(self.program1.program_name,'program_1')


class TestModelFunctions(TestCase):
    def setUp(self):
        self.program1 = Programs.objects.create(program_name='program1')
        self.form1 = Forms.objects.create(
            # form_name='form_1',
            program_id=10,
            completed_by_coordinator=True,
            completed_by_supervisor=True,
            completed_by_student=True,
            user_id=0,
            form_num=2
        )
        self.program1.id = self.form1.program_id
    def test_getforms(self):
        self.assertEquals(get_forms(self.program1), [self.form1.form_num])
    def test_get_forms_cc(self):
        self.assertEquals(get_forms_cc(self.program1), [self.form1.form_num])

    def test_get_forms_cs(self):
        self.assertEquals(get_forms_cs(self.program1), [self.form1.form_num])
