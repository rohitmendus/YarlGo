from django.urls import path
from . import views

urlpatterns = [
    path('subjects/', views.AdminSubjectsView.as_view(), name="admin_subjects"),
    path('subjects/create_subject/', views.CreateSubjectView.as_view(), name="create_subject"),
    path('subjects/delete_subject/<int:subject_id>/', views.DeleteSubjectView.as_view(), name="delete_subject"),
    path('subjects/edit_subject/<int:subject_id>/', views.EditSubjectView.as_view(), name='edit_subject'),
    path('faculty_allotment/', views.FacultyAllotmentView.as_view(), name='faculty_allotment'),
    path('faculty/', views.FacultyTemplateView.as_view(), name="faculty_operations"),
    path('subjects/store_subject/', views.store_subject, name="store_subject"),
    path('topics/create/', views.CreateTopicView.as_view(), name="create_topic"),
]

htmx_urlpatterns = [
    path('get_subject_form/', views.get_subject_form, name="get_subject_form"),
    path('get_topic_form/', views.get_topic_form, name="get_topic_form"),
]

urlpatterns += htmx_urlpatterns