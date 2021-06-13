from django.urls import path
from . import views

urlpatterns = [

    path('media-folders/', views.handle_media_dirs),
    path('media-folders/<str:dir_type>/', views.handle_media_dirs),

    path('sync/', views.Sync.as_view()),

    path('count/<str:count_type>/', views.get_count),
    path('total-media-duration/', views.get_duration),
    path('port/', views.update_port)
]
