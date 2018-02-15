from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^pagamentos/(?P<id_projeto>[0-9]+)/$', views.pagamentos, name='pagamentos'),
    url(r'^pagamento/(?P<id_pagamento>[0-9]+)/$', views.pagamento, name='pagamento'),
    url(r'^novopagamento/(?P<id_projeto>[0-9]+)/$', views.novopagamento, name='novopagamento'),
    url(r'^eliminapagamento/(?P<id_pagamento>[0-9]+)/$', views.eliminapagamento, name='eliminapagamento'),
    url(r'^novarubricapagamento/(?P<id_pagamento>[0-9]+)/$', views.novarubricapagamento, name='novarubricapagamento'),
    url(r'^novaformapagamento/(?P<id_pagamento>[0-9]+)/$', views.novaformapagamento, name='novaformapagamento'),
    url(r'^novaformacomprovacao/(?P<id_pagamento>[0-9]+)/$', views.novaformacomprovacao, name='novaformacomprovacao'),
    url(r'^listarubricasprojeto/(?P<id_pagamento>[0-9]+)/$', views.listarubricasprojeto, name='listarubricasprojeto'),
    url(r'^atualizarubricas/(?P<id_pagamento>[0-9]+)/$', views.atualizarubricas, name='atualizarubricas'),
    url(r'^eliminaitempagamento/(?P<id_item>[0-9]+)/$', views.eliminaitempagamento, name='eliminaitempagamento'),
    url(r'^editaitempagamento/(?P<id_item>[0-9]+)/$', views.editaitempagamento, name='editaitempagamento'),
    url(r'^editadescontos/(?P<id_pagamento>[0-9]+)/$', views.editadescontos, name='editadescontos'),
    url(r'^cancelardescontos/(?P<id_pagamento>[0-9]+)/$', views.cancelardescontos, name='cancelardescontos'),
    url(r'^alterarbenefiario/(?P<id_pagamento>[0-9]+)/$', views.alterarbenefiario, name='alterarbenefiario'),
    url(r'^novaformapagamento/(?P<id_pagamento>[0-9]+)/$', views.novaformapagamento, name='novaformapagamento'),
    url(r'^editaformapagamento/(?P<id_forma_pagamento>[0-9]+)/$', views.editaformapagamento, name='editaformapagamento'),
    url(r'^eliminaformapagamento/(?P<id_forma_pagamento>[0-9]+)/$', views.eliminaformapagamento, name='eliminaformapagamento'),
    url(r'^novaformacomprovacao/(?P<id_forma_comprovacao>[0-9]+)/$', views.novaformacomprovacao, name='novaformacomprovacao'),
    url(r'^editaformacomprovacao/(?P<id_forma_comprovacao>[0-9]+)/$', views.editaformacomprovacao, name='editaformacomprovacao'),
    url(r'^eliminaformacomprovacao/(?P<id_forma_comprovacao>[0-9]+)/$', views.eliminaformacomprovacao, name='eliminaformacomprovacao'),
    url(r'^projeto/(?P<id_projeto>[0-9]+)/emitir_rpa/(?P<id_pagamento>[0-9]+)/$', views.emitir_rpa, name='emitir_rpa'),
]