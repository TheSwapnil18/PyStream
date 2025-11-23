from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .models import Video, Comment, VideoView
from .forms import VideoUploadForm, CommentForm


def home_view(request):
    """
    Show all videos for anonymous users.
    Show all videos EXCEPT user's own for logged-in users.
    """
    if request.user.is_authenticated:
        videos = Video.objects.exclude(uploaded_by=request.user).order_by('-uploaded_at')
    else:
        videos = Video.objects.all().order_by('-uploaded_at')

    return render(request, "videos/home.html", {'videos': videos})


# ✅ Only logged-in users can upload
@login_required(login_url='/accounts/login/')
def upload_view(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user
            video.save()
            messages.success(request, "Video uploaded successfully!")
            return redirect('home')
    else:
        form = VideoUploadForm()
    return render(request, "videos/upload.html", {'form': form})


# ✅ Anyone can watch videos
def video_detail_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    videos = Video.objects.all().order_by('-uploaded_at')
    user = request.user if request.user.is_authenticated else None

    # ✅ Unique view count (1 view / 24 hours / user)
    if user:
        view_record, created = VideoView.objects.get_or_create(video=video, user=user)
        if created:
            video.views += 1
            video.save()
        else:
            time_passed = timezone.now() - view_record.last_viewed
            if time_passed > timedelta(hours=24):
                video.views += 1
                video.save()
                view_record.last_viewed = timezone.now()
                view_record.save()
    else:
        # Optional: handle guest views if needed
        pass

    # ✅ Comments
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to comment.")
            return redirect('/accounts/login/')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video
            comment.save()
            return redirect('video_detail', video_id=video.id)
    else:
        form = CommentForm()

    comments = video.comments.all()
    return render(request, "videos/video_detail.html", {
        'video': video,
        'videos': videos,
        'form': form,
        'comments': comments,
    })


# ✅ Like Video (Login Required)
@login_required(login_url='/accounts/login/')
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user = request.user

    if user in video.likes.all():
        video.likes.remove(user)
    else:
        video.likes.add(user)
        video.dislikes.remove(user)

    return redirect('video_detail', video_id=video_id)


# ✅ Dislike Video (Login Required)
@login_required(login_url='/accounts/login/')
def dislike_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user = request.user

    if user in video.dislikes.all():
        video.dislikes.remove(user)
    else:
        video.dislikes.add(user)
        video.likes.remove(user)

    return redirect('video_detail', video_id=video_id)


# ✅ Delete Video (Only by owner)
@login_required(login_url='/accounts/login/')
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if video.uploaded_by != request.user:
        return HttpResponseForbidden("You are not allowed to delete this video.")

    if request.method == 'POST':
        video.delete()
        messages.success(request, "Video deleted successfully!")
        return redirect('manage_videos')

    return render(request, "videos/delete_confirm.html", {"video": video})


# ✅ Manage user’s own videos
@login_required(login_url='/accounts/login/')
def manage_videos(request):
    user_videos = Video.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    return render(request, "videos/manage_videos.html", {"videos": user_videos})

@login_required(login_url='/accounts/login/')
def dashboard_view(request):
    user = request.user
    videos = Video.objects.filter(uploaded_by=user)
    
    total_videos = videos.count()
    total_views = videos.aggregate(Sum('views'))['views__sum'] or 0
    total_likes = sum([v.total_likes() for v in videos])
    total_dislikes = sum([v.total_dislikes() for v in videos])
    
    return render(request, "videos/dashboard.html", {
        'user': user,
        'videos': videos,
        'total_videos': total_videos,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
    })