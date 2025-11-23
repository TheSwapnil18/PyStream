from django.urls import path
from .views import video_detail_view, like_video, dislike_video, home_view, upload_view
from . import views

urlpatterns = [
    # path('video/<int:video_id>/', video_detail_view, name='video_detail'),
    # path('video/<int:video_id>/like/', like_video, name='like_video'),
    # path('video/<int:video_id>/dislike/', dislike_video, name='dislike_video'),
    path('', views.home_view, name='home'),
    path('upload/', views.upload_view, name='upload'),
    path('video/<int:video_id>/', views.video_detail_view, name='video_detail'),
    path('video/<int:video_id>/like/', views.like_video, name='like_video'),
    path('video/<int:video_id>/dislike/', views.dislike_video, name='dislike_video'),
    path('video/<int:video_id>/delete/', views.delete_video, name='delete_video'),  # ✅ NEW
    path('my-videos/', views.manage_videos, name='manage_videos'),
    path('dashboard/', views.dashboard_view, name='dashboard'),


]
