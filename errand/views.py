from asyncio import Task
from turtle import title
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Job
from django.urls import reverse_lazy


# Create your views here.

class UserRegistration(FormView):
    template_name = 'errand/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('jobs')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegistration, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('jobs')
        return super(UserRegistration, self).get(*args, **kwargs)

class UserLoginView(LoginView):
    template_name = 'errand/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('jobs')

class JobList(LoginRequiredMixin, ListView):
    model = Job
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = context['jobs'].filter(user=self.request.user)
        context['count'] = context['jobs'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['jobs'] = context['jobs'].filter(
                title__icontains=search_input
            ) #use 'title_startswith' to search with the beginning of a word

        context['search_input'] = search_input

        return context

class JobDetail(LoginRequiredMixin, DetailView):
    model = Job
    context_object_name = 'job'

class JobCreate(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('jobs')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreate, self).form_valid(form)

class JobDetailUpdate(LoginRequiredMixin, UpdateView):
    model = Job
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('jobs')

class JobDelete(LoginRequiredMixin, DeleteView):
    model = Job
    context_object_name = 'job'
    success_url = reverse_lazy('jobs')