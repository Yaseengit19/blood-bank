from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Donor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/Donor/',null=True,blank=True)
    bloodgroup=models.CharField(max_length=10)
    address = models.CharField(max_length=40)
    age = models.PositiveIntegerField(null=True, blank=True)  # Age of the donor
    mobile = models.CharField(max_length=20,null=False)
    weight = models.PositiveIntegerField(null=True, blank=True)  # Weight in kg
    has_health_issues = models.BooleanField(default=False)  # Health conditions
    last_donation_date = models.DateField(null=True, blank=True)  # Date of last donation

    def is_eligible(self):
        # Check age
        if self.age < 18 or self.age > 65:
            return False, "You must be between 18 and 65 years old to donate blood."

        # Check weight
        if self.weight < 50:
            return False, "You must weigh at least 50 kg to donate blood."

        # Check health conditions
        if self.has_health_issues:
            return False, "You are not eligible to donate blood due to health conditions."

        # Check last donation date
        if self.last_donation_date:
            days_since_last_donation = (date.today() - self.last_donation_date).days
            if days_since_last_donation < 56:
                return False, f"You must wait {56 - days_since_last_donation} more days before donating again."

        return True, "You are eligible to donate blood."
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class BloodDonate(models.Model): 
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE)   
    disease=models.CharField(max_length=100,default="Nothing")
    age=models.PositiveIntegerField()
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now=True)
    def __str__(self):
        return self.donor