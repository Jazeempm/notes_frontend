"""notes_frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import never_cache

from myapp.views import LoginView,RegisterView,notes_list,refresh,\
    NoteApiCallView,addnote_view,update_note,delete_note,view_note,upload_image,logout

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("",),
    path("login/",never_cache(LoginView.as_view()),name="login"),
    path("register/",RegisterView.as_view(),name="register"),
    path("",notes_list,name="notes_list"),
    path("refresh",refresh,name="refresh"),
    path("addnote/",addnote_view,name="addnoteform"),
    path("call_addnote/",NoteApiCallView.as_view(),name="addnoteapicall"),
    path("viewnote/<int:pk>/",view_note,name="viewnote"),
    path("updatenote/<int:pk>/",update_note,name="updatenote"),
    path("deletenote/<int:pk>/",delete_note,name="deletenote"),
    path("uploadimage/<int:pk>/",upload_image,name="uploadimage"),
    path("logout/",logout,name="logout")


]
