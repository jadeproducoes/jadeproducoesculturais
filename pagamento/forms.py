from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import *
from django.core.validators import ValidationError
from decimal import *
from datetime import date
from utils import *

class FormularioItemPagamento(forms.ModelForm):

    def clean_valor_bruto_pagamento(self):
        valor_item = self.instance.valor_bruto_pagamento
        valor_pagamento = self.cleaned_data.get('valor_bruto_pagamento')
        if valor_pagamento > valor_item:
            if (valor_pagamento - valor_item) > self.instance.saldo_rubrica:
                excesso = (valor_pagamento - valor_item) - self.instance.saldo_rubrica
                msg = "O valor do pagamento excede o valor total da rubrica. Pagamento excede R$ {excesso:2.2f}".format(excesso=excesso)
                raise ValidationError(_(msg))
        return valor_pagamento

    class Meta:
        model = ItemPagamento
        fields = '__all__'
        exclude = ['id_pagamento', 'id_rubrica']

class FormularioDescontos(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = '__all__'
        exclude = ['id_pessoa', 'id_projeto', 'id_orcamento', 'data_pagamento', 'pendente', 'observacoes']

class FormularioBeneficiario(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = '__all__'
        exclude = ['id_projeto', 'id_orcamento', 'data_pagamento', 'pendente', 'observacoes', 'cobrar_ISS', 'cobrar_INSS']

class FormularioFormaPagamento(forms.ModelForm):

    def clean(self):
        data_emissao = self.cleaned_data.get('data_emissao')
        data_efetivacao = self.cleaned_data.get('data_efetivacao')
        if data_efetivacao:
            if data_efetivacao < data_emissao:
                raise ValidationError(_("A data de efetivação tem que ser maior que a data de emissão"))
            if data_efetivacao > date.today():
                raise ValidationError(_("A data de efetivação deve ser, no máximo, a data atual"))

    def clean_valor(self):
        parcela = Decimal(self.cleaned_data.get('valor'))
        pagamento = self.instance.id_pagamento
        valor_pagamento = Decimal(round(pagamento.valor_liquido,2))
        excesso = Decimal(parcela - self.instance.valor)
        soma_parcelas = Decimal(pagamento.soma_fomas_pagamento)
        print("Pagamento: {} Parcela: {} Excesso: {} Parcelas {} ".
              format(valor_pagamento, parcela, excesso, soma_parcelas))

        if excesso > 0:
            if (soma_parcelas + excesso) > valor_pagamento:
                valor_maximo_parcela = valor_pagamento - soma_parcelas
                msg = "Com esta parcela (R$ {parcela:2.2f}) a soma dos meios de pagamento excedem o valor " \
                      "do pagamento R$ {pagamento:2.2f}. Volte ao pagamento e resolva o problema!".\
                        format(parcela=parcela, pagamento=valor_pagamento)
                raise ValidationError(_(msg))
        else:
            if soma_parcelas > valor_pagamento:
                msg = "Com a parcela de R$ {parcela:2.2f} o total dos meios de pagamento torna-se maior que o valor " \
                      "total do pagamento que é de R$ {pagamento:2.2f}. Volte ao pagamento e resolva o problema!".\
                        format(parcela=parcela, pagamento=valor_pagamento)
                raise ValidationError(_(msg))
        return parcela

    class Meta:
        model = FormaDePagamento
        fields = '__all__'
        exclude = ['id_pagamento']


class FormularioFormaComprovacao(forms.ModelForm):

    class Meta:
        model = FormaComprovacao
        fields = '__all__'
        exclude = ['id_pagamento']

    def clean(self):
        data_emissao = self.cleaned_data.get('data_emissao')
        data_efetivacao = self.cleaned_data.get('data_recebimento')
        if data_efetivacao:
            if data_efetivacao < data_emissao:
                raise ValidationError(_("A data de recebimento tem que ser maior que a data de emissão"))
            if data_efetivacao > date.today():
                raise ValidationError(_("A data de recebimento deve ser, no máximo, a data atual"))

    # verifica se o beneficiario e pessoa fisica ou juridica para efeito de emissao de documento de comprovacao
    def clean_tipo_comprovacao(self):

        tipo_comprovacao = self.cleaned_data.get('tipo_comprovacao')
        print("Primeira escolha %s" % tipo_comprovacao)

        formas_comprovacao = tipocomprovacao()
        pessoa_fisica = self.instance.id_pagamento.id_pessoa.pessoa_fisica
        msg = ""
        lanca_erro = False
        for tipo in formas_comprovacao:
            if pessoa_fisica:
                if tipo_comprovacao == tipo[0]:
                    if tipo[0] not in ('RP', 'RB'):
                        lanca_erro = True
                        msg = "O(a) benefiário(a) é pessoa física: só pode fazer comprovação por meio de RPA"
            else:
                if tipo_comprovacao == tipo[0]:
                    if tipo[0] not in ('NF', 'CP'):
                        lanca_erro = True
                        msg = "O(a) benefiário(a) é pessoa jurídica e tem que emitir Nota Fiscal"

        if lanca_erro:
            raise ValidationError(_(msg))

        return tipo_comprovacao