from django import forms

from .models import Forms
from datetime import timezone
class FormsForm(forms.ModelForm):

    class Meta:
        model = Forms
        fields = [
            'form_name',
            'program_id',
            'user_id',
            'completed_by_supervisor',
            'completed_by_coordinator',
            'completed_by_student',
            'form_num',
            'time_completed_by_coordinator',
            'time_completed_by_supervisor',
            'time_completed_by_student',
        ]
        widgets = {

            # Hide inputs as the user does not need to see these - the code automatically supplies these 
            
            'user_id': forms.HiddenInput(),
            'form_num': forms.HiddenInput(),
            'completed_by_coordinator': forms.HiddenInput(),
            'completed_by_supervisor': forms.HiddenInput(),
            'completed_by_student': forms.HiddenInput(),
            'time_completed_by_coordinator': forms.HiddenInput(),
            'time_completed_by_supervisor': forms.HiddenInput(),
            'time_completed_by_student': forms.HiddenInput()
        }


class RawFormsForm(forms.Form):
    form_name = forms.CharField()
