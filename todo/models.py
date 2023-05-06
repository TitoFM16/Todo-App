from django.db import models
from django.utils import timezone

class Task(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_CHOICES = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField(default=timezone.now)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=MEDIUM)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
