# Generated by Django 4.2.7 on 2023-11-12 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('mobile_no', models.CharField(blank=True, max_length=15, null=True)),
                ('email_id', models.CharField(max_length=30)),
                ('website', models.CharField(max_length=50)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('job_type', models.CharField(choices=[('Internship', 'Internship'), ('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time')], max_length=10)),
                ('slab', models.CharField(choices=[('1', 'First'), ('2', 'Second'), ('3', 'Third'), ('D', 'Dream')], max_length=10)),
                ('ctc', models.DecimalField(decimal_places=2, max_digits=5)),
                ('can_placed_students_apply', models.BooleanField()),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('application_deadline', models.DateTimeField()),
                ('maximum_backlogs', models.IntegerField(default=0)),
                ('maximum_active_backlogs', models.IntegerField(default=0)),
                ('min_gpa', models.FloatField()),
                ('eligible_departments', models.ManyToManyField(to='student.department')),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruiter.recruiter')),
            ],
        ),
    ]
