from django.urls import path
from . import views

urlpatterns = [
    path('exams/', views.MainExamsView.as_view(), name="exams"),
    path('exams/create/', views.CreateMainExamView.as_view(), name="create_exam"),
    path('exams/delete/<int:exam_id>/', views.DeleteMainExamView.as_view(), name="delete_exam"),
    path('exams/edit/<int:exam_id>/', views.EditMainExamView.as_view(), name="edit_exam"),
    path('exam_categories/', views.ExamCategoriesView.as_view(), name="exam_categories"),
    path('exam_categories/create/', views.CreateExamCategory.as_view(), name="create_exam_cat"),
    path('exam_categories/delete/<int:exam_cat_id>/', views.DeleteExamCategoryView.as_view(), name="delete_exam_cat"),
    path('exam_categories/edit/<int:exam_cat_id>/', views.EditExamCategoryView.as_view(), name="edit_exam_cat"),
]

htmx_urlpatterns = [
    path('exams/get_form/', views.get_exam_form, name="get_exam_form"),
    path('exam_categories/get_form/', views.get_exam_cat_form, name="get_exam_cat_form"),
]

urlpatterns += htmx_urlpatterns