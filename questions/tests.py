from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.test import TestCase
from questions.models import Question

# Create your tests here.
class TestModels(TestCase):
    def setUp(self):
        self.q1 = Question.objects.create(
            question_type=0,
            question_content='my_question',
            question_answer='my_answer',
            options_number=3,
            form_number=123
        )

    def test_Quetsion_is_assinged (self):
        self.assertEquals(self.q1.question_type,0)

    def test_are_options(self):
        self.assertEquals(self.q1.are_options(), False)

    def test_ret_question(self):
        self.assertEquals(self.q1.ret_question(), 'my_question')
