from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^$', views.todolist, name='todo'),
    url(r'^$', views.TodoListView.as_view(), name='todo'),
    url(r'^addtodo/$', views.TodoAddView.as_view(), name='add'),
    url(r'^todofinish/(?P<pk>\d+)/$', views.TodoFinishView.as_view(), name='finish'),
    url(r'^todobackout/(?P<pk>\d+)/$', views.TodoBackView.as_view(),  name='backout'),
    url(r'^updatetodo/(?P<pk>\d+)/$', views.UdateTodoView.as_view(), name='update'),
    url(r'^tododelete/(?P<pk>\d+)/$', views.TodoDeleteView.as_view(), name='delete'),
]
