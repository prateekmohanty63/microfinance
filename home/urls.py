from django.urls import path
from . import views

urlpatterns = [

    # Website
    path('', views.landing, name='landing'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('about/', views.about, name='about'),

    # Core app
    path('home', views.home, name='home'),

    # Uploading directly to S3
    path('sign-s3/', views.sign_s3, name='sign_s3'),


]
