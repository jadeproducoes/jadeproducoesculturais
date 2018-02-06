from django.contrib import admin
from .models import *
from orcamento.models import *
# Register your models here.
admin.site.register(Pagamento)
admin.site.register(FormaComprovacao)
admin.site.register(FormaDePagamento)
