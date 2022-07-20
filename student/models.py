from tabnanny import check
from django.db import models
from programs.models import Programs, get_forms, get_forms_cc, get_forms_cs, get_forms_cs22
from forms.models import Forms, check_form, get_questions, get_questions2
from questions.models import clone_ques
# from supervisor.models import SuperVisor
class Student(models.Model):

    student_name = models.TextField()
    program_id = models.IntegerField()
    supervisor_id = models.IntegerField()

    def get_program(self):
        program = Programs.objects.get(id=self.program_id).program_name
        return program
    def get_student_forms(self):
        program = Programs.objects.get(id = self.program_id)
        form_ids = get_forms(program)
        return form_ids
    def get_coorcomp_forms(self):
        program = Programs.objects.get(id = self.program_id)
        form_ids = get_forms_cc(program)
        return form_ids
    def get_sprvcomp_forms(self):
        program = Programs.objects.get(id = self.program_id)
        form_ids = get_forms_cs(program)
        return form_ids
    def get_sprvcomp_forms22(self):
        program = Programs.objects.get(id = self.program_id)
        form_ids = get_forms_cs22(program,self.id)
        return form_ids
    
def generate_form(studentid, form_num):
    forms = Forms.objects.all()
    # print(form_num)
    form = None
    for f in forms:
        # print(f.form_num)
        if f.form_num == form_num and f.user_id == 0:
            form = f
    qids = get_questions(form)
    form.id = None
    form.user_id = studentid
    form.save()
    for qid in qids:
        clone_ques(qid, form.id)
    print("saved")

def generate_form2(studentid, form_num):

    if not check_form(studentid, form_num):
        forms = Forms.objects.all()
        # print(form_num)
        form = None
        for f in forms:
            # print(f.form_num)
            if f.form_num == form_num and f.user_id == 0:
                form = f
        qids = get_questions2(form)
        form.id = None
        form.user_id = studentid
        form.save()
        for qid in qids:
            clone_ques(qid, form.id)
        # print("saved")

def generate_forms(student):
    form_ids = student.get_student_forms()
    # print(form_ids)
    for i in range(len(form_ids)):
        if not check_form(student.id, form_ids[i]):
            # print(form_ids[i])
            generate_form(student.id, form_ids[i])
# Create your models here.
