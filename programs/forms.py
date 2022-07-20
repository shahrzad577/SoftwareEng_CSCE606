from django import forms

from .models import Programs

class ProgramsForm(forms.ModelForm):
    class Meta:
        model = Programs
        fields = [
            'program_name'
        ]