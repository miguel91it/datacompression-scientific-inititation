# encoding: utf-8

import sys

#funcao que convert o caractere new_line para pipe "|"
def converteCaractere(str):
	if len(str) == 0:
		return "/EOF/"
	#if str == "\n":
	#	return "|"
	else:
		return str

def leCaractereArquivoConvertendo():
	char = (arquivo_entrada.read((1)).decode)("latin1")

	return converteCaractere(char)

#busca no dicionario a string str e retorna a posicao de ocorrencia
def buscaNoDicionario(dicionario, str):

	#tenta encontrar a string str no dicionario
	try:
		return dicionario.index(str)

	#se nao conseguir, retorna -1
	except ValueError:
		return -1

#adiciona uma string no dicionario
def adicionaNoDicionario(dicionario, str):

	dicionario.append(str)

num_argv = 0

for elemento in sys.argv:
    num_argv += 1

if num_argv > 1:
    arquivo_entrada = open(sys.argv[1], "r")
    #arquivo_entrada = open("C:\Users\migue\Dropbox\UFABC\PDPD\Programas\Programas Pesquisa\LZ78\compactar.txt", "r")
else:
   sys.exit("Programa executado sem arquivo a ser compactado")

#direciona cursos para o inicio do arquivo
arquivo_entrada.seek(0)

chars = leCaractereArquivoConvertendo()

#EOF no Python é uma string de len = 0
EOF = "/EOF/"

if chars == "/EOF/":
    sys.exit("Arquivo Vazio!")

#Cria Arquivo novo no modo append
#arquivo_saida = open("C:\Users\migue\Dropbox\UFABC\PDPD\Programas\Programas Pesquisa\LZ78\os_lusiadas_compactado.txt", "a")
#arquivo_saida = open("/home/joao/Área de Trabalho/os_lusiadas_compactado.lz78", "a")
arquivo_saida = open(sys.argv[1][0 : len(sys.argv[1]) - 3] + "l78", "w")

#cria objeto dicionario lz78
dicionario78 = []

adicionaNoDicionario(dicionario78, "")

arquivo_entrada.seek(0)

chars = leCaractereArquivoConvertendo()

#i = 1

while True:

	#print i, " bytes lidos"

	posicaoNoDicionario = buscaNoDicionario(dicionario78, chars)

	#se encontrar o padrão no dicionario
	if posicaoNoDicionario != -1:

		chars += leCaractereArquivoConvertendo()

		ultimaPosicaoLida = posicaoNoDicionario

	else:

		#adiciona a sequencia de caracterers no dicionario
		adicionaNoDicionario(dicionario78, chars)

		#cria o output (0, chars)
		if len(chars) == 1:
			chars_compactados = "{0|" + chars + "}"

		#cria o output (ultimaPosicaoLida, chars)
		else:
			chars_compactados = "{" + str(ultimaPosicaoLida) + "|"

			if ("/EOF/" in chars) == True:
				chars_compactados += chars[len(chars) - 5 : len(chars)] + "}"

			else:
				chars_compactados += chars[len(chars) - 1] + "}"


		arquivo_saida.write((chars_compactados).encode("latin1"))

		chars = leCaractereArquivoConvertendo()


	if chars == "/EOF/":

		if dicionario78[len(dicionario78) - 1].find("/EOF/") == -1:

			adicionaNoDicionario(dicionario78, "/EOF/")

			chars_compactados = "{0|/EOF/}"

			arquivo_saida.write(chars_compactados)

		print "Fim do Programa - Compressao Concluida"

		break

	#i += 1

#fecha o arquivo
arquivo_entrada.close()
arquivo_saida.close()