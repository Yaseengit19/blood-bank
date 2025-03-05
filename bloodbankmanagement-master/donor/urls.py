from django.urls import path

from django.contrib.auth.views import LoginView
from . import views
urlpatterns = [
    path('donorlogin', LoginView.as_view(template_name='donor/donorlogin.html'),name='donorlogin'),
    path('donorsignup', views.donor_signup_view,name='donorsignup'),
    path('donor-dashboard', views.donor_dashboard_view,name='donor-dashboard'),
    path('donate-blood', views.donate_blood_view,name='donate-blood'),
    path('donation-history', views.donation_history_view,name='donation-history'),
    path('make-request', views.make_request_view,name='make-request'),
    path('request-history', views.request_history_view,name='request-history'),
    path('donor-profile', views.donor_profile_view,name='donor-profile'),
    path('edit-donor-profile/', views.edit_donor_profile_view, name='edit_donor_profile'),
    path('update-account/', views.update_account_view, name='update_account'),
    path('schedule-donation/', views.schedule_donation_view, name='schedule_donation'),
    path('view-scheduled-donations/', views.view_scheduled_donations_view, name='view_scheduled_donations'),
    path('donation-requests/', views.donation_requests_view, name='donation_requests'),
    path('approve-request/<int:request_id>/', views.approve_request_view, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request_view, name='reject_request'),

]