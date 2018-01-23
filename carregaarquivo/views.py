from .forms import FormUploadArquivo
from django.core.files.storage import FileSystemStorage
from utils.utilitarios import *
from openpyxl import load_workbook
import xlrd

class Carregaarquivo():

    formulario = FormUploadArquivo()
    cabecalho_formulario = '<form method="post" enctype="multipart/form-data"><table class="table">'
    rodape_formulario = '</table><button type="submit">Carregar</button></form>'

    def model_form_upload(self, request):
        if request.method == 'POST':
            form_upload = FormUploadArquivo(request.POST, request.FILES)
            if form_upload.is_valid():
                form_upload.save()
                self.formulario = None
            else:
                self.formulario = form_upload
        return self.formulario

    def caminho_midias(self):
        fs = FileSystemStorage()
        return fs.base_location + "\\"

    def caminho_completo_arquivo(self, nome):
        return self.caminho_midias() + nome

    def arquivo_midia_existe(self, nome):
        fs = FileSystemStorage()
        return True if fs.exists(self.caminho_completo_arquivo(nome)) else False


class FiltroImportacao():
    nome_arquivo = ""
    tipo_arquivo = ""

class ImportaPlanilha(FiltroImportacao):

    linha_inicial = 1
    linha_final = 1
    coluna_inicial = 'A'
    coluna_final = 'A'

    __idx_linha_inicial = 0
    __idx_linha_final = 0
    __idx_coluna_inicial = 0
    __idx_coluna_final = 0

    para_se_linha_vazia = True

    def importa_planilha(self, nome):
        ca = Carregaarquivo()
        ws = False
        lista_planilha = []
        if ca.arquivo_midia_existe(nome):

            # Verifica se os dados foram inseridos indevidamente
            if (self.linha_inicial <= 0) or (self.linha_final <= 0):
                raise ValueError('A linha inicial ou a linha final é menor ou igual a zero')
            elif (self.linha_inicial > self.linha_final) or \
                    (ord(self.coluna_inicial.upper()) > ord(self.coluna_final.upper())):
                raise ValueError('A linha inicial é maior que a linha final ou a coluna inicial é maior que a coluna final')

            if extensao_arquivo(nome) == 'xlsx':
                wb = load_workbook(ca.caminho_completo_arquivo(nome))
                ws = wb.active
                linhas = range(self.linha_inicial, self.linha_final+1)
                colunas = [chr(x) for x in range(ord(self.coluna_inicial.upper()), ord(self.coluna_final.upper())+1)]
                for linha in linhas:
                    celulas_linhas = []
                    for coluna in colunas:
                        celulas_linhas.append(ws[coluna+str(linha)].value)
                    lista_planilha.append(celulas_linhas)

            if extensao_arquivo(nome) == 'xls':
                # faz a conversao de coluna para poder lidar com a bilioteca xlrd
                self.__idx_linha_inicial = self.linha_inicial - 1
                self.__idx_linha_final = self.linha_final
                self.__idx_coluna_inicial = self.converte_coluna_em_indice(self.coluna_inicial)
                self.__idx_coluna_final = self.converte_coluna_em_indice(self.coluna_final)
                print("Nome: {}\nLI, LF, CI e CF: {} - {} - {} - {}".format(nome,self.__idx_linha_inicial,
                                                                            self.__idx_linha_final,
                                                                            self.__idx_coluna_inicial,
                                                                            self.__idx_coluna_final))
                wb = xlrd.open_workbook(ca.caminho_completo_arquivo(nome))
                ws = wb.sheet_by_index(0)
                for nr_linha in range(self.__idx_linha_inicial, self.__idx_linha_final):
                    linha = ws.row_values(nr_linha)[self.__idx_coluna_inicial:self.__idx_coluna_final + 1]
                    lista_planilha.append(linha)
        return lista_planilha

    def converte_coluna_em_indice(self, str_coluna):
        '''
        Converte colunas indicadas como letras (ex. 'A', 'AD'), para indice de coluna numerico.

        A funcao faz a conversao para manter a compatibilidade de tratamento entre diferentes
        pacotes que tratam da importacao ou expotacao de planilhas Excel
        :param str_coluna: um indice de coluna (ex.: 'A', 'AD')
        :return: indice numerico da coluna iniciando em 0 (zero)
        '''
        indice = 0
        if str_coluna and type(str_coluna) is str:
            base = 26
            multiplicadores = range(1, 27)
            colunas_AZ = [chr(x+64) for x in multiplicadores]
            if len(str_coluna) == 1:
                if str_coluna in colunas_AZ:
                    indice = colunas_AZ.index(str_coluna.upper())
            elif len(str_coluna) == 2:
                str_multiplicacao = str_coluna[0]
                str_soma = str_coluna[1]
                if (str_multiplicacao in colunas_AZ) and (str_soma in colunas_AZ):
                    indice = ((colunas_AZ.index(str_multiplicacao) + 1) * base) + colunas_AZ.index(str_soma)
            else:
                raise IndexError('A função converte_coluna_em_indice() não trata colunas com mais de duas letras. Ex.: AAA')

        return indice


