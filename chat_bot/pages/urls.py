from django.urls import path
from pages import views

urlpatterns = [
   path('', views.intro, name='intro'),
    path('set_personality/', views.set_personality, name='set_personality'),
    path('home/', views.home, name='home'),
    path('send/', views.send_message, name='send_message'),
]