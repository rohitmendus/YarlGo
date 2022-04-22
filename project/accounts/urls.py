from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html', 
            redirect_authenticated_user=True),
        name="login"),
    path('accounts/logout/',
        auth_views.LogoutView.as_view(),
        name="logout"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('users/', views.UserFormView.as_view(), name="users"),
    path('get_user_form/', views.get_user_form, name="get_user_form")
]