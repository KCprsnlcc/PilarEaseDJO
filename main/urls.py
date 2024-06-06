from django.contrib import admin
from django.urls import path, include
from main import views  # Adjust this import if your views are in a different app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Your home view
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's auth URLs
    # Other URL patterns...
]
