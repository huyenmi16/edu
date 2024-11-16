# Generated by Django 5.0.7 on 2024-09-09 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_service', '0003_quiz_is_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='is_completed',
        ),
        migrations.CreateModel(
            name='UserQuizCompletion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('is_completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz_service.quiz')),
            ],
        ),
    ]