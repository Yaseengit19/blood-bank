from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('hospitallogin',LoginView.as_view(template_name='hospital/hospitallogin.html'),name='hospitallogin'),
    path('hospital-signup/', views.hospital_signup_view, name='hospital_signup'),
    path('hospital-dashboard/', views.hospital_dashboard_view , name='hospital_dashboard'),
    path('make-bulk-request/', views.make_bulk_request_view, name='make_bulk_request'),
    path('make-emergency-request/', views.make_emergency_request_view, name='make_emergency_request'),
    path('my-requests/', views.my_requests_view, name='my_requests'),
    path('recieved-blood-units/', views.recieved_blood_units_view, name='recieved_blood_units'),
    path('hospital-profile/', views.hospital_profile_view, name='hospital_profile'),
    path('edit-hospital-profile/', views.edit_hospital_profile_view, name='edit_hospital_profile'),
    path('update-hospital-account/', views.update_hospital_account_view, name='update_hospital_account'),
    path('manage-donation-schedules/', views.manage_donation_schedules_view, name='manage_donation_schedules'),
    path('approve-donation-schedule/<int:schedule_id>/', views.approve_donation_schedule_view, name='approve_donation_schedule'),
    path('reject-donation-schedule/<int:schedule_id>/', views.reject_donation_schedule_view, name='reject_donation_schedule'),
]