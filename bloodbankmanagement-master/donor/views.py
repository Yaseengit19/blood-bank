from django.shortcuts import render,redirect,reverse,get_object_or_404
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels
from .models import Donor
from .forms import DonorForm,UpdateUsernameForm, UpdatePasswordForm,DonorEligibilityForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from blood.forms import DonationScheduleForm
from .models import Donor
from blood.models import DonationSchedule 
from blood.models import DonationRequest



def donor_signup_view(request):
    userForm=forms.DonorUserForm()
    donorForm=forms.DonorForm()
    mydict={'userForm':userForm,'donorForm':donorForm}
    if request.method=='POST':
        userForm=forms.DonorUserForm(request.POST)
        donorForm=forms.DonorForm(request.POST,request.FILES)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            my_donor_group = Group.objects.get_or_create(name='DONOR')
            my_donor_group[0].user_set.add(user)
        return HttpResponseRedirect('donorlogin')
    return render(request,'donor/donorsignup.html',context=mydict)


def donor_dashboard_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_donor=donor).filter(status='Rejected').count(),
    }
    return render(request,'donor/donor_dashboard.html',context=dict)


def donate_blood_view(request):
    donation_form=forms.DonationForm()
    if request.method=='POST':
        donation_form=forms.DonationForm(request.POST)
        if donation_form.is_valid():
            blood_donate=donation_form.save(commit=False)
            blood_donate.bloodgroup=donation_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_donate.donor=donor
            blood_donate.save()
            return HttpResponseRedirect('donation-history')  
    return render(request,'donor/donate_blood.html',{'donation_form':donation_form})

def donation_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    donations=models.BloodDonate.objects.all().filter(donor=donor)
    return render(request,'donor/donation_history.html',{'donations':donations})

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            donor= models.Donor.objects.get(user_id=request.user.id)
            blood_request.request_by_donor=donor
            blood_request.save()
            return HttpResponseRedirect('request-history')  
    return render(request,'donor/makerequest.html',{'request_form':request_form})

def request_history_view(request):
    donor= models.Donor.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_donor=donor)
    return render(request,'donor/request_history.html',{'blood_request':blood_request})

@login_required(login_url='donorlogin')
def donor_profile_view(request):
    donor = Donor.objects.get(user=request.user)  # Get the logged-in donor
    eligibility_message = None

    if request.method == 'POST':
        form = DonorEligibilityForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()  # Save the updated donor details
            eligibility_message = donor.is_eligible()  # Check eligibility
    else:
        form = DonorEligibilityForm(instance=donor)

    return render(request, 'donor/donor_profile.html', {
        'donor': donor,
        'form': form,
        'eligibility_message': eligibility_message,
    })


# def donor_profile_view(request):
#     donor = get_object_or_404(Donor, user_id=request.user.id)
#     return render(request, 'donor/donor_profile.html', {'donor': donor})

@login_required
def edit_donor_profile_view(request):
    donor = get_object_or_404(Donor, user_id=request.user.id)
    
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('donor-profile')  # Redirect to the profile page after saving
    else:
        form = DonorForm(instance=donor)
    
    return render(request, 'donor/edit_donor_profile.html', {'form': form})

@login_required
def update_account_view(request):
    donor = get_object_or_404(Donor, user_id=request.user.id)
    
        # Initialize forms
    username_form = UpdateUsernameForm(instance=request.user)
    password_form = UpdatePasswordForm(request.user)
    
    if request.method == 'POST':
        # Check which form was submitted
        if 'update_username' in request.POST:
            username_form = UpdateUsernameForm(request.POST, instance=request.user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, 'Your username has been updated successfully!')
                return redirect('donor-profile')
        
        elif 'update_password' in request.POST:
            password_form = UpdatePasswordForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep the user logged in
                messages.success(request, 'Your password has been updated successfully!')
                return redirect('donor-profile')
    
    return render(request, 'donor/update_account.html', {
        'username_form': username_form,
        'password_form': password_form,
        'donor': donor,
    })

@login_required(login_url='donorlogin')
def schedule_donation_view(request):
    donor = Donor.objects.get(user=request.user)
    if request.method == 'POST':
        form = DonationScheduleForm(request.POST)
        if form.is_valid():
            donation_schedule = form.save(commit=False)
            donation_schedule.donor = donor
            donation_schedule.save()
            return redirect('donor-dashboard')  # Redirect to donor dashboard
    else:
        form = DonationScheduleForm()
    return render(request, 'donor/schedule_donation.html', {'form': form})


@login_required(login_url='donorlogin')
def view_scheduled_donations_view(request):
    donor = Donor.objects.get(user=request.user)  # Get the logged-in donor
    scheduled_donations = DonationSchedule.objects.filter(donor=donor)  # Get all scheduled donations for the donor
    return render(request, 'donor/view_scheduled_donations.html', {'scheduled_donations': scheduled_donations})

@login_required(login_url='donorlogin')
def donation_requests_view(request):
    donor = Donor.objects.get(user=request.user)  # Get the logged-in donor
    requests = DonationRequest.objects.filter(donor=donor)  # Get all requests for the donor

    return render(request, 'donor/donation_requests.html', {
        'requests': requests,
    })

@login_required(login_url='donorlogin')
def approve_request_view(request, request_id):
    donation_request = DonationRequest.objects.get(id=request_id)
    donation_request.status = 'Approved'
    donation_request.save()
    return redirect('donation_requests')

@login_required(login_url='donorlogin')
def reject_request_view(request, request_id):
    donation_request = DonationRequest.objects.get(id=request_id)
    donation_request.status = 'Rejected'
    donation_request.save()
    return redirect('donation_requests')