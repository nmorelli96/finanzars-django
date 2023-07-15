from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

from .forms import RegistroForm

# Create your views here.


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("tipos")
    else:
        form = RegistroForm()
    return render(request, "registro.html", {"form": form})
