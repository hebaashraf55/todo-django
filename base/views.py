from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy 

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from . models import Task

# Create your views here.
class CustomerLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPageView(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPageView, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPageView, self).get(*args, **kwargs)
    


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/task_list.html'
    context_object_name = 'tasks'
    
    def get_context_data(self, **kwargs): #this func is for make the user show the tasks just releated to him not the all tasks
       context = super().get_context_data(**kwargs)
       context ['tasks'] = context['tasks'].filter(user=self.request.user)
       context ['count'] = context['tasks'].filter(complete=False).count()
       
       search_input = self.request.GET.get('search-area') or ''
       if search_input:
           context['tasks']= context['tasks'].filter(title__startswith=search_input)
           context['search-input']= 'search_input'
       return context
    
    
class DetailTaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/task_detail.html'
    context_object_name = 'task'
    
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'discription', 'complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
      
    
    
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'discription', 'complete']
    success_url = reverse_lazy('tasks')
    
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    fields = ['title', 'discription', 'complete']
    success_url = reverse_lazy('tasks')