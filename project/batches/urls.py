from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.AdminBatchesView.as_view(), name="admin_batches"),
    path('create_batch/', views.CreateBatchView.as_view(), name="create_batch"),
    path('delete_batch/<int:batch_id>/', views.DeleteBatchView.as_view(), name="delete_batch"),
    path('edit_batch/<int:batch_id>/', views.EditBatchView.as_view(), name='edit_batch'),
]

htmx_urlpatterns = [
    path('get_batch_form/', views.get_batch_form, name="get_batch_form"),
]

urlpatterns += htmx_urlpatterns