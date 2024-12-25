from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('calculate-calories/', views.calculate_calories, name='calculate_calories'),
    path('recommendations/', views.calculate_calories, name='recommendations'),
    # Route for the index page
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)