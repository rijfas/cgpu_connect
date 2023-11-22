from django import forms
from .models import Recruiter

class RegisterRecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = (
            'name',
            'mobile_no',
            'email_id',
            'website'
        )