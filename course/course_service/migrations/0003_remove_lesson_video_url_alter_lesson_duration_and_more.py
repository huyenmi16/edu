# Generated by Django 5.0.7 on 2024-08-25 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_service', '0002_course_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='video_url',
        ),
        migrations.AlterField(
            model_name='lesson',
            name='duration',
            field=models.DurationField(help_text='Duration in HH:MM:SS format'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='type',
            field=models.CharField(choices=[('video', 'Video'), ('article', 'Article'), ('quiz', 'Quiz'), ('document', 'Document')], max_length=50),
        ),
    ]
