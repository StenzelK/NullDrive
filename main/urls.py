from django.contrib import admin
from django.urls import path, re_path

from . import views

app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register, name="register"),
    path("logout", views.logout_request, name="logout"),
    path("login/", views.login_request, name="login"),
    path("change_pass/", views.change_password, name="change_pass"),
    path("delete_user/", views.delete_user, name="delete_user"),
    path('admin/', admin.site.urls),
    re_path(r'^.*/$', views.homepage, name="delete_user"),

]
