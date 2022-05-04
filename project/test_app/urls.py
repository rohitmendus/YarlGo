from django.urls import path
from . import views

urlpatterns = [
    path('questions/create/', views.CreateQuestionView.as_view(), name="create_question"),
    path('questions/delete/<int:question_id>/', views.DeleteQuestionView.as_view(), name="delete_question"),
    path('questions/edit/<int:question_id>/', views.EditQuestionView.as_view(), name="edit_question"),
]

htmx_urlpatterns = [
    # path('get_subject_form/', views.get_subject_form, name="get_subject_form"),
    # path('get_topic_form/', views.get_topic_form, name="get_topic_form"),
]

# urlpatterns += htmx_urlpatterns