from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from.forms import BlogCreateForm
from . import models
from.models import Blog
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from . import forms
# Create your views here.


class BlogCreateView(CreateView):
    model = models.Blog
    form_class = forms.BlogCreateForm
    template_name = 'blog_create.html'
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin,UpdateView):
    model = models.Blog
    form_class = forms.BlogCreateForm
    template_name = 'blog_update.html'
    success_url = reverse_lazy('blog_list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BlogDeleteView(DeleteView):
    model = models.Blog
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('blog_list')


def Blog_list(request):
    blogs = Blog.objects.all()
    user = request.user
    blog_writer = []
    if user.is_authenticated:

        blog_writer = Blog.objects.filter(user=user).values_list('user', flat=True)
    context = {
        'blogs': blogs,
        'blog_writer':blog_writer
    }
    return render(request, 'blog_list.html', context)

def Blog_view(request, id):
    blog = Blog.objects.get(id=id)
    return render(request, 'blog_view.html', {'blog':blog})