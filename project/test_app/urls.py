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
    path('question_bank/<int:topic_id>/', views.QuestionBankView.as_view(), name="qb"),
    path('download_question_temp/', views.DownloadQuestionTempView.as_view(), name="download_question_temp"),
    path('upload_questions/', views.UploadQuestionsView.as_view(), name="upload_questions"),
    path('test/<int:test_id>/', views.TestPromptView.as_view(), name="test_prompt"),
    path('take_test/', views.TakeTestView.as_view(), name="take_test"),
    path('take_test/select_answer/', views.select_answer, name="select_answer_test"),
    path('take_test/clear_answer/', views.clear_answer, name="clear_answer_test"),
    path('take_test/mark_question/', views.mark_question, name="mark_question_test"),
    path('take_test/get_info/', views.get_test_info, name="get_info_test"),
    path('take_test/submit/', views.submit_test, name="submit_test"),
    path('test/<int:test_id>/review/<int:user_id>/', views.ReviewAnswersView.as_view(), name="review_answers"),
    path('test/<int:test_id>/report/<int:user_id>/', views.StudentTestReportView.as_view(), name="student_test_report"),
    path('test/<int:test_id>/overall_report/', views.FacultyTestReportView.as_view(), name="faculty_test_report"),
]

htmx_urlpatterns = [
    path('get_back_test/', views.get_back_test, name="get_back_test"),
]

urlpatterns += htmx_urlpatterns