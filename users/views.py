from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from .forms import LoginForm,RegisterForm,ProfileForm
from .models import User
from django.views.generic import UpdateView
from django.urls import reverse_lazy





def login_page(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username, password=password)

            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('cleaner:index'))

    form = LoginForm()

    data = {
        'form':form
    }

    return render(request, 'users/login_page.html',context=data)

def logout_page(request):
    logout(request)

    return HttpResponseRedirect(reverse('login_page'))


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User()
                user.username = form.cleaned_data['username']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.set_password(form.cleaned_data['password'])
                user.save()
                return HttpResponseRedirect(reverse('login_page'))
            except:
                return HttpResponseRedirect(reverse('cleaner:index'))


    form = RegisterForm()

    data = {
        'form':form
    }

    return render(request, 'users/register_page.html',context=data)


class ProfileView(UpdateView):
    form_class = ProfileForm
    model = User

    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('cleaner:index')