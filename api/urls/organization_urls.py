from django.urls import path
from api.views import organization_views as views

urlpatterns = [

    path('', views.getOrganizations, name="organizations"),
    path('create/', views.createOrganization, name="organization-create"),
    path('<str:organization_id>/', views.getOrganization, name="organization"),
    path('<str:organization_id>/update/', views.updateOrganization, name="organization-update"),
    path('<str:organization_id>/archive/', views.archiveOrganization, name="organization-archive"),
    
    # Settings
    path('<str:organization_id>/settings/', views.getOrganizationSettings, name="organization-settings"),
    path('<str:organization_id>/settings/update/', views.updateOrganizationSettings, name="organization-settings-update"),

]