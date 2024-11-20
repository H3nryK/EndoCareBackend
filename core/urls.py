from django.urls import path
from . import views

urlpatterns = [
    path("sync-user/<str:uid>/", views.sync_user_data, name="sync_user_data"),
    path("get-user/<str:uid>/", views.get_user_profile, name="get_user_profile"),
    path("edit-user/<str:uid>/", views.edit_user_profile, name="edit_user_profile"),
    path('medications/add/<str:uid>/', views.add_medication, name='add_medication'),
    path('medications/get/<str:uid>/', views.get_medications, name='get_medications'),
    path('appointments/add/<str:uid>/', views.add_appointment, name='add_appointment'),
    path('appointments/get/<str:uid>/', views.get_appointments, name='get_appointments'),
]
