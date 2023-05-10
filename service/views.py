from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import NewUserForm, UserFindForm
from .models import OutgoingRequests, IngoingRequests


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("service:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="service/register.html", context={"register_form": form})


def homepage(request):
    # return HttpResponse('<h1>Hello</h1>')
    return render(request=request, template_name="service/home.html")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # print(type(user.id))
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("service:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="service/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("service:homepage")


def find_user(request):
    if request.method == "POST":
        user = request.user
        form = UserFindForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            finded_user = User.objects.filter(username=username).first()
            if finded_user is not None:
                status = 0
                f1 = False
                f2 = False
                # print(OutgoingRequests.objects.get(to_user_id=finded_user, from_user_id=user.id))
                try:
                    outgoing = OutgoingRequests.objects.get(to_user_id=finded_user, from_user_id=user.id)
                except OutgoingRequests.DoesNotExist:
                    outgoing=None

                try:
                    ingoing = IngoingRequests.objects.get(from_user_id=finded_user, to_user_id=user.id)
                except IngoingRequests.DoesNotExist:
                    ingoing=None

                if outgoing is not None:
                    f1 = True
                if ingoing is not None:
                    f2 = True

                if not f1 and not f2:
                    status = 1
                if f1 and not f2:
                    status = 2
                if not f1 and f2:
                    status = 3
                if f1 and f2:
                    status = 4

                return render(request=request, template_name="service/find_user.html",
                              context={"find_form": form, "status": status, "username": username})
            else:
                return render(request=request, template_name='service/Error404.html')

    form = UserFindForm()
    return render(request=request, template_name="service/find_user.html", context={"find_form": form, })


def outgoing_friend_request_list(request):
    user = request.user
    outgoing =set(map(lambda x: x.to_user_id.username, OutgoingRequests.objects.filter(from_user_id=user.id).all()))
    ingoing = set(map(lambda x: x.from_user_id.username, IngoingRequests.objects.filter(to_user_id=user.id).all()))



    friends = set.intersection(outgoing, ingoing)
    outgoing_result = outgoing.difference(ingoing)
    ingoing_result = ingoing.difference(outgoing)

    return render(request=request, template_name="service/outgoing.html", context={"outgoing": outgoing_result, "ingoing": ingoing_result, "friends": friends})


def send_friend_request(request):
    username = request.GET.get('username', None)
    print(username)
    user = request.user

    finded_user = User.objects.filter(username=username).first()
    OutgoingRequests.objects.create(from_user_id=user.id, to_user_id=finded_user)
    IngoingRequests.objects.create(to_user_id=finded_user.id, from_user_id=user)

    return redirect("service:find_user")


def cancel_friend_request(request):
    username = request.GET.get('username', None)
    print(username)
    user = request.user

    finded_user = User.objects.filter(username=username).first()
    OutgoingRequests.objects.get(from_user_id=user.id, to_user_id=finded_user).delete()
    IngoingRequests.objects.get(to_user_id=finded_user.id, from_user_id=user).delete()

    return redirect("service:find_user")