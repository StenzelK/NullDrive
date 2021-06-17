import os

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect

from file_handler import list_files

def homepage(request):
    if request.user.is_authenticated:
        username = request.user.username
        max_dir = list_files.MAX_DIR
        used = list_files.get_dir_size('media/userfiles/{}'.format(username))
        percent = round((used/max_dir)*100)
        used = "{}MB".format(round(used / (1024 ** 2)))
        max_dir = "{}GB".format(round(max_dir/(1024 ** 3)))

        return render(request=request,
                    template_name='main/index.html',
                    context={
                        'username': username,
                        'max_dir': max_dir,
                        'used': used,
                        'percent': percent
                    })
    else:
        max_dir = "{}GB".format(round(list_files.MAX_DIR / (1024 ** 3)))
        return render(request=request,
                      template_name='main/welcome.html',
                      context={
                          'max_dir': max_dir
                      })


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "You are now logged in as {}".format(username))
                return redirect('/user')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")


def register(request):
    if request.user.is_authenticated:
        return redirect('/user')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            os.mkdir(os.path.join('media/userfiles', username), mode=0o777)
            messages.success(request, "New account created: {}".format(username))
            login(request, user)
            return redirect('/')

        else:
            for msg in form.error_messages:
                messages.error(request, "{}: {}".format(msg, form.error_messages[msg]))

            return render(request=request,
                          template_name="main/register.html",
                          context={"form": form})

    form = UserCreationForm
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/user')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/change_password.html', {
        'form': form
    })

@login_required
def delete_user(request):
    user = request.user
    user.is_active = False
    user.save()
    username = request.user.username
    for f in list_files.list_files(username):
        list_files.secure_delete(username, f)

    os.rmdir('media/userfiles/{}'.format(username))

    messages.success(request, 'Account deleted')
    return redirect('main:homepage')