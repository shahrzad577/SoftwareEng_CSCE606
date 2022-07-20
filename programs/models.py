from django.db import models
from forms.models import Forms
# from student.models import Student

class Programs(models.Model):
    program_name = models.TextField()

def get_forms(program):
    form_id = []
    forms = Forms.objects.all()
    for form in forms:
        if form.user_id == 0:
            if program.id == form.program_id:
                form_id.append(form.form_num)
    return form_id

def get_forms_cc(program):
    form_id = []
    forms = Forms.objects.all()
    for form in forms:
        if form.user_id == 0:
            if program.id == form.program_id:
                form_id.append(form.form_num)
    return form_id

def get_forms_cs(program):
    form_id = []
    forms = Forms.objects.all()
    for form in forms:
        if form.user_id == 0:
            if program.id == form.program_id:
                form_id.append(form.form_num)
    return form_id

def get_forms_cs22(program,id):
    form_id = []
    forms = Forms.objects.all()
    for form in forms:
        if form.user_id == id:
            if program.id == form.program_id:
                form_id.append(form)
    return form_id
# Create your models here.
