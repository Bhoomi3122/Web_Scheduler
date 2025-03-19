from django.contrib.auth.models import User
from django.db import models

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"
