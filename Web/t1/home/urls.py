from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
        path('bck1/', views.bck1, name='bck1'),  
]
