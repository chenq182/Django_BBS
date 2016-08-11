from django.conf.urls import include, url

from . import views


app_name = 'bbs'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^forum/(?P<forum_id>[0-9]+)/$', views.forum),
    url(r'^forum/(?P<forum_id>[0-9]+)/(?P<page>[0-9]+)/$',
        views.forum, name='forum'),
    url(r'^forum/(?P<forum_id>[0-9]+)/new/$', views.new_post, name='new_post'),
    url(r'^p/(?P<post_id>[0-9]+)/$', views.post),
    url(r'^p/(?P<post_id>[0-9]+)/(?P<page>[0-9]+)/$',
        views.post, name='post'),
    url(r'^p/(?P<post_id>[0-9]+)/del/$', views.del_post, name='del_post'),
    url(r'^r/(?P<reply_id>[0-9]+)/del/$', views.del_reply, name='del_reply'),
    url(r'^p/(?P<post_id>[0-9]+)/top/(?P<top>[0-9]+)/$',
        views.top_post, name='top_post'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user/$', views.user, name='user'),
]
