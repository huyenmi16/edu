# Generated by Django 5.0.7 on 2024-08-25 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_service', '0003_remove_lesson_video_url_alter_lesson_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='duration',
            field=models.DurationField(help_text='Duration in HH:MM:SS format'),
        ),
    ]
