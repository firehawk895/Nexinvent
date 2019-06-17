"""nexinvent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from mvp import views
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'order_items', views.OrderItemViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'carts', views.CartViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'upload/', views.upload_file),
    url(r'send_orders/', views.send_orders),
    url(r'checkin/', views.checkin),
    path('', include(router.urls)),
    url(r'^docs/', include_docs_urls(title='OrderClap APIs')),
    url(r'^api-token-auth/', obtain_auth_token)
]
