from django import forms
from .models import Recruiter, Job

class RegisterRecruiterForm(forms.ModelForm):
    class Meta:
        model = Recruiter
        fields = (
            'name',
            'mobile_no',
            'email_id',
            'website'
        )

class AddJobForm(forms.ModelForm):
    class Meta:
        model = Job 
        fields = (
            'role',
            'description',
            'job_type',
            'ctc',
            'application_deadline',
            'maximum_backlogs',
            'maximum_active_backlogs',
            'min_gpa',
            'eligible_courses',
        )