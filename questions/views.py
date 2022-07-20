from django.shortcuts import render
# from django.http import HttpResponse
from .models import Question

def questions_view(request, qid):
    if request.user.username == "":
        return render(request, "anon.html")
    question = Question.objects.get(id=qid)
    context = {
        "question_type": question.question_type,
        "question_content": question.question_content,
        "options_number": question.options_number
    }
    return render(request, "questions.html", context)
# Create your views here.
