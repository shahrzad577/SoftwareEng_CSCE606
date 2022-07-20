from pickle import TRUE
from django.db import models

class Question(models.Model):
    question_type = models.IntegerField()
    question_content = models.TextField()
    question_answer = models.TextField()
    options_number = models.IntegerField()
    form_number = models.IntegerField()
    def are_options(self):
        if self.question_type == 1:
            return True
        else:
            return False

    def ret_question(self):
        return self.question_content
    
class feedbacks(models.Model):
    form_id = models.IntegerField()
    user_comment = models.CharField(max_length=30)

def clone_ques(qid, form_num):
   print("")
   question = Question.objects.get(id = qid)
   question.id = None
   question.form_number = form_num 
   question.save()

# Create your models here.
