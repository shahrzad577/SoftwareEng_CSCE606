from django.shortcuts import render
from .models import Student, generate_forms
from programs.models import Programs

def student_view(request, stu_id):
    if request.user.username == "":
        return render(request, "anon.html")
    student = Student.objects.get(id=stu_id)
    generate_forms(student)
    forms = student.get_student_forms()
    program_name = Programs.objects.get(id=student.program_id).program_name
    context = {
        'programName': program_name,
        'studentName': student.student_name,
        'forms': forms
    }
    return render(request, "student.html", context)
# Create your views here.
