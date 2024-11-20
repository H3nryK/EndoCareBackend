from django.urls import path
from . import views

urlpatterns = [
    path("sync-user/<str:uid>/", views.sync_user_data, name="sync_user_data"),
    path("get-user/<str:uid>/", views.get_user_profile, name="get_user_profile"),
]
