from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import views as core_views
from dispatch import views as dispatch_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", core_views.home, name="home"),
    path("dashboard/", core_views.dashboard, name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("load_reading/", dispatch_views.load_reading_table, name="load_reading_table"),
    path("load_reading/create/", dispatch_views.load_reading_form, name="load_reading_form"),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
