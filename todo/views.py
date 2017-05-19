from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import Http404
from .models import Todo

from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, UpdateView



class TodoListView(ListView):
    template_name = 'todo/simpleTodo.html'

    context_object_name = 'todo_list'

    def get_queryset(self):
        return Todo.objects.filter(flag=1)

    def get_context_data(self, **kwargs):
        ctx = super(TodoListView, self).get_context_data(**kwargs)
        ctx['finished_todo_list'] = Todo.objects.filter(flag=0)

        return ctx


# def todofinish(request, id=''):
#     todo = Todo.objects.get(id=id)
#     if todo.flag == '1':
#         todo.flag = '0'
#         todo.save()
#         return HttpResponseRedirect('/todos/')
#     todolist = Todo.objects.filter(flag=1)
#     return render(request, 'todo/simpleTodo.html',
#                            {'todolist': todolist})

class TodoFinishView(SingleObjectMixin, View):
    model = Todo
    success_url = '/todos/'

    def get(self, request, *args, **kwargs):
        todo = self.get_object()
        if todo.flag == '1':
            todo.flag = '0'
            todo.save()
        return HttpResponseRedirect('/todos/')

def todoback(request, id=''):
    todo = Todo.objects.get(id=id)
    if todo.flag == '0':
        todo.flag = '1'
        todo.save()
        return HttpResponseRedirect('/todos/')
    todolist = Todo.objects.filter(flag=1)
    return render(request, 'todo/simpleTodo.html', {'todolist': todolist})

def tododelete(request, id=''):
    try:
        todo = Todo.objects.get(id=id)
    except Exception:
        raise Http404
    if todo:
        todo.delete()
        return HttpResponseRedirect('/todos/')
    todolist = Todo.objects.filter(flag=1)
    return render(reqeust, 'todo/simpleTodo.html', {'todolist': todolist})

def addTodo(request):
    if request.method == 'POST':
        atodo = request.POST['todo']
        priority = request.POST['priority']
        user = User.objects.get(id='1')
        todo = Todo(user=user, todo=atodo, priority=priority, flag='1')
        todo.save()
        todolist = Todo.objects.filter(flag='1')
        finishtodos = Todo.objects.filter(flag=0)
        return render(request, 'todo/showtodo.html',
                              {'todolist': todolist, 
                               'finishtodos': finishtodos})
    else:
        todolist = Todo.objects.filter(flag=1)
        finishtodos = Todo.objects.filter(flag=0)
        return render(request, 'todo/simpleTodo.html',
                              {'todolist': todolist, 
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

