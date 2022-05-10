from django.urls import path
from . import views

urlpatterns = [
    # Admin
    path('subjects/', views.AdminSubjectsView.as_view(), name="admin_subjects"),
    path('subjects/create_subject/', views.CreateSubjectView.as_view(), name="create_subject"),
    path('subjects/delete_subject/<int:subject_id>/', views.DeleteSubjectView.as_view(), name="delete_subject"),
    path('subjects/edit_subject/<int:subject_id>/', views.EditSubjectView.as_view(), name='edit_subject'),
    path('faculty_allotment/', views.FacultyAllotmentView.as_view(), name='faculty_allotment'),
    # Faculty
    path('faculty/', views.FacultyTemplateView.as_view(), name="faculty_operations"),
    path('subjects/store_subject/', views.store_subject, name="store_subject"),
    path('topics/create/', views.CreateTopicView.as_view(), name="create_topic"),
    path('topics/delete/<int:topic_id>/', views.DeleteTopicView.as_view(), name="delete_topic"),
    path('topics/delete_questions/<int:topic_id>/', views.DeleteTopicQuestionsView.as_view(), name="delete_questions_topic"),
    path('topics/edit/<int:topic_id>/', views.EditTopicView.as_view(), name="edit_topic"),
    path('download_topic_temp/', views.DownloadTopicTempView.as_view(), name="download_topic_temp"),
    path('upload_topics/', views.UploadTopicsView.as_view(), name="upload_topics"),
]

htmx_urlpatterns = [
    path('get_subject_form/', views.get_subject_form, name="get_subject_form"),
    path('get_topic_form/', views.get_topic_form, name="get_topic_form"),
]

urlpatterns += htmx_urlpatterns