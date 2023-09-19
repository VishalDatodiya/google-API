from django.urls import path, re_path

from account.api import views

app_name = 'users'

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name="login"),
    re_path('api/register-by-access-token/' + r'social/(?P<backend>[^/]+)/$', views.register_by_access_token),
    path('api/authentication-test/', views.authentication_test),
]