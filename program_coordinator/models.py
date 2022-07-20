from django.db import models
from forms.models import Forms

class Program_Coordinator(models.Model):
    pc_name = models.TextField()


# def update_form(form_num):
#     forms = Forms.objects.all()
#     oform = None
#     form_ids = []
#     for form in forms:
#         if form.user_id == 0 and form.form_num == form_num:
#             oform = form
#         elif form.form_num == form_num:
#             if form.user_id != 0:
#                 form_ids.append(form.id)
#     for f_id in form_ids:
#         form.id = f_id
#         form.save()
# Create your models here.
