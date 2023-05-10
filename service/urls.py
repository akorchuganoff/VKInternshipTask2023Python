from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "service"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path('logout', views.logout_request, name='logout'),

    path('find_user', views.find_user, name='find_user'),
    path('outgoing', views.outgoing_friend_request_list, name='outgoing'),

    path('send_friend_request', views.send_friend_request, name='send_friend_request'),
    path('cancel_friend_request', views.cancel_friend_request, name='cancel_friend_request'),

]
