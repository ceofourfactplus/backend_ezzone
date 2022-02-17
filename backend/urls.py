from django.contrib import admin
from django.urls import path,include 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('pos/', include('pos.urls')),
    path('raw_material/', include('raw_material.urls')),
    # path('material/', include('material.urls')),
    path('customer/', include('customer.urls')),
    path('promotion/',include('promotion.urls')),
    path('user/', include('user.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
