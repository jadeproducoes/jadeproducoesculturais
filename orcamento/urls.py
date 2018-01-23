# URLs do aplicativo orçamento

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^listaorcamentos/(?P<id>[0-9]+)/$', views.listaorcamentos, name='listaorcamentos'),
    url(r'^exibeorcamento/(?P<id>[0-9]+)/$', views.exibeorcamento, name='exibeorcamento'),
    url(r'^ultimo/$', views.ultimoorcamento, name='ultimoorcamento'),
    url(r'^primeirarubricadalista/(?P<id>[0-9]+)/$', views.primeirarubricadalista, name='primeirarubricadalista'),
    url(r'^ultimarubricadalista/(?P<id>[0-9]+)/$', views.ultimarubricadalista, name='ultimarubricadalista'),
    url(r'^umarubricacima/(?P<id>[0-9]+)/$', views.umarubricacima, name='umarubricacima'),
    url(r'^umarubricabaixo/(?P<id>[0-9]+)/$', views.umarubricabaixo, name='umarubricabaixo'),
    url(r'^editarubrica/(?P<id>[0-9]+)/$', views.editarubrica, name='editarubrica'),
    url(r'^novarubrica/(?P<id>[0-9]+)/$', views.novarubrica, name='novarubrica'),
    url(r'^exiberubrica/(?P<id>[0-9]+)/(?P<id_orcamento>[0-9]+)/$', views.exiberubrica, name='exiberubrica'),
    url(r'^eliminarubrica/(?P<id>[0-9]+)/(?P<id_orcamento>[0-9]+)/$', views.eliminarubrica, name='eliminarubrica'),
    url(r'^ativarorcamento/(?P<id>[0-9]+)/$', views.ativarorcamento, name='ativarorcamento'),
    url(r'^desativarorcamento/(?P<id>[0-9]+)/$', views.desativarorcamento, name='desativarorcamento'),
    url(r'^controleorcamentario/(?P<id_projeto>[0-9]+)/$', views.controleorcamentario, name='controleorcamentario'),
    url(r'^download_controle_excel/(?P<id_projeto>[0-9]+)/$', views.download_controle_excel, name='download_controle_excel'),
    url(r'^carrega_orcamento/$', views.carrega_orcamento, name='carrega_orcamento'),
    url(r'^novoorcamento/(?P<id_projeto>[0-9]+)/$', views.novoorcamento, name='novoorcamento'),
    url(r'^planilhascarregadas/$', views.planilhascarregadas, name='planilhascarregadas'),
    url(r'^exibir_planilha/(?P<id_arquivo>[0-9]+)/$', views.exibir_planilha, name='exibir_planilha'),

]