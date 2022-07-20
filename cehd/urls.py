"""cehd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import home_view, coordinator_view
from questions.views import questions_view
from forms.views import student_form_view, forms_view, form_create_view, generate_pdf, generate_pdf2 #edit_question_view #,create_form
from programs.views import program_view, program_create_view, pform_create_view
from student.views import student_view
from supervisor.views import supervisor_view
from program_coordinator.views import pc_view
from django.views.generic.base import TemplateView # new
# from form_creator.views import create_form

urlpatterns = [
    path('accounts/login/home', home_view,name='home'),
    #path('home/', home_view),
    path('admin/', admin.site.urls),
    path('question/<int:qid>', questions_view, name='question'),
    #path('forms/', forms_view),
    #path('create/', create_form),
    path('create_form/', form_create_view, name='create_form'),
    path('create_program/', program_create_view, name='create_program'),
    path('form/<int:form_id>', forms_view, name='form_view'),
    path('program/<int:my_id>', program_view, name='program_view'),
    path('student/<int:stu_id>', student_view, name='student_view'),
    path('supervisor/<int:spv_id>', supervisor_view, name='supervisor_view'),
    path('program_coordinator', pc_view, name='program_coordinator'),
    path("accounts/", include("django.contrib.auth.urls")),  # new
    path('', TemplateView.as_view(template_name='initial_page.html'), name='initial_page'), # new),
    path('test', coordinator_view),
    path('form/<int:student_id>/<int:form_id>', student_form_view, name='student_form_view'),
    path('create_form/<int:program_id>', pform_create_view, name='program_create_form'),
    # path('edit/<int:qid>', edit_question_view, name="edit_question_view"),
    path('form/generate_pdf/<int:form_id>', generate_pdf, name='pdf'),
    path('form/<int:student_id>/generate_pdf/<int:form_id>', generate_pdf2, name='pdf'),
]