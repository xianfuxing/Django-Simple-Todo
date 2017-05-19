from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^$', views.todolist, name='todo'),
    url(r'^$', views.TodoListView.as_view(), name='todo'),
    url(r'^addtodo/$', views.addTodo, name='add'),
    url(r'^todofinish/(?P<pk>\d+)/$', views.TodoFinishView.as_view(), name='finish'),
    url(r'^todobackout/(?P<pk>\d+)/$', views.TodoBackView.as_view(),  name='backout'),
    url(r'^updatetodo/(?P<id>\d+)/$', views.updatetodo, name='update'),
    url(r'^tododelete/(?P<id>\d+)/$', views.tododelete, name='delete'),
]
