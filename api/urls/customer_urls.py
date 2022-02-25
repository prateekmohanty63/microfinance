from django.urls import path
from api.views.customers import customer_views as views

urlpatterns = [

    path('', views.getCustomers, name="customers"),
    path('create/', views.createCustomer, name="customer-create"),
    path('<str:customer_id>/', views.getCustomer, name="customer"),
    path('<str:customer_id>/update/', views.updateCustomer, name="customer-update"),
    path('<str:customer_id>/archive/', views.archiveCustomer, name="customer-archive"),

]