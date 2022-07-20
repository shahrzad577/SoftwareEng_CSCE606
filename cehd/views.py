from django.shortcuts import render
from django.http import HttpResponse
from forms.models import Forms
from programs.models import Programs
from supervisor.models import SuperVisor, get_students
from student.models import Student, generate_forms

from django.contrib.auth import get_user_model

def home_view(request):
    if request.user.username == "":
        return render(request, "anon.html")

    username = None

    username = request.user.username
    programs = Programs.objects.all()

    context = {
        "username": username,
        "programs": programs
    }

    #redirecting different users to different home page based on the user type
    if username == "supervisor1" or username == "supervisor2" or username == "supervisor3":
        return supervisor_home_view(request)
    elif username == "student1" or username == "student2" or username == "student3" or username == "student4" or username == "student5" or username == "student6":
        return student_home_view(request)
    elif username == "coordinator":
        return coordinator_view(request)
    return render(request, "home.html", context)


# Coordinator view generates all data - supervisor, student, program 
def coordinator_view(request):
    #It generates the home page for the coordinator
    if request.user.username == "":
        return render(request, "anon.html")
    programs = Programs.objects.all()
    students = Student.objects.all()
    supervisors = SuperVisor.objects.all()


    # ids = get_forms(program)
    # form = forms(ids)


    # for student in students:
    #     generate_forms(student)
    point = []
    data2 = []
    for st in students:
        point = [st.student_name, SuperVisor.objects.get(id=st.supervisor_id).supervisor_name, st.get_program()]
        data2.append(point)
    username = request.user.username
    context = {
        "data":data2,
        "programs":programs
    }
    return render(request, "coordinator_view.html", context)

def get_email(s_id):   
    #It retrieves the email address of the particular student from the data base
    User = get_user_model()
    users = User.objects.all()
    student = Student.objects.get(id = s_id)
    email = ""
    for user in users:
        if user.first_name == student.student_name:
            email = user.email
    return email

def supervisor_home_view(request):
    #It generates the home page for the supervisor
    if request.user.username == "":
        return render(request, "anon.html")
    first_name = request.user.first_name
    last_name = request.user.last_name
    if last_name == "":
        name = first_name
    else:
        name = first_name + " " + last_name
    supervisors = SuperVisor.objects.all()
    supervisor = None
    for sv in supervisors:
        if sv.supervisor_name == name:
            supervisor = sv
    
    students = get_students(supervisor)
    context = {
        "supervisorName": supervisor.supervisor_name,
        "students":students
    }
    return render(request, 'supervisor_home.html', context)
    

def student_home_view(request):
    #It generates the home page for the students
    if request.user.username == "":
        return render(request, "anon.html")
    first_name = request.user.first_name
    last_name = request.user.last_name
    if last_name == "":
        name = first_name
    else:
        name = first_name + " " + last_name
    # print(name)
    students = Student.objects.all()
    student = None
    for st in students:
        if st.student_name == name:
            student = st
    forms = Forms.objects.all()
    form_ids = student.get_student_forms()
    print(form_ids)
    form_data = []
    forms_data = []
    for id in form_ids:
        for form in forms:
            if form.user_id == student.id and form.form_num == id:
                forms_data.append(form)
    print(forms_data)
    program_name = Programs.objects.get(id=student.program_id).program_name
    # print(program_name)
    context = {
        'programName': program_name,
        'studentName': student.student_name,
        'forms': forms
    }
    context = {
        'programName': program_name,
        'student': student,
        'forms': forms_data
    }
    return render(request, "student_home.html", context)
