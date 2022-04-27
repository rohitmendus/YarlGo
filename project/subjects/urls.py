from django.urls import path
from . import views

urlpatterns = [
    path('', views.AdminSubjectsView.as_view(), name="admin_subjects"),
    path('create_subject/', views.CreateSubjectView.as_view(), name="create_subject"),
    path('delete_subject/<int:subject_id>/', views.DeleteSubjectView.as_view(), name="delete_subject"),
    path('edit_subject/<int:subject_id>/', views.EditSubjectView.as_view(), name='edit_subject'),
]

htmx_urlpatterns = [
    path('get_subject_form/', views.get_subject_form, name="get_subject_form"),
]

urlpatterns += htmx_urlpatterns