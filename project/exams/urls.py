from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainExamsView.as_view(), name="exams"),
    path('create_exam/', views.CreateMainExamView.as_view(), name="create_exam"),
    path('delete_exam/<int:exam_id>/', views.DeleteMainExamView.as_view(), name="delete_exam"),
    path('edit_exam/<int:exam_id>/', views.EditMainExamView.as_view(), name="edit_exam"),
]

htmx_urlpatterns = [
    path('get_exam_form/', views.get_exam_form, name="get_exam_form"),
]

urlpatterns += htmx_urlpatterns