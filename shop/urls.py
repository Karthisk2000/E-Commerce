from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login, name='login'),
    path('login_success', views.login_success, name='login_success'),
    path('register', views.register, name='register'),
    path('user_register', views.user_register, name='user_register'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_product', views.add_product, name='add_product'),
    path('product_delete', views.product_delete, name='product_delete'),
    path('product_update', views.product_update, name='product_update')
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
