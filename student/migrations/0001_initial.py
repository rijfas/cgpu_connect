# Generated by Django 4.2.7 on 2023-11-12 04:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('stream', models.CharField(choices=[('BTECH', 'B.Tech'), ('MTECH', 'M.Tech'), ('MBA', 'MBA'), ('MCA', 'MCA')], max_length=10)),
                ('course', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('middle_name', models.CharField(blank=True, max_length=150, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('dob', models.DateField()),
                ('height', models.IntegerField(blank=True, null=True)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=20)),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('category', models.CharField(choices=[('General', 'General'), ('OBC', 'OBC'), ('SC/ST', 'SC/ST'), ('Physically Handicaped', 'Physically Handicaped'), ('Foreign Nationals', 'Foreign Nationals')], max_length=25)),
                ('religion', models.CharField(choices=[('en', 'English'), ('zh', 'Chinese (Mandarin)'), ('es', 'Spanish'), ('hi', 'Hindi'), ('ar', 'Arabic'), ('bn', 'Bengali'), ('ru', 'Russian'), ('pt', 'Portuguese'), ('ja', 'Japanese'), ('pa', 'Punjabi'), ('de', 'German'), ('te', 'Telugu'), ('mr', 'Marathi'), ('fr', 'French'), ('vi', 'Vietnamese'), ('ko', 'Korean'), ('ta', 'Tamil'), ('ma', 'Malayalam'), ('ur', 'Urdu')], max_length=20)),
                ('guardian_name', models.CharField(max_length=150)),
                ('guardian_occupation', models.CharField(max_length=150)),
                ('permenant_address', models.TextField()),
                ('communication_address', models.TextField()),
                ('mobile_no', models.CharField(max_length=12)),
                ('email_id', models.CharField(max_length=150)),
                ('entrance_type', models.CharField(blank=True, choices=[('KEAM', 'KEAM'), ('LBS', 'LBS MCA Entrance'), ('LET', 'LET')], max_length=50, null=True)),
                ('entrance_rank', models.IntegerField(blank=True, null=True)),
                ('year_of_pass', models.IntegerField()),
                ('admission_number', models.IntegerField()),
                ('ktu_id', models.CharField(max_length=50)),
                ('pending_arrears', models.IntegerField(default=0)),
                ('cleared_arrears', models.IntegerField(default=0)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.department')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('4', 'Fourth'), ('5', 'Fifth'), ('6', 'Sixth'), ('7', 'Seventh'), ('8', 'Eighth'), ('9', 'Ninth'), ('10', 'Tenth'), ('11', 'Eleventh'), ('12', 'Twelfth')], max_length=10)),
                ('gpa', models.DecimalField(decimal_places=3, max_digits=5)),
                ('is_failed', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentprofile')),
            ],
        ),
        migrations.CreateModel(
            name='AcademicQualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_education', models.CharField(choices=[('HSC', 'High School'), ('SSC', 'Secondary School'), ('UG', 'Undergraduate'), ('PG', 'Postgraduate')], max_length=50)),
                ('board', models.CharField(max_length=150)),
                ('year_of_pass', models.IntegerField()),
                ('grade', models.DecimalField(decimal_places=3, max_digits=7)),
                ('institution', models.CharField(max_length=150)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.studentprofile')),
            ],
        ),
    ]
