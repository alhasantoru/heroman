from django.shortcuts import render
from .forms import UserForm, UserInfoForm
from .models import UserInfo


from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, "basic_app/index.html")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    
    registered = False

    if request.method == "POST":

        user_form = UserForm(data=request.POST)
        profile_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserInfoForm()
    
    return render(request, 'basic_app/registration.html', 
                            {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered':registered})
                             

def user_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponseRedirect("Account not Active!")

        else:
            print("Username and Password incorrect!")
            return HttpResponseRedirect(reverse("basic_app:user_login"))

    else:
        return render(request, "basic_app/login.html")