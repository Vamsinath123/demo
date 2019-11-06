from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login
from .models import Album
from django.generic.views import View
from .forms import UserForm

def index(request):
	all_albums = Album.objects.all()
	context = {'all_albums' : all_albums}
	return render(request, 'music/index.html', context)

def detail(request, album_id):
	'''try:
		album = Album.objects.get(pk = album_id)
	except Album.DoesNotExist:
		raise Http404('Album DoesNotExist')'''
	album = get_object_or_404(Album, pk = album_id)
	return render(request, 'music/detail.html', {'album' : album})

def favorite(request, album_id):
	album = get_object_or_404(Album, pk = album_id)
	try:
		selected_song = album.song_set.get(pk = request.POST['song'])
	except (KeyError, Song.DoesNotExist):
		return render(request, 'music/detail.html', {
			'album' : album,
			'error_message':"You did not select right song",
			})
	else:
		selected_song.is_favorite = True
		selected_song.save()
		return render(request, 'music/detail.html', {'album' : album})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'music/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
    context = {
        "form": form,
    }
    return render(request, 'music/register.html', context)