from django.urls import path
from configapp import views
from configapp.views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", views.login_views, name="login"),
    path("", views.base_view, name="base"),
    path("download/cv/", views.download_cv, name="download_cv"),
    path("send-message/", views.contact_form, name="send_message"),
    path("messages/", views.contact, name="contact"),
    path('logout/', views.logout_view, name = 'logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
