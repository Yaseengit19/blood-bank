from django.urls import path

from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    path('patientlogin', LoginView.as_view(template_name='patient/patientlogin.html'),name='patientlogin'),
    path('patientsignup', views.patient_signup_view,name='patientsignup'),
    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('make-request', views.make_request_view,name='make-request'),
    path('my-request', views.my_request_view,name='my-request'),
    path('matching-donors/', views.matching_donors_view, name='matching_donors'),
    path('available-blood-units/', views.available_blood_units_view, name='available_blood_units'),
    path('matching-donors/', views.matching_donors_view, name='matching_donors'),
    path('send-request/<int:donor_id>/', views.send_donation_request_view, name='send_donation_request'),
]