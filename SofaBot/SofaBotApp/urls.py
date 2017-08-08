from django.conf.urls import url


from . import views

app_name = 'SofaBotApp'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^updateActualValue/$', views.updateActualValue, name='updateActualValue'),
    url(r'^addBot/$', views.addBot, name='addBot'),
    url(r'^(?P<exchange_id>[0-9]+)/startExchange/$', views.startExchange, name='startExchange'),
    url(r'^(?P<exchange_id>[0-9]+)/stopExchange/$', views.stopExchange, name='stopExchange'),
    url(r'^getOrderStateList/$', views.getOrderStateList, name='getOrderStateList'),
]