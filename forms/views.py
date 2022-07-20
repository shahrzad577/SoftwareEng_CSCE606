from argparse import RawDescriptionHelpFormatter
from multiprocessing import context
from urllib import request
from django.shortcuts import render
from .models import Forms, get_questions, get_questions2, clone_form, getnewformn
from questions.models import Question, feedbacks
from .forms import FormsForm, RawFormsForm
from .utils import render_to_pdf
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from student.models import Student, generate_form, generate_form2
from programs.models import Programs
from django.contrib import messages
from django.shortcuts import redirect
from cehd.views import get_email
from datetime import timezone
import datetime

# from program_coordinator.models import update_form
# Create your views here.


def questions(question_ids):
    #retirive all the question objects given the question ids
    returnVal = []
    for question_id in question_ids:
        returnVal.append(Question.objects.get(id=question_id))
    return returnVal

def increase_order(form_id, order):
    #increase the ordering of all the questions by 1 in case of update. If any question gets into order 2, all questions starting from order 2 will be increased by 1 in their order
    #form_id is the id of the form that will be updated and order is the order number where the new question was added    
    questions = Question.objects.all()
    for x in questions:
        if x.form_number == form_id and x.options_number >= order:
            x.options_number = x.options_number + 1
            x.save()
            # Question.objects.filter(form_number=x.form_number, id=x.id).update(options_number=x.options_number)

def decrease_order(form_id, order):
    #decrease the ordering of the other questions if we delete any question. If we delete any element from 2nd order, all the questions from 2nd order will be moved back by one poistion
    #form id is the id of the form which will be updated. Order is the order number where the question was deleted
    questions = Question.objects.all()
    for x in questions:
        if x.form_number == form_id and x.options_number > order:
            x.options_number = x.options_number - 1
            x.save()
            # Question.objects.filter(form_number=x.form_number, id=x.id).update(options_number=x.options_number)


#increases order of everything below the edited question if order is changed 
def edit_increase(form_id, order, question_id, prev_order):
     
     questions = Question.objects.all()
     questions = Question.objects.filter(form_number = form_id).exclude(id = question_id)

     for x in questions:
         if x.form_number == form_id and x.id != question_id and x.options_number > prev_order:
             # print("X-ID: ", x.id)
             # print("Q-ID: ", question_id)
             x.options_number = x.options_number - 1
             x.save()

     for x in questions:
         if x.form_number == form_id and x.id != question_id and x.options_number >= order:
             # print("X-ID: ", x.id)
             # print("Q-ID: ", question_id)
             x.options_number = x.options_number + 1
             x.save()
      

def student_form_view(request, student_id, form_id):
    if request.user.username == "":
        return render(request, "anon.html")
    forms = Forms.objects.all()
    output_id = 0
    for form in forms:
        if form.user_id == student_id and form.form_num == form_id:
            output_id = form.id
    # print(output_id)
    # print("2nd")
    if output_id == 0:
        return render(request, "form_not_avail.html")
    else:
        return forms_view(request, output_id)

def get_form(form_num, studentid = 0):
    form = None
    forms = Forms.objects.all()
    for f in form:
        if f.form_num == form_num and f.user_id == studentid:
            form = f
    return f.id

isEdit = 0
id_for_edit = -1

def forms_view(request, form_id):
    if request.user.username == "":
        return render(request, "anon.html")
    students = Student.objects.all()
    forms = Forms.objects.all()
    form = None
    # for f in forms:
    #     if f.user_id == 0 and f.form_num == form_id:
    #         form = f
    form = Forms.objects.get(id=form_id)

    global isEdit # checks if user has clicked on edit
    global id_for_edit # ID of the question that is to be edited 

    formnum = form.form_num
    completed_by_coordinator=0
    # To access the email of the student associated with form use get_email(form.user_id)
    if form.completed_by_coordinator==True:
        completed_by_coordinator=1
    else:
        completed_by_coordinator=0

    completed_by_supervisor = 0
    if form.completed_by_supervisor == True:
        completed_by_supervisor = 1
    else:
        completed_by_supervisor = 0
    program_id = form.program_id
    ids = get_questions2(form)
    #######update_final
    if form.completed_by_coordinator == False and 'supervisor' in request.user.username:
        return render(request, "page_not_avail.html")
    elif form.completed_by_supervisor == False  and 'student' in request.user.username:
        return render(request, "page_not_avail.html")
    how_many_questions=len(ids)+1
    #isEdit = 0
    editQuestion = None
    # print("ProgramID:")
    # print(program_id)
    splitStr = None
    type=0#0 for no question to add, 1 for normal question to add and 2 for mcq to add
    username = request.user.username
    user_access=1
    if 'supervisor' in username:
        user_access=2
    elif 'student' in username:
        user_access=3
    #user accesss=1 for coordinator, 2 for supervisor and 3 for student

    if request.method == 'POST':
        if request.POST.get("question_type"):
            #which question type is selected, MCQ or Normal
            question_type=request.POST.get("question_type")

            if question_type=="Normal":
                type=0
            elif question_type=="MCQ":
                if request.POST.get("how_many"):
                    how_many_MCQ = request.POST.get("how_many")
                    type=int(how_many_MCQ)


        if request.POST.get('normalquestion'):
            question=request.POST.get('normalquestion')
            order = how_many_questions#+1  # last position to add, by default it will be added to the last position

            is_update=0
            old_id=-1
            # if '%' in question:
            if isEdit == 1:

                is_update=1
                isEdit = 0


            if request.POST.get('order'):
                order = request.POST.get('order')
                if order== 'Order:':
                    order = how_many_questions  # +1
                else:
                    order = int(order)
            # change order of other elements

            if is_update==1:

                prev_order = Question.objects.get(id = id_for_edit).options_number
            


                if request.method == 'POST' and 'order' in request.POST and request.POST.get('order') != "Order:":

                    order = int(request.POST.get('order')) # grabs order by selected value and updates to that position

                    Question.objects.filter(id=id_for_edit).update(question_content=question, options_number=order)
                    edit_increase(form.id, order, id_for_edit, prev_order)

                Question.objects.filter(id=id_for_edit).update(question_content=question)
                
            else:

                increase_order(form.id, order)
                how_many_questions=how_many_questions+1
                art = Question.objects.create(question_type=type, question_content=question, options_number=order,
                                            form_number=form.id)
                # isEdit = 0
        elif request.POST.get('MCQquestion'):
            question=request.POST.get('MCQquestion')
            options=[]
            for i in range(10):
                i=str(i)
                if request.POST.get(i):
                    question=question+'!!'+request.POST.get(i)
                else:
                    break
            order = how_many_questions#+1  # last position to add, by default it will be added to the last position


            is_update=0
            if isEdit == 1:

                # print("IS-EDIT: ", isEdit)
                # print("IDS: " , id_for_edit)
                is_update=1
  
                isEdit = 0


            if request.POST.get('order'):
                order = request.POST.get('order')
                if order== 'Order:':
                    order = how_many_questions  # +1
                else:
                    order = int(order)
            #change order of other elements

            if is_update==1:
                prev_order = Question.objects.get(id = id_for_edit).options_number
    
                print("ORDER: ", request.POST.get('order'))
                if request.method == 'POST' and 'order' in request.POST and request.POST.get('order') != "Order:":
                    # string_value = request.POST.get('order')
                    order = int(request.POST.get('order'))
                    print("Order: ", order)
                    Question.objects.filter(id=id_for_edit).update(question_content=question, options_number=order)
                    edit_increase(form.id, order, id_for_edit, prev_order)
                Question.objects.filter(id=id_for_edit).update(question_content=question)
                
          
            else:
                print("THIS IS A TEST ON LINE 211")

                increase_order(form.id, order)
                how_many_questions=how_many_questions+1
                art = Question.objects.create(question_type=type, question_content=question, options_number=order,
                                            form_number=form.id)

                                # form_number=form.id)
        if request.POST.get('DeleteButton'):
            ids = request.POST.get('DeleteButton')
            delete_element=Question.objects.get(form_number=form.id, id=ids)
            decrease_order(form.id, delete_element.options_number)

            how_many_questions=how_many_questions-1
            Question.objects.filter(form_number=form.id, id=request.POST.get('DeleteButton')).delete()

        if request.POST.get('EditButton'):
            isEdit = 1
            ids = request.POST.get('EditButton')
            id_for_edit = ids
            obj = Question.objects.get(id=ids)
            string = obj.question_content.split("!!")
            # print(string)
            editQuestion = string[0]
            type = 0
            del string[0]
            if "!!" in obj.question_content:  # check if question is MCQ
                editOptions = (obj.question_content).count("!!")
                splitStr = {x.replace('Option', '') for x in string}
                ids = [i for i in range(editOptions)]
                # print(splitStr)
                # print(ids)
                splitStr = zip(splitStr, ids)
                type = editOptions
   

        if request.POST.get("Finalize Form"):
            temp_form = Forms.objects.get(id=form_id)
            if temp_form.completed_by_coordinator == False:
                Forms.objects.filter(id=form_id).update(completed_by_coordinator=True,
                                                        time_completed_by_coordinator=datetime.datetime.now())
                messages.add_message(request, messages.INFO, 'You have finalized the form')
                st = []
                for student in students:
                    if student.program_id == program_id:
                        st.append(student)
                for s in st:
                    generate_form2(s.id, Forms.objects.get(id=form_id).form_num)
            else:
                messages.add_message(request, messages.INFO, 'You can not edit the form')

            
            
        if request.POST.get("Finalize Answer"):
            print('hii')
            temp_form = Forms.objects.get(id=form_id)
            if temp_form.completed_by_supervisor == False:
                Forms.objects.filter(id=form_id).update(completed_by_supervisor=True,
                                                        time_completed_by_supervisor=datetime.datetime.now())
                messages.add_message(request, messages.INFO, 'You have completed the form')
            else:
                messages.add_message(request, messages.INFO, 'You can not edit the form anymore')

            email(get_email(form.user_id))


        if request.POST.get("Clone Form"):
            # print(form_id)
            return redirect('/form/' + str(clone_form(formnum)))
            # print(form_id)
            # forms_view(request, form_id)
        if request.POST.get("Submit Feedback"):
            feedback=request.POST.get("Feedback")
            print(feedback)

            feedbacks.objects.filter(form_id=form_id).delete()
            art = feedbacks.objects.create(form_id=form_id,user_comment=feedback) #type=-1 for feedback
            Forms.objects.filter(id=form_id).update(completed_by_student=True,
                                                    time_completed_by_student=datetime.datetime.now())
            messages.add_message(request, messages.INFO, 'Your feedback is submitted')
    questions = Question.objects.filter(form_number=form.id).order_by('options_number')
    processed_questions=[]
    ids,orders,options,types,answers=[],[],[],[],[]
    for x in questions:
        if request.POST.get(str(x.id)+"_answer"):
            answer=request.POST.get(str(x.id) + "_answer")
            Question.objects.filter(id=x.id).update(question_answer=answer)

    for x in questions:

        if "!!" not in x.question_content:
            processed_questions.append(x.question_content)
            options.append([])
            types.append('normal')

        else:
            strings=x.question_content.split("!!")
            question=strings[0]+f"\n"
            mcqoption = []
            for i in range(1, len(strings)):
                mcqoption.append(strings[i])
            options.append(mcqoption)
            processed_questions.append(question)
            types.append('mcq')
        ids.append(x.id)
        orders.append(x.options_number)
        answers.append(x.question_answer)

    a=[i for i in range(1,10)]#21
    mylist = zip(processed_questions, ids,orders,options,types,answers)
    feedback=""
    if feedbacks.objects.filter(form_id=form.id).exists():
        feedback=feedbacks.objects.filter(form_id=form.id)[0]
        feedback=feedback.user_comment

    # print(form_id)
    form = Forms.objects.get(id=form_id)
    completed_by_coordinator = 0
    if form.completed_by_coordinator == True:
        completed_by_coordinator = 1
    else:
        completed_by_coordinator = 0

    completed_by_supervisor = 0
    if form.completed_by_supervisor == True:
        completed_by_supervisor = 1
    else:
        completed_by_supervisor = 0
    if isEdit == 1:
        how_many_questions=how_many_questions-1
    feedback_exists=0
    if feedbacks.objects.filter(form_id=form.id).exists():
        feedback_exists=1
        feedback=feedbacks.objects.filter(form_id=form.id)[0]
        feedback=feedback.user_comment


    context = {
        "user_access":user_access,
        "form_id": form_id,
        "articles": mylist,
        "lists":['MCQ','Normal'],
        "lists2":a,
        "type":type,
        "n":range(type),
        "editQuestion": editQuestion,
        "editOptions": splitStr,
        "isEdit": isEdit,
        "available_positions":range(1,how_many_questions+1),
        "feedback":feedback,
        "completed_by_coordinator":completed_by_coordinator,
        "completed_by_supervisor": completed_by_supervisor,
        "feedback_exists":feedback_exists,
    }
    #print(maps)
    return render(request,'create_form.html',context=context)
    # return render(request, "forms.html", context)


def form_create_view(request):
    # print(initial_data)
    if request.user.username == "":
        return render(request, "anon.html")
    initial_data = {
        'form_num': getnewformn(),
        'user_id': 0 ,
        'completed_by_supervisor': False,
        'completed_by_coordinator': False
    }


    
    form = FormsForm(request.POST or None, initial=initial_data)
    # if (True):
    #     print(form.cleaned_data['form_num'])
    if form.is_valid():
        form.save()
        return redirect('home')
    
    context = {
        'form': form
    }
    return render(request, "form_create.html", context)
    
def generate_pdf(request, form_id):
    #generate the pdf of the form given the form id
    if request.user.username == "":
        return render(request, "anon.html")
    username = request.user.username
    user_access = 1
    if 'supervisor' in username:
        user_access = 2
    elif 'student' in username:
        user_access = 3
    questions = Question.objects.filter(form_number=form_id).order_by('options_number')
    processed_questions = []
    ids, orders, options, types, answers = [], [], [], [], []
    for x in questions:
        if request.POST.get(str(x.id) + "_answer"):
            answer = request.POST.get(str(x.id) + "_answer")
            Question.objects.filter(id=x.id).update(question_answer=answer)

    for x in questions:

        if "!!" not in x.question_content:
            processed_questions.append(x.question_content)
            options.append([])
            types.append('normal')

        else:
            strings = x.question_content.split("!!")
            question = strings[0] + f"\n"
            mcqoption = []
            for i in range(1, len(strings)):
                mcqoption.append(strings[i])
            options.append(mcqoption)
            processed_questions.append(question)
            types.append('mcq')
        ids.append(x.id)
        orders.append(x.options_number)
        answers.append(x.question_answer)


    mylist = zip(processed_questions, ids, orders, options, types, answers)

    form = Forms.objects.get(id=form_id)
    completed_by_coordinator = 0
    if form.completed_by_coordinator == True:
        completed_by_coordinator = 1
    else:
        completed_by_coordinator = 0

    completed_by_supervisor = 0
    if form.completed_by_supervisor == True:
        completed_by_supervisor = 1
    else:
        completed_by_supervisor = 0
    feedback = ""
    is_feedback=0
    if feedbacks.objects.filter(form_id=form_id).exists():
        feedback = feedbacks.objects.filter(form_id=form_id)[0]
        feedback = feedback.user_comment
        is_feedback=1
    context = {
        "user_access": user_access,
        "form_id": form_id,
        "articles": mylist,
        "completed_by_coordinator": completed_by_coordinator,
        "completed_by_supervisor": completed_by_supervisor,
        "feedback":feedback,
        "is_feedback":is_feedback,
    }
    return render_to_pdf('generate_pdf.html', context)

    #return HttpResponse(pdf, content_type='application/pdf')
def generate_pdf2(request, student_id, form_id):
    #generetae the pdf of the form given the form id
    if request.user.username == "":
        return render(request, "anon.html")
    username = request.user.username
    user_access = 1
    if 'supervisor' in username:
        user_access = 2
    elif 'student' in username:
        user_access = 3
    questions = Question.objects.filter(form_number=form_id).order_by('options_number')
    processed_questions = []
    ids, orders, options, types, answers = [], [], [], [], []
    for x in questions:
        if request.POST.get(str(x.id) + "_answer"):
            answer = request.POST.get(str(x.id) + "_answer")
            Question.objects.filter(id=x.id).update(question_answer=answer)

    for x in questions:

        if "!!" not in x.question_content:
            processed_questions.append(x.question_content)
            options.append([])
            types.append('normal')

        else:
            strings = x.question_content.split("!!")
            question = strings[0] + f"\n"
            mcqoption = []
            for i in range(1, len(strings)):
                mcqoption.append(strings[i])
            options.append(mcqoption)
            processed_questions.append(question)
            types.append('mcq')
        ids.append(x.id)
        orders.append(x.options_number)
        answers.append(x.question_answer)

    mylist = zip(processed_questions, ids, orders, options, types, answers)
    form = Forms.objects.get(id=form_id)
    completed_by_coordinator = 0
    if form.completed_by_coordinator == True:
        completed_by_coordinator = 1
    else:
        completed_by_coordinator = 0

    completed_by_supervisor = 0
    if form.completed_by_supervisor == True:
        completed_by_supervisor = 1
    else:
        completed_by_supervisor = 0
    feedback = ""
    is_feedback = 0
    if feedbacks.objects.filter(form_id=form_id).exists():
        feedback = feedbacks.objects.filter(form_id=form_id)[0]
        feedback = feedback.user_comment
        is_feedback = 1
    context = {
        "user_access": user_access,
        "form_id": form_id,
        "articles": mylist,
        "completed_by_coordinator": completed_by_coordinator,
        "completed_by_supervisor": completed_by_supervisor,
        "feedback": feedback,
        "is_feedback": is_feedback,
    }
    return render_to_pdf('generate_pdf.html', context)

def email(email_address):
    #send an email to the given email address of the student if the form for that student is completed by the supervisor
    subject="This is a message from CEHD"
    receipient='Aman'
    message=f'Hi {receipient}, Your supervisor has completed a form for you. '
    email_from=settings.EMAIL_HOST_USER
    receipient_list = [email_address,]
    send_mail(subject,message, email_from,receipient_list)
    #print('hi')
    return

