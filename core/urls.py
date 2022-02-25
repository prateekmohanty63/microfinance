from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import handler403, handler404, handler500
from home import views as home_views

handler500 = home_views.error_500
handler403 = home_views.error_403
handler404 = home_views.error_404

urlpatterns = [

    # API
    path('api/users/', include('api.urls.user_urls')),
    path('api/organizations/', include('api.urls.organization_urls')),
    path('api/loans/products/', include('api.urls.loan_product_urls')),
    
    # Web App
    path('', include('accounts.urls')),
    path('', include('home.urls')),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Microfinance Admin Panel"
admin.site.site_title = "Microfinance Admin Panel"
admin.site.index_title = ""
