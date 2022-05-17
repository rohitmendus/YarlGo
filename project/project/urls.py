from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/upload/', login_required(ckviews.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckviews.browse)), name='ckeditor_browse'),
    path('', include('accounts.urls')),
    path('', include('exams.urls')),
    path('', include('subjects.urls')),
    path('batches/', include('batches.urls')),
    path('', include('test_app.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)