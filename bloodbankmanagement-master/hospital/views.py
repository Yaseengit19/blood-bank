from django.shortcuts import render, redirect
from . import forms, models
from django.db.models import Sum, Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from blood import forms as bforms
from blood import models as bmodels
from .forms import HospitalUserForm,HospitalForm
from django.db.models import Sum
from .models import Hospital
from blood.models import DonationSchedule
from blood.forms import BloodRequestForm

def hospital_signup_view(request):
    userForm = HospitalUserForm()
    hospitalForm = HospitalForm()
    mydict = {'userForm': userForm, 'hospitalForm': hospitalForm}

    if request.method == 'POST':
        userForm = HospitalUserForm(request.POST)
        hospitalForm = HospitalForm(request.POST, request.FILES)
        if userForm.is_valid() and hospitalForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)  # Hash the password
            user.save()
            hospital = hospitalForm.save(commit=False)
            hospital.user = user
            hospital.save()
            # Add user to the HOSPITAL group
            my_hospital_group, created = Group.objects.get_or_create(name='HOSPITAL')
            my_hospital_group.user_set.add(user)
            return redirect('hospitallogin')  # Redirect to hospital login page after successful registration
        else:
            # If form is invalid, re-render the form with errors
            mydict['userForm'] = userForm
            mydict['hospitalForm'] = hospitalForm

    return render(request, 'hospital/hospital_signup.html', context=mydict)

# Hospital Dashboard View
@login_required(login_url='hospitallogin')
def hospital_dashboard_view(request):
    try:
        
        hospital = Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
            return redirect('hospital_signup')
    blood_requests = bmodels.BloodRequest.objects.filter(request_by_hospital=hospital)
    dict = {
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital).filter(status='Rejected').count(),
        'bloodunitsreceived': bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital).filter(status='Approved').aggregate(Sum('unit'))['unit__sum'] or 0,
    }
    return render(request, 'hospital/hospital_dashboard.html', context=dict)

# Bulk Blood Request View
@login_required(login_url='hospitallogin')
def make_bulk_request_view(request):
    request_form = BloodRequestForm()
    if request.method == 'POST':
        request_form = BloodRequestForm(request.POST)
        if request_form.is_valid():
            blood_request = request_form.save(commit=False)
            blood_request.bloodgroup = request_form.cleaned_data['bloodgroup']
            blood_request.urgency_level = request_form.cleaned_data['urgency_level']
            hospital = Hospital.objects.get(user_id=request.user.id)
            blood_request.request_by_hospital = hospital
            blood_request.is_emergency = False  # Bulk request
            blood_request.save()
            return redirect('my_requests')
    return render(request, 'hospital/make_bulk_request.html', {'request_form': request_form})

# Emergency Blood Request View
@login_required(login_url='hospitallogin')
def make_emergency_request_view(request):
    request_form = BloodRequestForm()
    if request.method == 'POST':
        request_form = BloodRequestForm(request.POST)
        if request_form.is_valid():
            blood_request = request_form.save(commit=False)
            blood_request.bloodgroup = request_form.cleaned_data['bloodgroup']
            blood_request.last_date = request_form.cleaned_data['last_date']  # Save last date
            hospital = Hospital.objects.get(user_id=request.user.id)
            blood_request.request_by_hospital = hospital
            blood_request.is_emergency = True  # Emergency request
            blood_request.save()
            return redirect('my_requests')
    return render(request, 'hospital/make_emergency_request.html', {'request_form': request_form})


# View to Track Blood Requests
@login_required(login_url='hospitallogin')
def my_requests_view(request):
    hospital = models.Hospital.objects.get(user_id=request.user.id)
    blood_requests = bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital)
    return render(request, 'hospital/my_requests.html', {'blood_requests': blood_requests})

# View to Manage Received Blood Units
@login_required(login_url='hospitallogin')
def recieved_blood_units_view(request):
    hospital = models.Hospital.objects.get(user_id=request.user.id)
    blood_requests = bmodels.BloodRequest.objects.all().filter(request_by_hospital=hospital).filter(status='Approved')
    return render(request, 'hospital/recieved_blood_units.html', {'blood_requests': blood_requests})


@login_required(login_url='hospitallogin')
def hospital_profile_view(request):
    hospital = Hospital.objects.get(user=request.user)
    return render(request, 'hospital/hospital_profile.html', {'hospital': hospital})

@login_required(login_url='hospitallogin')
def edit_hospital_profile_view(request):
    hospital = Hospital.objects.get(user=request.user)
    if request.method == 'POST':
        form = HospitalForm(request.POST, request.FILES, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('hospital_profile')
    else:
        form = HospitalForm(instance=hospital)
    return render(request, 'hospital/edit_hospital_profile.html', {'form': form})

@login_required(login_url='hospitallogin')
def update_hospital_account_view(request):
    hospital = Hospital.objects.get(user=request.user)
    if request.method == 'POST':
        form = HospitalUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('hospital_profile')
    else:
        form = HospitalUserForm(instance=request.user)
    return render(request, 'hospital/update_hospital_account.html', {'form': form})

@login_required(login_url='hospitallogin')
def manage_donation_schedules_view(request):
    hospital = Hospital.objects.get(user=request.user)
    donation_schedules = DonationSchedule.objects.filter(hospital=hospital)
    return render(request, 'hospital/manage_donation_schedules.html', {'donation_schedules': donation_schedules})

@login_required(login_url='hospitallogin')
def approve_donation_schedule_view(request, schedule_id):
    donation_schedule = DonationSchedule.objects.get(id=schedule_id)
    donation_schedule.status = 'Approved'
    donation_schedule.save()
    return redirect('manage_donation_schedules')

@login_required(login_url='hospitallogin')
def reject_donation_schedule_view(request, schedule_id):
    donation_schedule = DonationSchedule.objects.get(id=schedule_id)
    donation_schedule.status = 'Rejected'
    donation_schedule.save()
    return redirect('manage_donation_schedules')