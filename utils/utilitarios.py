from datetime import datetime
from .models import TabelaIRRF
from decimal import *

# funcoes genericas

def calcula_impostos(valor_bruto, calc_ISS=True, calc_INSS=True, calc_IRRF=True):

    valor_bruto = Decimal(valor_bruto)
    descontos = {'Bruto':valor_bruto, 'ISS': Decimal(0.0), 'INSS':Decimal(0.0),
                 'IR':Decimal(0.0), 'Descontos':Decimal(0.0), 'Liquido':valor_bruto}
    if valor_bruto > 0:

        if calc_ISS:
            descontos['ISS'] = valor_bruto * Decimal(0.05)

        if calc_INSS:
            descontos['INSS'] = valor_bruto * Decimal(0.11)

        if calc_IRRF:
            base_calculo = valor_bruto - descontos['INSS']
            tabelaIRRF = TabelaIRRF.objects.filter(ano=datetime.now().year, ativa=True)[0]
            if base_calculo <= tabelaIRRF.limite_faixa1:
                descontos['IR'] = Decimal(0.0)
            elif base_calculo > tabelaIRRF.limite_faixa1 and base_calculo <= tabelaIRRF.limite_faixa2:
                descontos['IR'] = Decimal((base_calculo * (tabelaIRRF.aliquota_faixa2 /100)) - tabelaIRRF.deducao_faixa2)
            elif base_calculo > tabelaIRRF.limite_faixa2 and base_calculo <= tabelaIRRF.limite_faixa3:
                descontos['IR'] = Decimal((base_calculo * (tabelaIRRF.aliquota_faixa3 / 100)) - tabelaIRRF.deducao_faixa3)
            elif base_calculo > tabelaIRRF.limite_faixa3 and base_calculo <= tabelaIRRF.limite_faixa4:
                descontos['IR'] = Decimal((base_calculo * (tabelaIRRF.aliquota_faixa4 / 100)) - tabelaIRRF.deducao_faixa4)
            else:
                descontos['IR'] = Decimal((base_calculo * (tabelaIRRF.aliquota_faixa5 / 100)) - tabelaIRRF.deducao_faixa5)

        descontos['Descontos'] = descontos['ISS'] + descontos['INSS'] + descontos['IR']
        descontos['Liquido'] = valor_bruto - descontos['Descontos']

    return descontos

def tabela_ativa_IRRF():
    tabela_ativa = None
    tabela = TabelaIRRF.objects.filter(ano=datetime.now().year, ativa=True)
    if tabela.count() > 0:
        tabela_ativa = TabelaIRRF.objects.filter(ano=datetime.now().year, ativa=True)[0]
    return tabela_ativa

def cores(indice):
    cor = ""
    if indice == 'cabecalho' or indice == 'rodape':
        cor = '#ADD8E6'
    elif indice == 'padrao':
        cor = '#F0FFFF'
    elif indice == 'alerta':
        cor = '#FFE4E1'
    elif indice == 'critico':
        cor = '#FFC0CB'
    else:
        cor = '#FFFFFF'
    return cor

# Quebra uma string a partir de uma posicao, sem quebrar palavras
def reticencias(str, posicao):
    frase = ""
    if not ((len(str) == 0) or (posicao == 0)):
        pedacos = str.split()
        for palavra in pedacos:
            if len(frase) == 0:
                frase = palavra + " "
            elif (len(frase) > 0) and (len(frase) < posicao):
                frase = frase + " " + palavra
            else:
                frase = frase + " ..."
                break
    return frase if len(frase) > 0 else str

def extensao_arquivo(nome_arquivo):
    extensao = ""
    nome_quebrado = nome_arquivo.split(".")
    if len(nome_quebrado) >= 2:
        extensao = nome_quebrado[len(nome_quebrado)-1]
    return extensao

class TabelaHTML():

    linha_inicial = 0
    linha_final = 0
    coluna_inicial = 0
    coluna_final = 0
    considera_limites = False
    cabecalho_primeira_linha = True
    class_padrao = ""
    enumera = True
    cabecalho = []

    def gerar_tabela(self, lista):

        celulas_corpo = ""
        celulas_cabecalho = ""

        if not self.considera_limites:
            self.linha_final = len(lista)
            self.coluna_final = len(lista[0])
        else:
            if self.linha_final > 0:
                lista = lista[self.linha_inicial:self.linha_final]
            if self.coluna_final > 0:
                for i, linha in enumerate(lista):
                    lista[i] = linha[self.coluna_inicial:self.coluna_final]


        if (not self.cabecalho) and self.cabecalho_primeira_linha:
            self.cabecalho = lista[0]
            lista = lista[1:]

        if self.cabecalho:
            for coluna in self.cabecalho:
                celulas_cabecalho += self.formata_celula_cabecalho(coluna)
            if self.enumera:
                celulas_cabecalho = self.formata_celula_cabecalho("Nr") + celulas_cabecalho
            celulas_cabecalho = "<tr>{}</tr>".format(celulas_cabecalho)

        for i, linha in enumerate(lista):
            celulas_linha = ""
            for j, coluna in enumerate(linha):
                if j == 0 and self.enumera:
                    celulas_linha = self.formata_celula_linha(i+1)
                celulas_linha += self.formata_celula_linha(coluna)
            celulas_corpo += "<tr>{}</tr>".format(celulas_linha)
        return "<table class='{}'><thead>{}</thead><tbody>{}</tbody></table>".format(self.class_padrao,
                                                                                     celulas_cabecalho,celulas_corpo)

    def formata_celula_cabecalho(self, valor):
        return "<th>{}</th>".format(valor)

    def formata_celula_linha(self, valor):
        return "<td>{}</td>".format(valor)

