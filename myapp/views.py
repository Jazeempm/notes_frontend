import json

from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect,render
from django.views.generic import FormView,View,DeleteView
from .forms import LoginForm,RegisterForm
import requests
# Create your views here.

class LoginView(View):
    def get(self,request):
        if self.request.session.get('token', False):
            return redirect("/")
        return render(request,"login.html")
    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            url = "http://localhost:9000/login/"
            header = {
                "Content-Type": "application/json",
            }
            result = requests.post(url, data=json.dumps(form.cleaned_data), headers=header)
            if result.status_code == 200:
                data = result.json()
                self.request.session['token'] = data
                return redirect('/')
        else:
            return redirect("/login")



# class RegisterView(View):
#     def get(self,request):
#         pass
#     def post(self,request):
#         pass

# class LoginView(View):
#     # template_name = 'login.html'
#     form_class = LoginForm
#     success_url = '/'
#
#     def get_template_names(self):
#         if self.request.session.get('token', False):
#             return redirect("/")
#         return 'login.html'
#
#     def form_valid(self, form):
#         url = "http://localhost:9000/login/"
#         header = {
#             "Content-Type": "application/json",
#         }
#         result = requests.post(url, data=json.dumps(form.cleaned_data), headers=header)
#         if result.status_code == 200:
#             data=result.json()
#             self.request.session['token']=data
#             return super(LoginView, self).form_valid(form)
#         else:
#             return redirect("/login")

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/login'

    def form_valid(self, form):
        url = "http://localhost:9000/register/"
        header = {
            "Content-Type": "application/json",
        }
        result = requests.post(url, data=json.dumps(form.cleaned_data), headers=header)
        if result.status_code == 201:
            return super(RegisterView, self).form_valid(form)
        else:
            return HttpResponse("error")

def addnote_view(request):
    if request.session.get('token', False):

        return render(request,"notes_form.html",{})
    return redirect('/login')


def view_note(request,pk):
    if request.session.get('token', False):
        access_token = request.session['token']['access']
        url = f"http://localhost:9000/notes/{pk}"
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        }
        result = requests.get(url, headers=header)
        if result.status_code == 200:
            return render(request, "viewnote.html", {"data": result.json()})
        else:
            refresh(request)
            return redirect(request.path_info)
    return redirect('/login')

def update_note(request,pk):
    if request.session.get('token', False):
        access_token = request.session['token']['access']
        url = f"http://localhost:9000/notes/{pk}/"
        header = {
            "Authorization": "Bearer " + access_token
        }
        d = {
            "title": request.POST["title"],
            "content": request.POST["content"],
        }

        result = requests.put(url, data=d, headers=header)
        print(result.status_code)
        if result.status_code == 200:
            return redirect(view_note,pk)
        else:
            refresh(request)
            return redirect(request.path_info)
    return redirect('/login')

def delete_note(request,pk):
    if request.session.get('token', False):
        access_token = request.session['token']['access']
        print(access_token)
        url = f"http://localhost:9000/notes/{pk}"
        header = {
            "Content-Type": "application/json",
            "X-Client-Id": "6786787678f7dd8we77e787",
            "X-Client-Secret": "96777676767585",
            "Authorization": "Bearer " + access_token
        }
        result = requests.delete(url, headers=header)
        print(result.status_code)
        if result.status_code == 204:
            return redirect('/')
        else:
            refresh(request)
            return redirect(request.path_info)
    return redirect('/login')

class NoteApiCallView(View):

    def post(self,request):
        if request.session.get('token', False):
            access_token = request.session['token']['access']
            url = "http://localhost:9000/notes/"
            header = {
                "Authorization": "Bearer " + access_token
            }
            d={
                "title":request.POST["title"],
                "content":request.POST["content"],
            }

            result = requests.post(url,data=d,files=request.FILES, headers=header,)

            if result.status_code == 201:
                return redirect("/")
            else:
                refresh(request)
                return redirect(request.path_info)
        return redirect('/login')

def notes_list(request):
    if request.session.get('token', False):
        access_token=request.session['token']['access']
        url = "http://localhost:9000/notes/"
        header = {
            "Authorization":"Bearer "+access_token
        }
        result = requests.get(url, headers=header)
        if result.status_code == 200:
            return render(request,"notes.html",{"data":result.json()})
        else:
            refresh(request)
            return redirect(request.path_info)
    return redirect('/login')


def upload_image(request,pk):
    if request.session.get('token', False):
        access_token = request.session['token']['access']
        url = f"http://localhost:9000/upload_image/{pk}/"
        header = {
            "Authorization": "Bearer " + access_token
        }

        result = requests.post(url,data={}, files=request.FILES, headers=header)
        if result.status_code == 201:
            return redirect(view_note,pk)
        else:
            refresh(request)
            return redirect(request.path_info)
    return redirect('/login')

def refresh(request):
    refresh_token = request.session['token']['refresh']
    url = "http://localhost:9000/api/token/refresh/"

    header = {
        "Content-Type": "application/json"
    }
    body={
        "refresh":refresh_token
    }
    result = requests.post(url,data=json.dumps(body),headers=header)
    if result.status_code == 200:
        data = result.json()
        request.session['token'] = data
    else:
        return redirect('/login')


def logout(request):
    del request.session['token']

    return redirect('/login')