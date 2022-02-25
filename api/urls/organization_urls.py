from django.urls import path
from api.views import organization_views as views

urlpatterns = [

    path('', views.getOrganizations, name="organizations"),
    path('create/', views.createOrganization, name="organization-create"),
    path('<str:organization_id>/', views.getOrganization, name="organization"),
    path('update/<str:organization_id>/', views.updateOrganization, name="organization-update"),
    path('archive/<str:organization_id>/', views.archiveOrganization, name="organization-archive"),

]