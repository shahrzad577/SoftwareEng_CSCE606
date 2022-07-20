from django.test import TestCase, Client
from django.urls import reverse, resolve
from forms.views import form_create_view, forms_view, student_form_view
from forms.models import Forms, get_questions, check_form, clone_form, getnewformn
from questions.models import Question
from forms.forms import FormsForm, RawFormsForm
from django.contrib.auth.models import User
from django.test import Client
from student.models import Student

# Create your tests here.
class TestUrls (TestCase):

    def test_forms_view_url_resolves(self):
        url = reverse('form_view', args=[1])
        # print(resolve(url))
        self.assertEquals(resolve(url).func, forms_view)

    def test_form_create_view_url_resolves(self):
        url = reverse('create_form')
        self.assertEquals(resolve(url).func, form_create_view)

    def test_student_form_view(self):
        self.form1 = Forms.objects.create(
            #form_name='test_form',
            program_id=4,
            completed_by_coordinator=True,
            completed_by_supervisor=True,
            completed_by_student = True,
            user_id=0,
            form_num=1,
        )
        self.st1 = Student.objects.create(
            student_name='st_1',
            program_id=1,
            supervisor_id=2
        )
        id = self.form1.id
        stId = self.st1.id
        url = reverse('student_form_view', args = [stId, id])
        self.assertEquals(resolve(url).func, student_form_view)


class TestViews (TestCase):

    def setUp(self):
        self.client = Client()

        self.form1 = Forms.objects.create(
            #form_name='test_form',
            program_id=4,
            completed_by_coordinator=True,
            completed_by_supervisor=True,
            completed_by_student=True,
            user_id=0,
            form_num=1
        )
        self.st1 = Student.objects.create(
            student_name='st_1',
            program_id=1,
            supervisor_id=2
        )

        user = User.objects.create(username='coordinator')
        user.set_password('systempassword')
        user.save()
        self.client.login(username='coordinator', password='systempassword')

        id = self.form1.id
        stId = self.st1.id

        self.form_view_url = reverse('form_view', args=[id])
        self.create_form_url = reverse('create_form')
        self.student_form_view = reverse ('student_form_view', args= [stId, id])

    def test_forms_view_Get (self):
        response = self.client.get(self.form_view_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_form.html')


    def test_form_create_view_Get (self):
        response = self.client.get(self.create_form_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_create.html')

    def test_form_not_available(self):
        response = self.client.get(self.student_form_view)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_not_avail.html')


class TestModels(TestCase):
    def setUp(self):
        self.form1 = Forms.objects.create(
            #form_name='form_1',
            program_id=10,
            completed_by_coordinator = True,
            completed_by_supervisor = True,
            completed_by_student=True,
            user_id=0,
            form_num = 1
        )

    def test_Forms_is_assinged (self):
        self.assertEquals(self.form1.program_id,10)
        self.assertEquals(self.form1.user_id, 0)


class TestForms(TestCase):
    def setUp(self):
        self.form1 = Forms.objects.create(
            #form_name='form_1',
            program_id=10,
            completed_by_coordinator=True,
            completed_by_supervisor=True,
            completed_by_student=True,
            user_id=1,
            form_num=2
        )
    
    #check if form is not empty  *** not solved
    #def test_FormsForm(self):
        #form = FormsForm(data={
        #'model':self.form1, 'fields':[10, False, False,True, 1, 2]})
        #self.assertTrue(form.is_valid())
    
    #check if form is empty
    def test_FormsForm_no_data(self):
        form = FormsForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),7)


class TestModelFunctions(TestCase):
    def setUp(self):
        self.form1 = Forms.objects.create(
            #form_name='form_1',
            program_id=10,
            completed_by_coordinator=True,
            completed_by_supervisor=True,
            completed_by_student=True,
            user_id=1,
            form_num=2
        )

    def test_get_questions(self):
        self.q1 = Question.objects.create(
            question_type=1,
            question_content='content',
            question_answer='answer',
            options_number=3,
            form_number=self.form1.form_num
        )
        questionId = self.q1.id
        self.assertEquals(get_questions(self.form1), [questionId])

    def test_check_form(self):
     userId = self.form1.user_id

     self.st1 = Student.objects.create(
         student_name='st_1',
         program_id=1,
         supervisor_id=2
     )
     self.st1.id = userId
     self.form1.user_id = userId
     self.assertEquals(check_form(self.st1.id, self.form1.form_num), True)

    def test_getnewformn(self):
        self.form1 = Forms.objects.create(
            #form_name='form_1',
            program_id=10,
            completed_by_coordinator=True,
            completed_by_supervisor=True,
            completed_by_student=True,
            user_id=0,
            form_num=1000
        )
        self.assertEquals(getnewformn(), self.form1.form_num+1)
'''
    def test_clone_form (self):
        self.form2 = Forms.objects.create(
            program_id=10,
            completed_by_coordinator=True,
            completed_by_supervisor=True,
            completed_by_student=True,
            user_id=0,
            form_num=1000
        )
        idd = self.form2.id
        self.assertEquals(clone_form(self.form2.form_num), idd)
'''



from forms.views import questions, get_form

class TestViewsFunctions(TestCase):
    def test_questions (self):
        self.q1 = Question.objects.create(
            question_type=1,
            question_content='content',
            question_answer='answer',
            options_number=3,
            form_number=1
        )
        id1 = self.q1.id
        self.q2 = Question.objects.create(
            question_type=2,
            question_content='content2',
            question_answer='answer2',
            options_number=4,
            form_number=1
        )
        id2 = self.q2.id
        question_ids = [id1, id2]
        self.assertEquals(questions(question_ids), [self.q1, self.q2])