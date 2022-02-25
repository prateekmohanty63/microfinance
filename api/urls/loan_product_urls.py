from django.urls import path
from api.views.loan_product import product_views as product_views

urlpatterns = [

    # Loan Products
    path('', product_views.getProducts, name="products"),
    path('create/', product_views.createProduct, name="product-create"),
    path('<str:product_id>/', product_views.getProduct, name="product"),
    path('<str:product_id>/update/', product_views.updateProduct, name="product-update"),
    path('<str:product_id>/archive/', product_views.archiveProduct, name="product-archive"),

    # Product Config
    path('<str:product_id>/config/', product_views.getProductConfig, name="product-config"),
    path('<str:product_id>/config/update/', product_views.updateProductConfig, name="product-config-update"),
    
    # Payment Config
    # path('<str:product_id>/payment-config/', views.getProductPaymentConfig, name="product-payment-configs"),
    # path('<str:product_id>/payment-config/create/', views.createProductPaymentConfig, name="product-payment-config-create"),
    # path('<str:product_id>/payment-config/<str:payment_config_id>/', views.getProductPaymentConfig, name="product-payment-config"),
    # path('<str:product_id>/payment-config/<str:payment_config_id>/update/', views.updateProductPaymentConfig, name="product-payment-config-update"),
    # path('<str:product_id>/payment-config/<str:payment_config_id>/archive/', views.archiveProductPaymentConfig, name="product-payment-config-archive"),

    # Interest Config
    # path('<str:product_id>/interest-config/', views.getProductInterestConfig, name="product-interest-configs"),
    # path('<str:product_id>/interest-config/create/', views.createProductInterestConfig, name="product-interest-config-create"),
    # path('<str:product_id>/interest-config/<str:interest_config_id>/', views.getProductInterestConfig, name="product-interest-config"),
    # path('<str:product_id>/interest-config/<str:interest_config_id>/update/', views.updateProductInterestConfig, name="product-interest-config-update"),
    # path('<str:product_id>/interest-config/<str:interest_config_id>/archive/', views.archiveProductInterestConfig, name="product-interest-config-archive"),

    # Fee Config
    # path('<str:product_id>/fee-config/', views.getProductFeeConfig, name="product-fee-configs"),
    # path('<str:product_id>/fee-config/create/', views.createProductFeeConfig, name="product-fee-config-create"),
    # path('<str:product_id>/fee-config/<str:fee_config_id>/', views.getProductFeeConfig, name="product-fee-config"),
    # path('<str:product_id>/fee-config/<str:fee_config_id>/update/', views.updateProductFeeConfig, name="product-fee-config-update"),
    # path('<str:product_id>/fee-config/<str:fee_config_id>/archive/', views.archiveProductFeeConfig, name="product-fee-config-archive"),

]