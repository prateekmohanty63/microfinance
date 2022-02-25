from django.urls import path
from api.views.loan_products import product_views as product_views
from api.views.loan_products import product_config_views as product_config_views
from api.views.loan_products import payment_config_views as payment_config_views
from api.views.loan_products import interest_config_views as interest_config_views
from api.views.loan_products import fee_config_views as fee_config_views

urlpatterns = [

    # Loan Products
    path('', product_views.getProducts, name="products"),
    path('create/', product_views.createProduct, name="product-create"),
    path('<str:product_id>/', product_views.getProduct, name="product"),
    path('<str:product_id>/update/', product_views.updateProduct, name="product-update"),
    path('<str:product_id>/archive/', product_views.archiveProduct, name="product-archive"),

    # Product Config
    path('<str:product_id>/configs/', product_config_views.getProductConfigs, name="product-configs"),
    path('<str:product_id>/configs/create/', product_config_views.createProductConfig, name="product-config-create"),
    path('<str:product_id>/configs/<product_config_id>/', product_config_views.getProductConfig, name="product-config"),
    path('<str:product_id>/configs/<product_config_id>/update/', product_config_views.updateProductConfig, name="product-config-update"),
    path('<str:product_id>/configs/<product_config_id>/archive/', product_config_views.archiveProductConfig, name="product-config-archive"),
    
    # Payment Config
    path('<str:product_id>/configs/<product_config_id>/payment-configs/', payment_config_views.getPaymentConfigs, name="payment-configs"),
    path('<str:product_id>/configs/<product_config_id>/payment-configs/create/', payment_config_views.createPaymentConfig, name="payment-config-create"),
    path('<str:product_id>/configs/<product_config_id>/payment-configs/<str:payment_config_id>/', payment_config_views.getPaymentConfig, name="payment-config"),
    path('<str:product_id>/configs/<product_config_id>/payment-configs/<str:payment_config_id>/update/', payment_config_views.updatePaymentConfig, name="payment-config-update"),
    path('<str:product_id>/configs/<product_config_id>/payment-configs/<str:payment_config_id>/archive/', payment_config_views.archivePaymentConfig, name="payment-config-archive"),

    # Interest Config
    path('<str:product_id>/configs/<product_config_id>/interest-configs/', interest_config_views.getInterestConfigs, name="interest-configs"),
    path('<str:product_id>/configs/<product_config_id>/interest-configs/create/', interest_config_views.createInterestConfig, name="interest-config-create"),
    path('<str:product_id>/configs/<product_config_id>/interest-configs/<str:interest_config_id>/', interest_config_views.getInterestConfig, name="interest-config"),
    path('<str:product_id>/configs/<product_config_id>/interest-configs/<str:interest_config_id>/update/', interest_config_views.updateInterestConfig, name="interest-config-update"),
    path('<str:product_id>/configs/<product_config_id>/interest-configs/<str:interest_config_id>/archive/', interest_config_views.archiveInterestConfig, name="interest-config-archive"),

    # Fee Config
    path('<str:product_id>/configs/<product_config_id>/fee-configs/', fee_config_views.getFeeConfigs, name="fee-configs"),
    path('<str:product_id>/configs/<product_config_id>/fee-configs/create/', fee_config_views.createFeeConfig, name="fee-config-create"),
    path('<str:product_id>/configs/<product_config_id>/fee-configs/<str:fee_config_id>/', fee_config_views.getFeeConfig, name="fee-config"),
    path('<str:product_id>/configs/<product_config_id>/fee-configs/<str:fee_config_id>/update/', fee_config_views.updateFeeConfig, name="fee-config-update"),
    path('<str:product_id>/configs/<product_config_id>/fee-configs/<str:fee_config_id>/archive/', fee_config_views.archiveFeeConfig, name="fee-config-archive"),

]