from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Mix, Video
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import VideoForm, SearchForm
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList
import urllib
import requests


YOUTUBE_API_KEY = 'AIzaSyCqCIKyrPylUINAM-BkbNYOFNTrAObnhMs'

# Create your views here.
def home(request):
    popular_mixes = [Mix.objects.get(pk=3), Mix.objects.get(pk=4), Mix.objects.get(pk=5)]
    recent_mixes = Mix.objects.all().order_by('-id')
    return render(request,'mixes/home.html', {'recent_mixes':recent_mixes, 'popular_mixes':popular_mixes})

@login_required
def dashboard(request):
    mixes = Mix.objects.filter(user= request.user).order_by('-id')
    return render(request,'mixes/dashboard.html',{'mixes':mixes})

@login_required
def videosearch(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_search_term = urllib.parse.quote(search_form.cleaned_data['search_term'])
        response = requests.get(f'https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_search_term}&key={YOUTUBE_API_KEY}')
        return JsonResponse(response.json())
    else:
        return JsonResponse({'error':'Invalid Entry'})

@login_required
def addvideo(request, pk):
    form = VideoForm()
    search_form = SearchForm()
    mix = Mix.objects.get(pk=pk)
    if not mix.user == request.user:
        raise Http404

    if request.method == "POST":
        #Create
        form = VideoForm(request.POST)
        if form.is_valid():
            video = Video()
            video.mix = mix
            video_url = form.cleaned_data['url']
            video.url = video_url
            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get('v')
            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={ YOUTUBE_API_KEY }')
                json = response.json()
                title = json['items'][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect('detailmix',pk)
            else:
                errors = form._errors.setdefault('url', ErrorList())
                errors.append('Invalid URL')
    return render(request, 'mixes/addvideo.html', {'form':form, 'search_form':search_form, 'mix':mix})

class DeleteVideo(LoginRequiredMixin, generic.DeleteView):
    model = Video
    template_name = 'mixes/deletevideo.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        video = super(DeleteVideo, self).get_object()
        if not video.mix.user == self.request.user:
            raise Http404
        else:
            return video

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        view = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = authenticate(username = username, password = password)
        login(self.request, user)
        return view

class CreateMix(LoginRequiredMixin,generic.CreateView):
    model = Mix
    fields = ['title']
    template_name = 'mixes/createmix.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateMix, self).form_valid(form)
        return redirect('dashboard')

class DetailMix(generic.DetailView):
    model = Mix
    template_name = 'mixes/detailmix.html'

class UpdateMix(LoginRequiredMixin,generic.UpdateView):
    model = Mix
    template_name = 'mixes/updatemix.html'
    fields = ['title']
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        mix = super(UpdateMix, self).get_object()
        if not mix.user == self.request.user:
            raise Http404
        else:
            return mix

class DeleteMix(LoginRequiredMixin, generic.DeleteView):
    model = Mix
    template_name = 'mixes/deletemix.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        mix = super(DeleteMix, self).get_object()
        if not mix.user == self.request.user:
            raise Http404
        else:
            return mix
