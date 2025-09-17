# from django.urls import path
from configapp import views
# from configapp.views import *
# from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static
#
# from django.contrib import admin
# from django.urls import path
# from configapp import views  # 'portfolio' bu sizning ilovangiz nomi deb faraz qilindi
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.index, name='base'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('download-cv/', views.download_cv, name='download_cv'),
#     path('send-message/', views.index, name='send_message'),
#     path('admin_panel/', views.admin, name='admin_panel'),
#     path('projects/', views.projects_list, name='projects_list'),
#     path('projects/add/', views.add_project, name='add_project'),
#     path('projects/edit/<int:id>/', views.edit_project, name='edit_project'),
#     path('projects/delete/<int:id>/', views.delete_project, name='delete_project'),
#
#     # Messages
#     path('messages/', views.message_list, name='message_list'),
#
#     # Edit profile
#     path('profile/edit/', views.edit_profile, name='edit_profile'),
# ]
#
# # urlpatterns = [
# #     path('admin/', admin.site.urls),
# #     # path("login/", views.login_views, name="login"),
# #     # path("", views.base_view, name="base"),
# #     # path("download/cv/", views.download_cv, name="download_cv"),
#     # path("send-message/", views.contact_form, name="send_message"),
# #     # path("messages/", views.contact, name="contact"),
# #     # path('logout/', views.logout_view, name = 'logout'),
# #     # path("dashboard/", views.dashboard, name="dashboard"),
# #     # path("dashboard/", views.dashboard, name="dashboard"),
# #     # path("projects/", views.projects_list, name="projects_list"),
# #     # path("projects/add/", views.add_project, name="add_projects"),
# #     # path("projects/<int:pk>/update/", views.update_project, name="update_project"),
# #     # path("projects/<int:pk>/delete/", views.delete_project, name="delete_project"),
# #     # path("messages/", views.message_list, name="message_list"),
# #     # path("profile/edit/", views.edit_profile, name="edit_profile"),
# # ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from django.urls import path
# from  import views

urlpatterns = [
    path('', views.index, name='base'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', views.admin, name='admin_panel'),

    # Project CRUD
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/edit/<int:id>/', views.edit_project, name='edit_project'),
    path('projects/delete/<int:id>/', views.delete_project, name='delete_project'),

    # Profile
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Messages
    path('messages/', views.message_list, name='message_list'),

    # Download CV
    path('download-cv/', views.download_cv, name='download_cv'),
]
