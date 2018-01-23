from django.contrib import admin
from .models import TipoArquivo, FuncaoArquivo, Arquivo
# Register your models here.
admin.site.register(TipoArquivo)
admin.site.register(FuncaoArquivo)
admin.site.register(Arquivo)