# Generated by Django 4.2.7 on 2023-11-29 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0005_shortlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortlist',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
    ]