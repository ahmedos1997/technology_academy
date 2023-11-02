from django.shortcuts import render
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from . import forms
from .forms import Register,Profile
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.

class RegisterView(CreateView):
    form_class = Register
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


@login_required
def editprofile(request):
    if request.method == 'POST':
        form = Profile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = Profile(instance=request.user)
        return render(request, 'profile.html', {
            'form': form
        })