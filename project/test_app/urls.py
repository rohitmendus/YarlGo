from django.urls import path
from . import views

urlpatterns = [
    path('questions/create/', views.CreateQuestionView.as_view(), name="create_question"),
    path('questions/delete/<int:question_id>/', views.DeleteQuestionView.as_view(), name="delete_question"),
    path('questions/edit/<int:question_id>/', views.EditQuestionView.as_view(), name="edit_question"),
    path('tests/create/', views.CreateTestView.as_view(), name="create_test"),
]

htmx_urlpatterns = [
    # path('get_test_form/', views.get_test_form, name="get_test_form"),
]

urlpatterns += htmx_urlpatterns