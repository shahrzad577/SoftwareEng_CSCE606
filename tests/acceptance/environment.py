import inspect
import importlib
import coverage


# Reload modules after Coverage begins: https://behave-django.readthedocs.io/en/latest/testcoverage.html

def reload_modules():
  import cehd
  import forms
  import program_coordinator
  import programs 
  import questions
  import student 
  import supervisor

  for app in [cehd, forms, program_coordinator, programs, questions, student, supervisor]:
      members = inspect.getmembers(app)
      modules = map(
          lambda keyval: keyval[1],
          filter(lambda keyval: inspect.ismodule(keyval[1]), members),
      )
      for module in modules:
          try:
              importlib.reload(module)
          except:
              continue

def before_all(context):
    context.fixtures = ['tests/fixtures/initial-fixture.json']
    cov = coverage.Coverage()
    cov.start()
    context.cov = cov

    reload_modules()

def before_scenario(context, scenario):
    if scenario.name == 'Program Coordinator can create a form from form view':
        context.fixtures = ['tests/fixtures/2-fixture.json']
    elif scenario.name == 'Program Coordinator can add a multiple choice question':
        context.fixtures = ['tests/fixtures/5-fixture.json']
    elif scenario.name == 'Program Coordinator can edit a normal question':
        context.fixtures = ['tests/fixtures/6-fixture.json']
    elif scenario.name == 'Program Coordinator can edit a multiple choice question':
        context.fixtures = ['tests/fixtures/7-fixture.json']
    elif scenario.name == 'Program Coordinator can delete a normal question':
        context.fixtures = ['tests/fixtures/8-fixture.json']
    elif scenario.name == 'Program Coordinator can delete a multiple choice question':
        context.fixtures = ['tests/fixtures/8-fixture.json']
    elif scenario.name == 'Program Coordinator can change the order of any question':
        context.fixtures = ['tests/fixtures/8-fixture.json']
    elif scenario.name == 'Program Coordinator can finalize the form':
        context.fixtures = ['tests/fixtures/9-fixture.json']
    elif scenario.name == 'Program Coordinator can generate a PDF of the form':
        context.fixtures = ['tests/fixtures/10-fixture.json']
    elif scenario.name == 'Program Coordinator can clone the form':
        context.fixtures = ['tests/fixtures/10-fixture.json']
    elif scenario.name == 'Supervisor can answer questions to a form that program coordinator has finalized':
        context.fixtures = ['tests/fixtures/11-fixture.json']
    elif scenario.name == 'Student can submit feedback to form that supervisor and coordinator has finalized':
        context.fixtures = ['tests/fixtures/12-fixture.json']


# Save Code Coverage to ./cov
def after_all(context):
    cov = context.cov
    cov.stop()
    cov.save()
    cov.html_report(directory="./cov")