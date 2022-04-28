from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('exams.urls')),
    path('', include('subjects.urls')),
    path('batches/', include('batches.urls')),
]
