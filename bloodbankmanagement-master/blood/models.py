from django.db import models
from patient import models as pmodels
from donor import models as dmodels
from hospital import models as hmodels
from hospital.models import Hospital
from donor.models import Donor
from donor.models import Donor
from patient.models import Patient

class Stock(models.Model):
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.bloodgroup

class BloodRequest(models.Model):
    URGENCY_LEVEL_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    request_by_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, blank=True, related_name='blood_requests')
    request_by_patient=models.ForeignKey(pmodels.Patient,null=True,on_delete=models.CASCADE)
    request_by_donor=models.ForeignKey(dmodels.Donor,null=True,on_delete=models.CASCADE)
    patient_name=models.CharField(max_length=30)
    # patient_age=models.PositiveIntegerField(null=True ,blank=True)
    reason=models.CharField(max_length=500)
    bloodgroup=models.CharField(max_length=10)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_LEVEL_CHOICES, default='Low')  # Urgency level
    last_date = models.DateField(null=True, blank=True)  # Last date for the request
    unit=models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ], default='Pending')  # Status o
    is_emergency = models.BooleanField(default=False)
    date=models.DateField(auto_now=True)
    def __str__(self):
        return self.bloodgroup

class DonationSchedule(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donation_schedules')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='donation_schedules')
    donation_date = models.DateField()  # Date scheduled for donation
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Status of the donation
    created_at = models.DateTimeField(auto_now_add=True)  # Date the schedule was created

    def __str__(self):
        return f"{self.donor.user.username} - {self.hospital.name} - {self.donation_date}"
        
# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     message = models.CharField(max_length=255)
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.message
    
class DonationRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='donation_requests')
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donation_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    request_date = models.DateTimeField(auto_now_add=True)  # Date the request was made

    def __str__(self):
        return f"Request from {self.patient.user.username} to {self.donor.user.username}"