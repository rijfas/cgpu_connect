from django import forms
from .models import Student

class RegisterStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'dob',
            'height',
            'sex',
            'weight',
            'category',
            'religion',
            'guardian_name',
            'guardian_occupation',
            'permenant_address',
            'communication_address',
            'mobile_no',
            'email_id',
            'department',
            'course',
            'entrance_type',
            'entrance_rank',
            'year_of_pass',
            'admission_number',
            'ktu_id',
            'pending_arrears',
            'cleared_arrears',
        )