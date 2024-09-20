from django.http import HttpResponse
import django.shortcuts
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

import account.forms


def user_login(request):
    if request.method == 'POST':
        form = account.forms.LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Logged in successfully')
                else:
                    return HttpResponse('Your account is disabled')
            else:
                return HttpResponse('Invalid login or password')
    else:
        form = account.forms.LoginForm()

    return django.shortcuts.render(request=request, template_name='account/login.html', context={'form': form})


@login_required
def dashboard(request):
    return django.shortcuts.render(request=request,
        template_name='account/dashboard.html', context={"section": "dashboard"})