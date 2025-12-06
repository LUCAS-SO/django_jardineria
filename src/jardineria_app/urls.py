"""
URL configuration for jardineria_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from jobs.views import JobListView, JobDetailView, export_jobs_csv, export_jobs_xlsx, export_jobs_pdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),

    # Exportaciones
    path('export/csv/', export_jobs_csv, name='export-csv'),
    path('export/xlsx/', export_jobs_xlsx, name='export-xlsx'),
    path("export/pdf/", export_jobs_pdf, name="export_jobs_pdf"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
