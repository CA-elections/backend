"""backend URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views import generic
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
import os

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    url(r'^api$', generic.RedirectView.as_view(url='api/', permanent=True)),
    url(r'^api/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static('/dist/', document_root=os.path.join(settings.BASE_DIR, 'dist'))
