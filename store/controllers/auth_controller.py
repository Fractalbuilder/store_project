from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..services.auth_service import AuthService
from ..exceptions.common import PasswordMismatchError

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        try:
            AuthService.register_user(request, username, email, password, confirmation)
            return HttpResponseRedirect(reverse("index"))

        except PasswordMismatchError as e:
            return render(request, "store/register.html", {"message": str(e)})

        except ValueError as e:  # from repository
            return render(request, "store/register.html", {"message": str(e)})

    return render(request, "store/register.html")
