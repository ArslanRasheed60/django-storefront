from django.urls import path
from . import views

# URL Config
urlpatterns = [
    path('hello/', views.say_hello)
]
