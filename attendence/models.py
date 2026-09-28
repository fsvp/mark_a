from django.db import models
from django.contrib.auth.models import User


class Attendance(models.Model):

    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    note = models.CharField(
        max_length=300,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"