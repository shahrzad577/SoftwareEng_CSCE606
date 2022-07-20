from asyncio import proactor_events
from django.shortcuts import render
from .models import Program_Coordinator
from supervisor.models import SuperVisor
from student.models import Student

def pc_view(request):
    if request.user.username == "":
        return render(request, "anon.html")
    #program_coordinator = Program_Coordinator.objects.get(id=1)
    program_coordinator = Program_Coordinator.objects.all()#(id=1)
    pcName=''
    for x in program_coordinator:
        pcName=program_coordinator.pc_name
    students = Student.objects.all()
    supervisors = SuperVisor.objects.all()
    context = {
        #'pcName': program_coordinator.pc_name,
        'pcName': pcName,
        'students': students,
        'supervisors': supervisors
    }
    return render(request, 'coordinator.html', context)
