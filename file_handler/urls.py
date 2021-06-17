from django.urls import path
from . import views

app_name = 'file_handler'  # here for namespacing of urls.

urlpatterns = [
    path("", views.files, name="files"),

]
