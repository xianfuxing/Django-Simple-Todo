from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import Http404
from .models import Todo
from .forms import TodoForm

from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, DeleteView



class TodoListView(ListView):
    template_name = 'todo/simpleTodo.html'

    context_object_name = 'todo_list'

    def get_queryset(self):
        return Todo.objects.filter(flag=1)

    def get_context_data(self, **kwargs):
        ctx = super(TodoListView, self).get_context_data(**kwargs)
        ctx['finished_todo_list'] = Todo.objects.filter(flag=0)

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


def addTodo(request):
    if request.method == 'POST':
        user = User.objects.get(id='1')
        atodo = request.POST['todo']
        priority = request.POST['priority']

        form = TodoForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = user
            form.todo = atodo
            form.priority = priority
            form.flag = '1'
            form.save()

        todolist = Todo.objects.filter(flag='1')
        finishtodos = Todo.objects.filter(flag=0)
        return render(request, 'todo/showtodo.html',
                              {'todolist': todolist, 
                               'finishtodos': finishtodos,
                               'form': form})
    else:
        form = TodoForm()

        todolist = Todo.objects.filter(flag=1)
        finishtodos = Todo.objects.filter(flag=0)
        return render(request, 'todo/simpleTodo.html',
                              {'todolist': todolist, 
                               'form': form,
                               'finishtodos': finishtodos})




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

