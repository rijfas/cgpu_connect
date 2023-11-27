from django.db import models
from core.models import Account


SEX_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

CATEGORY_CHOICES = (
    ('General', 'General'),
    ('OBC', 'OBC'),
    ('SC/ST', 'SC/ST'),
    ('Physically Handicaped', 'Physically Handicaped'),
    ('Foreign Nationals', 'Foreign Nationals'),
)

RELEGION_CHOICES = (
    ('Hindu', 'Hindu'),
    ('Christian', 'Christian'),
    ('Islam', 'Islam'),
)

LANGUAGE_CHOICES = (
    ('en', 'English'),
    ('zh', 'Chinese (Mandarin)'),
    ('es', 'Spanish'),
    ('hi', 'Hindi'),
    ('ar', 'Arabic'),
    ('bn', 'Bengali'),
    ('ru', 'Russian'),
    ('pt', 'Portuguese'),
    ('ja', 'Japanese'),
    ('pa', 'Punjabi'),
    ('de', 'German'),
    ('te', 'Telugu'),
    ('mr', 'Marathi'),
    ('fr', 'French'),
    ('vi', 'Vietnamese'),
    ('ko', 'Korean'),
    ('ta', 'Tamil'),
    ('ma', 'Malayalam'),
    ('ur', 'Urdu'),
)

TYPE_OF_EDUCATION_CHOICES = (
    ('HSC', 'High School'),
    ('SSC', 'Secondary School'),
    ('UG', 'Undergraduate'),
    ('PG', 'Postgraduate'),
)

ENTRANCE_TYPE_CHOICES = (
    ('KEAM', 'KEAM'),
    ('LBS', 'LBS MCA Entrance'),
    ('LET', 'LET')
)

SEMESTER_CHOICES = (
    ('1', 'First',),
    ('2', 'Second',),
    ('3', 'Third',),
    ('4', 'Fourth',),
    ('5', 'Fifth',),
    ('6', 'Sixth',),
    ('7', 'Seventh'),
    ('8', 'Eighth',),
    ('9', 'Ninth',),
    ('10', 'Tenth',),
    ('11', 'Eleventh',),
    ('12', 'Twelfth',),
)

STREAM_CHOICE = (
    ('BTECH', 'B.Tech'),
    ('MTECH', 'M.Tech'),
    ('MBA', 'MBA'),
    ('MCA', 'MCA'),
)


class Course(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    stream = models.CharField(max_length=10, choices=STREAM_CHOICE)
    course = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.stream} {self.course}'

class Student(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    dob = models.DateField()
    height = models.IntegerField(null=True, blank=True)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES)
    weight = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES)
    religion = models.CharField(max_length=20, choices=RELEGION_CHOICES)
    guardian_name = models.CharField(max_length=150, null=True, blank=True)
    guardian_occupation = models.CharField(max_length=150, null=True, blank=True)
    permenant_address = models.TextField()
    communication_address = models.TextField()
    mobile_no = models.CharField(max_length=12)
    email_id = models.CharField(max_length=150)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    entrance_type = models.CharField(max_length=50, null=True, blank=True, choices=ENTRANCE_TYPE_CHOICES)
    entrance_rank = models.IntegerField(null=True,blank=True)
    year_of_pass = models.IntegerField()
    admission_number = models.IntegerField()
    ktu_id = models.CharField(max_length=50)
    pending_arrears = models.IntegerField(default=0)
    cleared_arrears = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.first_name}'
    

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    gpa = models.DecimalField(max_digits=5, decimal_places=3)
    is_failed = models.BooleanField(default=False)

    def __str__(self):
        return f'result of {self.student} of {self.semester} : {self.gpa}'

class AcademicQualification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type_of_education = models.CharField(max_length=50, choices=TYPE_OF_EDUCATION_CHOICES)
    board = models.CharField(max_length=150)
    year_of_pass = models.IntegerField()
    grade = models.DecimalField(max_digits=7, decimal_places=3)
    institution = models.CharField(max_length=150)

    def __str__(self):
        return f'qualififcation of {self.student} of {self.type_of_education} : {self.grade}'


class Department(models.Model):
    name = models.CharField(max_length=150)

    def courses(self):
        return Course.objects.filter(department=self).count()
    
    def students(self):
        return Student.objects.filter(department=self).count()
    
    def __str__(self):
        return self.name
    
