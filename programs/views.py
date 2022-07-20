from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from forms.models import getnewformn
from forms.forms import FormsForm
from django.forms import HiddenInput

from .models import Programs, get_forms
from forms.models import Forms
from .forms import ProgramsForm
def forms(form_ids):
    forms = Forms.objects.all()
    returnVal = []
    for fids in form_ids:
        for form in forms:
            if form.form_num == fids and form.user_id == 0:
                returnVal.append(form)
    
    return returnVal

def program_view(request, my_id):
    if request.user.username == "":
        return render(request, "anon.html")
    program = Programs.objects.get(id=my_id)
    ids = get_forms(program)
    form = forms(ids)
    context = {
        'program': program,
        'forms': form
    }
    return render(request, "program.html", context)

def program_create_view(request):
    if request.user.username == "":
        return render(request, "anon.html")
    form = ProgramsForm(request.POST or None)
    if form.is_valid():
        form.save()
        # return HttpResponseRedirect(reverse('/'))
        return redirect('home')
    context = {
        'form': form
    }

    return render(request, "program_create.html", context)

def pform_create_view(request, program_id): 
    # print(initial_data)
    # print(program_id)
    if request.user.username == "":
        return render(request, "anon.html")
    initial_data = {
        'program_id': program_id,
        'form_num': getnewformn(),
        'user_id': 0 ,
        'completed_by_supervisor': False,
        'completed_by_coordinator': False
    }
    form = FormsForm(None, initial=initial_data)

    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "form_create.html", context)
# Create your views here.
