from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('browse/', views.browse, name='browse'),
    path('upload/', views.upload_material, name='upload'),
    path('material/<int:pk>/', views.material_detail, name='material_detail'),
    path('materials/use/<int:material_id>/', views.use_material, name='use_material'),
    path('donate/', views.donate_material, name='donate'),
    # path('donations/pending/', views.pending_donations, name='pending_donations'),
    # path('donations/approve/<int:donation_id>/', views.approve_donation, name='approve_donation'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),
    path('approve_request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('decline_request/<int:request_id>/', views.decline_request, name='decline_request'),
    path('logout/', views.logout_user, name='logout'),
]
