from django.db import models
from questions.models import Question, clone_ques
from django.utils import timezone
import datetime

class Forms(models.Model):

    form_name = models.TextField()
    program_id = models.IntegerField()
    completed_by_coordinator = models.BooleanField(default=False)
    completed_by_supervisor=models.BooleanField(default=False)
    completed_by_student = models.BooleanField(default=False)
    user_id = models.IntegerField(default=0)
    form_num = models.IntegerField(default=0)
    time_completed_by_coordinator = models.DateTimeField(default=timezone.now(), null=False)
    time_completed_by_supervisor = models.DateTimeField(default=timezone.now(), null=False)
    time_completed_by_student = models.DateTimeField(default=timezone.now(), null=False)

def get_questions(form):
    question_id = []
    questions = Question.objects.all()
    # print(form.form_num)
    for question in questions:
        if form.form_num == question.form_number:
            question_id.append(question.id)
    return question_id

def get_questions2(form):
    question_id = []
    questions = Question.objects.all()
    # print(form.form_num)
    for question in questions:
        if form.id == question.form_number:
            question_id.append(question.id)
    return question_id

def check_form(studentid, formnum):
    forms = Forms.objects.all()
    checkform = None
    for form in forms:
        if form.form_num == formnum and form.user_id == studentid:
            checkform = form
    if checkform == None:
        return False
    else:
        return True
        

# creates new form at new ID, and grabs questions via get_quesstions() function
def clone_form(formnum): 
  
    forms = Forms.objects.all()
    checkform = None
    formn = 0
    for form in forms:
     
        if form.form_num == formnum and form.user_id == 0:
            checkform = form
        if formn < form.form_num:
            formn = form.form_num
    qids = get_questions2(checkform)
    # print(qids)
    checkform.id = None
    checkform.user_id = 0
    checkform.form_num = formn + 1
    checkform.completed_by_coordinator = False
    checkform.save()
    for qid in qids:
        clone_ques(qid, checkform.id)
    return checkform.id


def getnewformn():
    forms = Forms.objects.all()
    formn = 0
    for form in forms:
        if formn < form.form_num:
            formn = form.form_num
    return formn + 1


# Create your models here.
