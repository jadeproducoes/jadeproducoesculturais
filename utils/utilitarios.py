from datetime import datetime
from enum import Enum

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

def enumera_linhas_lista(lista=[], saltos=[], linha_inicial=1):
    '''
    Enumera as linhas de uma lista.

    Faz a numeracao das linhas de uma lista admitindos saltos nas nuemracoes
    :param lista: lista que deve ser numerada
    :param saltos: indica os saltos na numeracao
    :return: lista nuerada
    '''

    if isinstance(lista, list):
        for i, linha in enumerate(lista):
            if linha_inicial in saltos:
                linha_inicial += 1
            if isinstance(linha, str):  # nao tem como diferenciar lista de str? tem que fazer o teste antes?
                lista[i] = [linha_inicial, linha]
            elif isinstance(linha, list):
                lista[i] = [linha_inicial] + linha
            else:
                lista[i] = [linha_inicial, linha]
            linha_inicial += 1

    return lista


def a_z_maiusculo():
    return [chr(x) for x in range(ord("A"), ord("Z")+1)]

def a_z_minusculo():
    return [chr(x) for x in range(ord("a"), ord("z")+1)]

def intervalo_letras(letra_inicial='A', letra_final='Z', maiscula=True):
    intervalo = []
    if isinstance(letra_inicial, str) and isinstance(letra_final, str):
        letra_inicial = letra_inicial.upper() if maiscula else letra_inicial.lower()
        letra_final = letra_final.upper() if maiscula else letra_final.lower()
        intervalo = [chr(x) for x in range(ord(letra_inicial), ord(letra_final) + 1)]
    return intervalo

def intervalo_com_excecoes(letra_inicial='A', letra_final='Z', maiscula=True, lista_excecoes=[]):
    intervalo = intervalo_letras(letra_inicial, letra_final, maiscula)
    if intervalo and lista_excecoes:
        lista_intervalos = []
        for excecao in lista_excecoes:
            if isinstance(excecao, str):
                if "-" in excecao:
                    inicio_excecao = excecao.split("-")[0] if len(excecao.split("-")[0]) == 1 else excecao.split("-")[0][0]
                    fim_excecao = excecao.split("-")[1] if len(excecao.split("-")[1]) == 1 else excecao.split("-")[1][0]
                    inicio_excecao = inicio_excecao.upper() if maiscula else inicio_excecao.lower()
                    fim_excecao = fim_excecao.upper() if maiscula else fim_excecao.lower()
                    lista_intervalos += intervalo_letras(inicio_excecao, fim_excecao, maiscula)
                else:
                    lista_intervalos += [excecao[0].upper() if maiscula else excecao[0].lower()]
        if lista_intervalos:
            for del_letra in lista_intervalos:
                intervalo.remove(del_letra)
    return intervalo

def lista_de_intervalos(descrisao_intervalo):
    '''
    Calcula os intervalos de indices a partir de uma string Ex.: 3-5;11;21-23 retorna [3,4,5,11,21,22,23].

    :param descrisao_intervalo:
    :return: lista representando os intervalos
    '''
    lista_intervalos = []
    if descrisao_intervalo:
        blocos_intervalo = descrisao_intervalo.split(";")
        #if len(blocos_intervalo) == 1:
        #    lista_intervalos += [int(blocos_intervalo[0])]
        #else:
        for elemento in blocos_intervalo:
            if "-" in elemento:
                try:
                    elementos = elemento.split("-")
                    inicio = int(elementos[0])
                    fim = int(elementos[1])
                    lista_intervalos += range(inicio, fim+1)
                except ValueError:
                    print("Erro nos intervalos de linha. Revise: '{}'. Ex.:'3-5;11;21-23'".format(descrisao_intervalo))
                    raise
            else:
                lista_intervalos += [int(elemento)]
    return sorted(lista_intervalos)

def nr_esta_no_intervalo(nr, descrisao_intervalo):
    '''
    Verifica se um determinado número está presente nos intervalos escritos como 3-5;11;21-23.

    :param nr: numero que se desenja descobrir se esta no intervalo
    :param descrisao_intervalo:
    :return: True se o numero estiver no intervalo; False se nao estiver
    '''
    pertence_intervalo = False
    try:
        nr = nr if isinstance(nr, int) else int(nr)
    except:
        raise ValueError("O número {} não pode ser convertido num inteiro".format(nr))

    if nr in lista_de_intervalos(descrisao_intervalo):
        pertence_intervalo = True

    return pertence_intervalo

class TabelaHTML():

    linha_inicial = 0
    linha_final = 0
    coluna_inicial = 0
    coluna_final = 0
    considera_limites = False
    cabecalho_primeira_linha = False
    class_padrao = ""
    numera_linhas = True
    cabecalho = []
    cabecalho_tipo_planilha = True
    inicio_contagem = 0
    cor_especial = None
    intevalo_marcacao_cor_especial = []
    cor_padrao_linhas = ""

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

        if self.cabecalho_tipo_planilha:
            self.cabecalho = [chr(indice) for indice in range(65, (65 + len(lista[0])))]

        if self.cabecalho:
            for coluna in self.cabecalho:
                celulas_cabecalho += self.formata_celula_cabecalho(coluna)
            if self.numera_linhas:
                celulas_cabecalho = self.formata_celula_cabecalho("Nr") + celulas_cabecalho
            celulas_cabecalho = "<tr>{}</tr>".format(celulas_cabecalho)

        if self.inicio_contagem > 0:
            self.intevalo_marcacao_cor_especial = [(i-self.inicio_contagem) for i in self.intevalo_marcacao_cor_especial]

        for i, linha in enumerate(lista):
            celulas_linha = ""
            for j, coluna in enumerate(linha):
                if j == 0 and self.numera_linhas:
                    celulas_linha = self.formata_celula_linha(i+self.inicio_contagem, True)
                celulas_linha += self.formata_celula_linha(coluna)
            cor = self.cor_especial if self.intevalo_marcacao_cor_especial and \
                                       i in self.intevalo_marcacao_cor_especial else self.cor_padrao_linhas
            celulas_corpo += "<tr bgcolor='{}'>{}</tr>".format(cor, celulas_linha)
        return "<table class='{}'><thead>{}</thead><tbody>{}</tbody></table>".format(self.class_padrao,
                                                                                     celulas_cabecalho,celulas_corpo)

    def formata_celula_cabecalho(self, valor, negrito=False):
        celula = "<th><b>{}<b></th>" if negrito else "<th>{}</th>"
        return celula.format(valor)

    def formata_celula_linha(self, valor, negrito=False):
        celula = "<td><b>{}</b></td>" if negrito else "<td>{}</td>"
        return celula.format(valor)




class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        choices = list()

        # Loop thru defined enums
        for item in cls:
            choices.append((item.value, item.name))

        # return as tuple
        return tuple(choices)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value


# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# [dExtenso.py]
# Implementa o algoritmo geral de escrita
# por extenso de um número qualquer.
#
# [Autor]
# Marcos Paulo Ferreira (Daemonio)
# undefinido gmail com
# https://daemoniolabs.wordpress.com
#
# Versão 1.0 by daemonio @Thu Sep 12 22:22:06 BRT 2013
# Versão 1.1 by daemonio @Sat Dec 20 23:41:50 BRST 2014
#   + consertado bug no "cem"

class dExtenso():
    trioextenso = ()
    classextenso = ()

    def __init__(self):
        self.trioextenso = (
            ("dummy", "um", "dois", "três", "quatro", "cinco", "seis", "sete",
             "oito", "nove"),
            ("dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis",
             "dezessete", "dezoito", "dezenove"),
            ("dummy", "dummy", "vinte", "trinta", "quarenta", "cinquenta",
             "sessenta", "setenta", "oitenta", "noventa"),
            ("dummy", "cento", "duzentos", "trezentos", "quatrocentos",
             "quinhentos", "seiscentos", "setecentos", "oitocentos",
             "novecentos"))
        self.classextenso = (
            "dummy", "mil", "milh", "bilh", "trilh", "quatrilh",
            "quintilh", "sextilh", "septilh", "octilh",
            "nonilh", "decilh", "undecilh", "duodecilh",
            "tredecilh", "quatordecilh", "quindecilh",
            "sexdecilh", "setedecilh", "octodecilh",
            "novedecilh", "vigesilh")

    def escrever_trio_extenso(self, trio):
        """
        Retorna um trio por extenso.

        Entrada: trio na forma de string.

        Retorno: trio em extenso.
        """
        saida = []

        if trio == '100':
            # Erro antigo aqui. Consertado usando "return"
            return 'cem'
        elif trio == '000':
            return 'zero'
        else:
            c, d, u = trio
            c, d, u = int(c), int(d), int(u)

            if c != 0:
                saida.append(self.trioextenso[3][c])
            if d == 1:
                saida.append(self.trioextenso[1][u])
            else:
                if d != 0:
                    saida.append(self.trioextenso[2][d])
                if u != 0:
                    saida.append(self.trioextenso[0][u])
        return ' e '.join(saida)

    def nao_e_ultimo_trio(self, totalTrios, contador):
        """
        Retorna verdadeiro se o trio indicado pelo contador
        não é o último (isso é, não é o mais à direita).

        Entrada: Número total de trios e o contador.

        Retorno: Verdadeiro se o trio NÃO é o último e
        falso caso contrário.
        """
        return contador < (totalTrios - 1)

    def trio_a_esquerda_eq_zero(self, trioLista, contador):
        """
        Retorna verdadeiro se o trio à esquerda do trio
        indicado pelo contador é igual a zero.

        Entrada: Os trios em forma de Lista e o contador.

        Retorno: Verdadeiro se o trio à esquerda do contador
        for zero e falso caso contrário.
        """

        # Contador igual a zero indexa o elemento mais à direita,
        # por isso devemos acrescentar tamanho da lista.
        t = len(trioLista) - 1
        return trioLista[t - contador - 1] == '000'

    def get_decimal_extenso(self, num, moeda='', centavos='', quebradelinhas=0):
        '''
        Funcao acrescentada por Adriano Campos para lidar com numeros decimais.

        :param num:
        :param quebradelinhas:
        :return: numero decimal por extenso
        '''
        nr_extenso = ""
        if "." in num:
            composicao = num.split(".")
            principal = self.getExtenso(composicao[0]) if int(composicao[0])>0 else ""
            decimal = self.getExtenso(composicao[1]) if int(composicao[1])>0 else ""
            if principal:
                principal += (" " + moeda) if moeda else ""
            if decimal:
                decimal += (" " + centavos) if centavos else ""
        if moeda or centavos:
            nr_extenso = "{} e {}".format(principal, decimal) if principal and decimal else "{}{}".format(principal,decimal)
        else:
            nr_extenso = "{} virgula {}".format(principal, decimal) if principal and decimal else "{}{}".format(principal,
                                                                                                          decimal)
        return nr_extenso


    def getExtenso(self, num, quebradelinhas=0):
        """
        Algoritmo principal. Recebe um número na forma de
        string e retorna sua escrita em extenso.

        Entrada: Número na forma de string e uma flag que, se
        tiver o valor 0 (zero), o extenso é retornado em uma
        só linha. Um valor 1 (um) faz o extenso ser quebrado
        em várias linhas.

        Retorno: O número de entrada em extenso na forma de
        string.
        """

        # Remove os zeros iniciais e faz padding
        # para números com quantidade de algarismos
        # não múltipla de 3
        num = num.lstrip('0')
        pad = 3 - len(num) % 3
        if pad < 3: num = '0' * pad + num

        it = iter(num)
        trioLista = [''.join([a, b, c]) for a, b, c in zip(it, it, it)]

        if len(trioLista) > len(self.classextenso):
            raise IndexError('Número muito grande')

        contador = 0
        saida = ''
        extensofinal = ''

        for trio in reversed(trioLista):
            trioInt = int(trio)

            if trioInt > 0:
                saida = self.escrever_trio_extenso(trio)
                if contador > 0:
                    saida = saida + ' ' + self.classextenso[contador]
                if contador > 1:
                    if trioInt > 1:
                        saida = saida + 'ões'
                    else:
                        saida = saida + 'ão'
                if quebradelinhas == 0:
                    if self.nao_e_ultimo_trio(len(trioLista), contador):
                        if self.trio_a_esquerda_eq_zero(trioLista, contador):
                            saida = ' e ' + saida
                        elif trioInt >= 100:
                            saida = ', ' + saida
                        else:
                            saida = ' e ' + saida
                else:
                    saida = saida + '\n'

                extensofinal = saida + extensofinal
            contador = contador + 1
        return extensofinal.rstrip('\n')