from django.urls import path
from configapp import views
from configapp.views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home_view, name="home"),
    path('admin/', admin.site.urls),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path('posts', post_list, name="posts"),
    path("create/", views.post_create, name="post_create"),
    path("posts/<int:id>/", views.post_detail, name="post_detail"),
    path("posts/<int:id>/edit/", views.post_edit, name="post_edit"),
    path("posts/<int:id>/delete/", views.post_delete, name="post_delete"),

    path("posts/<int:id>/comments/add/", views.comment_add, name="comment_add"),

    path("install/", views.install_demo, name="install"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
