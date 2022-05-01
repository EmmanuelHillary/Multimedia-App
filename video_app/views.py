from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout 
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib import messages
from .models import Media
from django.contrib.auth.models import User
import random

def index(request):
    query = request.GET.get('s') or None
    signup_form = SignUpForm()
    objs = Media.objects.all().order_by('-updated') if query is None else Media.objects.filter(title__icontains=query).order_by('-updated')
    context = {
        "signup_form": signup_form,
        "objs": objs
    }
    return render(request, "video_app/index.html", context)

def user_media(request):
    query = request.GET.get('s') or None
    user = User.objects.get(username=request.user.username)
    objs = Media.objects.all().filter(user=user).order_by('-updated') if query is None else Media.objects.filter(user=user).filter(title__icontains=query).order_by('-updated')
    context = {
        "objs": objs
    }
    return render(request, "video_app/mymedia.html", context)

def signup(request):
    if request.is_ajax and request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"error": "Registration Failed"}, status=400)

def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("home")

def login_user(request):
    if request.is_ajax and request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"Welcome! {username}.")
            return redirect("home")
        else:
            return JsonResponse({"error": "Invalid username or password."}, status=400)
    else:
            return JsonResponse({"error": "Invalid username or password."}, status=400)


def create_media(request):
    if request.is_ajax and request.method == "POST":
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            media = request.FILES.getlist("file")[0]
            thumbnail = request.FILES.getlist("thumbnail")
            user = User.objects.get(username=request.user.username)
            obj = Media.objects.create(
                user = user,
                title=title,
                description=description,
                media=media,
                thumbnail = media if thumbnail == [] else thumbnail[0]
            )
            obj.save()
            return JsonResponse({"success": "Media successfully created"}, status=201)
        except:
            return JsonResponse({"error": "Unable to Create Media"}, status=400)
    return JsonResponse({"error": "Unable to Create Media"}, status=400)

def update(request, id):
    obj = get_object_or_404(Media, id=id)
    if request.is_ajax and request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        try:
            media = request.FILES.getlist("file")[0]
        except:
            media = request.FILES.getlist("file")
        thumbnail = request.FILES.getlist("thumbnail")
        user = User.objects.get(username=request.user.username)
        obj.title=title
        obj.description=description
        obj.save()
        if media:
            obj.media=media
            obj.thumbnail = media if thumbnail == [] else thumbnail[0]
            obj.save()
        return JsonResponse({"success": "Media successfully updated"}, status=200)
    return JsonResponse({"error": "Unable to update Media"}, status=400)

def detail_media(request, id):
    obj = get_object_or_404(Media, id=id)
    obj.views += 1
    obj.save()
    media_type = obj.media.url.split('.')[1].lower()
    pic = ['jpeg', 'jpg', 'png', 'gif']
    is_pic = True if media_type in pic else False
    medias = [media for media in Media.objects.all()]
    objs = random.sample(medias, 6) if len(medias) > 6 else random.sample(medias, len(medias))
    context = {
        "media": obj,
        "objs": objs,
        'is_pic': is_pic
    }
    return render(request, "video_app/detail.html", context)

def delete(request, id):
    try:
        obj = get_object_or_404(Media, id=id)
        obj.delete()
        messages.info(request, "Media Has Been successfully deleted")
        return redirect("vids")
    except:
        messages.info(request, "Unable to delete media")
        return redirect("vids")