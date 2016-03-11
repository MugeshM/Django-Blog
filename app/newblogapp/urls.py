from django.conf.urls import url
from django.contrib import admin
from app.newblogapp import views
urlpatterns = [
    url(r'^$', views.index,name="index"),
    url(r'^(?P<blogpost_id>[0-9]+)/$', views.detail, name='postdetail'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='postdetail'),
    #url(r'^newpost/',TemplateView.as_view(template_name='main/newpost.html'),name="newpost"),
    url(r'^post/', views.post, name='insertpost'),
    url(r'^(?P<blogpost_id>[0-9]+)/postcomment/$', views.postcomment, name='insertcomment'),
    url(r'^newpost/', views.newpost, name='newpost'),
    url(r'^login/', views.login, name='login'),
    url(r'^logincheck/', views.logincheck, name='logincheck'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^signupcheck/', views.signupcheck, name='signupcheck'),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),
    url(r'^session/',views.session_lost,name="session_lost")
]