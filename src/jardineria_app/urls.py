from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from jobs.views import JobListView, JobDetailView, export_jobs_csv, export_jobs_xlsx, export_jobs_pdf, health_check, splash

urlpatterns = [
    path('admin/', admin.site.urls),
    path("health/", health_check, name="health_check"),
    path("", splash, name="splash"),
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),

    # Exportaciones
    path('export/csv/', export_jobs_csv, name='export-csv'),
    path('export/xlsx/', export_jobs_xlsx, name='export-xlsx'),
    path("export/pdf/", export_jobs_pdf, name="export_jobs_pdf"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
