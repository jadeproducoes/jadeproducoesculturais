from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tarefas/(?P<id_projeto>[0-9]+)/$', views.tarefas, name='tarefas'),
    url(r'^editatarefa/(?P<id_tarefa>[0-9]+)/$', views.editatarefa, name='editatarefa'),
    url(r'^tarefaemandamento/(?P<id_tarefa>[0-9]+)/$', views.tarefaemandamento, name='tarefaemandamento'),
    url(r'^tarefaconcluida/(?P<id_tarefa>[0-9]+)/$', views.tarefaconcluida, name='tarefaconcluida'),
    url(r'^tarefapendente/(?P<id_tarefa>[0-9]+)/$', views.tarefapendente, name='tarefapendente'),
    url(r'^(?P<id_projeto>[0-9]+)/planilhascarregadas$', views.planilhascarregadas, name='planilhascarregadas'),
    url(r'^(?P<id_projeto>[0-9]+)/exibir_planilha/(?P<id_arquivo>[0-9]+)/$', views.exibir_planilha, name='exibir_planilha'),
    url(r'^(?P<id_projeto>[0-9]+)/carrega_orcamento$', views.carrega_orcamento, name='carrega_orcamento'),
]