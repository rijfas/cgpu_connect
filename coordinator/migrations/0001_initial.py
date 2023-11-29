# Generated by Django 4.2.7 on 2023-11-23 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('middle_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('mobile_no', models.CharField(blank=True, max_length=15, null=True)),
                ('email_id', models.CharField(max_length=30)),
            ],
        ),
    ]
