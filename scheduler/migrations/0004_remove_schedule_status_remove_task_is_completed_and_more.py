# Generated by Django 5.0.7 on 2025-02-01 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_remove_schedule_is_completed_schedule_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='status',
        ),
        migrations.RemoveField(
            model_name='task',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='schedule',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
