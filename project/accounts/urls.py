from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.redirect_dashboard),
    path('accounts/login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html', 
            redirect_authenticated_user=True),
        name="login"),
    path('accounts/logout/',
        auth_views.LogoutView.as_view(),
        name="logout"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('unauthorized/', views.unauthorized, name="unauthorized"),
    path('users/', views.UsersView.as_view(), name="users"),
    path('users/create_user/', views.CreateUserView.as_view(), name="create_user"),
    path('users/delete_user/<int:id>/', views.DeleteUserView.as_view(), name="delete_user"),
    path('users/edit_user/<int:pk>/', views.EditUserView.as_view(), name='edit_user'),
]

htmx_urlpatterns = [
    path('users/get_user_form/', views.get_user_form, name="get_user_form"),
    path('users/check_username/', views.check_username, name="check_username"),
]

urlpatterns += htmx_urlpatterns