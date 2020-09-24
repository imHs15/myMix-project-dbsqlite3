"""myMix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.urls import path
from mixes import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    #Auth
    path('signup', views.SignUp.as_view(), name = 'signup'),
    path('login', auth_views.LoginView.as_view(), name = 'login'),
    path('logout', auth_views.LogoutView.as_view(), name = 'logout'),
    #Mix
    path('myMix/create', views.CreateMix.as_view(), name='createmix'),
    path('myMix/<int:pk>', views.DetailMix.as_view(), name='detailmix'),
    path('myMix/<int:pk>/update', views.UpdateMix.as_view(), name='updatemix'),
    path('myMix/<int:pk>/delete', views.DeleteMix.as_view(), name='deletemix'),
    #Video
    path('myMix/<int:pk>/addvideo', views.addvideo, name='addvideo'),
    path('video/search', views.videosearch, name='videosearch'),
    path('video/<int:pk>/delete', views.DeleteVideo.as_view(), name='deletevideo'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
