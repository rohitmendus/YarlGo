from django.urls import path
from . import views

urlpatterns = [
    path('questions/create/', views.CreateQuestionView.as_view(), name="create_question"),
    path('questions/delete/<int:question_id>/', views.DeleteQuestionView.as_view(), name="delete_question"),
    path('questions/edit/<int:question_id>/', views.EditQuestionView.as_view(), name="edit_question"),
    path('tests/create/', views.CreateTestView.as_view(), name="create_test"),
    path('tests/delete/<int:test_id>/', views.DeleteTestView.as_view(), name="delete_test"),
    path('tests/duplicate/<int:test_id>/', views.DuplicateTestView.as_view(), name="duplicate_test"),
    path('tests/edit/<int:test_id>/', views.EditTestView.as_view(), name="edit_test"),
    path('question_bank/', views.QuestionBankView.as_view(), name="qb"),
]

htmx_urlpatterns = [
    path('get_back_test/', views.get_back_test, name="get_back_test"),
]

urlpatterns += htmx_urlpatterns