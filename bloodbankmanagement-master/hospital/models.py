from django.db import models
from django.contrib.auth.models import User

class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

class BloodRequest(models.Model):
    URGENCY_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    request_by_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True)
    blood_group = models.CharField(max_length=5)  # e.g., A+, O-, etc.
    unit = models.PositiveIntegerField()
    request_date = models.DateTimeField(auto_now_add=True)
    is_emergency = models.BooleanField(default=False)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_LEVEL_CHOICES, default='Low')
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Fulfilled', 'Fulfilled'),
        ('Cancelled', 'Cancelled'),
    ], default='Pending')

    def __str__(self):
        return f"{self.bloodgroup} - {self.unit} units (Urgency: {self.urgency_level})"
