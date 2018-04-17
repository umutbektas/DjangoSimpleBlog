from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout


def register(request):

        #request POST control
        form = RegisterForm(request.POST or None)
        #form validation control
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            newUser = User(username=username)
            newUser.set_password(password)
            newUser.save()

            login(request, newUser)
            messages.success(request, "Kayıt Başarılı !")

            return redirect("index")

        else:
            context = {
                "form": form
            }
            return render(request, "register.html", context)




def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form": form
    }

    if form.is_valid():

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Kullanıcı Adı veya Parola hatalı.")
            return render(request, "login.html", context)

        messages.success(request, "Başarıyla giriş yapıldı !")
        login(request,user)
        return redirect("index")

    else:
        return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yapıldı !")
    return redirect("index")