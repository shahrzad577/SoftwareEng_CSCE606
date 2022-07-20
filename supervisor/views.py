from django.shortcuts import render
from .models import SuperVisor, get_students
# from student.models import Student
def supervisor_view(request, spv_id):
    if request.user.username == "":
        return render(request, "anon.html")
    supervisor = SuperVisor.objects.get(id = spv_id)
    students = get_students(supervisor)
    context = {
        "supervisorName": supervisor.supervisor_name,
        "students": students,
    }
    return render(request, 'supervisor.html', context)
# Create your views here.
