# Generated by Django 4.2.7 on 2023-12-01 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0002_shortlist_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlist',
            name='recruiter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recruiter.recruiter'),
            preserve_default=False,
        ),
    ]
