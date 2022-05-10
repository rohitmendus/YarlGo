from django.urls import path
from . import views

urlpatterns = [
    # Admin urls
    path('admin/', views.AdminBatchesView.as_view(), name="admin_batches"),
    path('create_batch/', views.CreateBatchView.as_view(), name="create_batch"),
    path('delete_batch/<int:batch_id>/', views.DeleteBatchView.as_view(), name="delete_batch"),
    path('edit_batch/<int:batch_id>/', views.EditBatchView.as_view(), name='edit_batch'),
    path('timings/', views.BatchTimingsView.as_view(), name="batch_timings"),
    path('timings/create/', views.CreateBatchTimingView.as_view(), name="create_batch_timing"),
    path('timings/delete/<int:batch_timing_id>/', views.DeleteBatchTimingView.as_view(), name="delete_batch_timing"),
    path('timings/edit/<int:batch_timing_id>/', views.EditBatchTimingView.as_view(), name="edit_batch_timing"),
    # Student urls
    path('batch/<int:batch_id>/', views.StudentBatchView.as_view(), name="student_batch"),
]

htmx_urlpatterns = [
    path('get_batch_form/', views.get_batch_form, name="get_batch_form"),
    path('get_batch_timing_form/', views.get_batch_timing_form, name="get_batch_timing_form"),
]

urlpatterns += htmx_urlpatterns