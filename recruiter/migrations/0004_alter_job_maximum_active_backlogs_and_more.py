# Generated by Django 4.2.7 on 2023-11-26 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0003_remove_job_eligible_departments_job_eligible_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='maximum_active_backlogs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='maximum_backlogs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='min_gpa',
            field=models.FloatField(blank=True, null=True),
        ),
    ]