from django.urls import path
from .views import SignUpView, ProfileView, UpdateProfileView, upgrade_me

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', UpdateProfileView.as_view(), name='profile_edit'), 
    path('profile/upgrade/', upgrade_me, name='upgrade'),
]