from django.urls import path
from . import views

app_name = "api"
urlpatterns = [
    path('status', views.status.as_view()),
    path('hello', views.hello.as_view()),
]