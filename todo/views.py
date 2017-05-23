from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import Http404
from .models import Todo
from .forms import TodoForm

from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, DeleteView, CreateView



class TodoListView(ListView):
    template_name = 'todo/simpleTodo.html'

    context_object_name = 'todo_list'

    def get_queryset(self):
        return Todo.objects.filter(flag=1)

    def get_context_data(self, **kwargs):
        ctx = super(TodoListView, self).get_context_data(**kwargs)
        ctx['finished_todo_list'] = Todo.objects.filter(flag=0)
        ctx['form'] = TodoForm()

        return ctx


class TodoFinishView(SingleObjectMixin, View):
    model = Todo
    success_url = '/todos/'

    def get(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo.flag == '1':
            todo.flag = '0'
            todo.save()
        return HttpResponseRedirect('/todos/')

class TodoBackView(SingleObjectMixin, View):
    model = Todo
    success_url = '/todos/'

    def get(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo.flag == '0':
            todo.flag = '1'
            todo.save()
        return HttpResponseRedirect('/todos/')


class TodoDeleteView(DeleteView):
    model = Todo
    template_name = 'todo/todo_confirm_delete.html'
    success_url = '/todos/'

    # def get(self, request, *args, **kwargs):
    #     return self.post(request, *args, **kwargs)


class TodoAddView(CreateView):
    form_class = TodoForm

    def form_valid(self, form):
        todo = form.save(commit=False)
        todo.user = User.objects.get(id='1')
        todo.flag = '1'
        todo.save()

        return self.render_to_response(self.get_context_data())

    def get_template_names(self):
        if self.request.method == 'POST':
            return ['todo/showtodo.html']
        if self.request.method == 'GET':
            return ['todo/simpleTodo.html']

    def get_context_data(self, **kwargs):
        ctx = super(TodoAddView, self).get_context_data(**kwargs)
        ctx['finished_todo_list'] = Todo.objects.filter(flag=0)
        ctx['todo_list'] = Todo.objects.filter(flag=1)

        return ctx


def updatetodo(request, id=''):
    if request.method == 'POST':
        try:
            todo = Todo.objects.get(id=id)
        except Exception:
            return HttpResponseRedirect('/todos/')
        atodo = request.POST['todo']
        priority = request.POST['priority']
        todo.todo = atodo
        todo.priority = priority
        todo.save()
        return HttpResponseRedirect('/todos/')
    else:
        try:
            todo = Todo.objects.get(id=id)
        except Exception:
            raise Http404
        return render(request, 'todo/updatetodo.html', {'todo': todo})

