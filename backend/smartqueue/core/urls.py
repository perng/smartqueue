from django.conf.urls import patterns, include, url
from core.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smartqueue.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'enqueue/(?P<user_id>\d+)/(?P<queue_id>\d+)', Enqueue.as_view(), name="EnQueue a user"),
    url(r'dequeue/(?P<queue_id>\d+)/(?P<reservation_id>\d+)', Dequeue.as_view(), name="DeQueue a user"),
    url(r'query_position/(?P<queue_id>\d+)/(?P<reservation_id>\d+)', QueryQueue.as_view(), name="Query queue status against a reservation"),
    url(r'query_queue/(?P<queue_id>\d+)', QueryQueue.as_view(), name="Query queue status"),
    url(r'init/', Init.as_view(), name="Populate with test data"),
    url(r'register/', Register.as_view(), name="Register a new user or refresh access token"),

)
