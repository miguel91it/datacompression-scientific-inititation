# encoding: utf-8

import sys

from collections import deque

def leCaractereDoArquivo():
	return (arquivo_entrada.read((1)).decode)("latin1")

def adicionaNaJanela(janela, string):

	if len(string) == 1:
		janela.appendleft(string)

	elif len(string) > 1:

		for char in string:

			janela.appendleft(char)


num_argv = 0

for element in sys.argv:
    num_argv += 1

if num_argv > 1:
    arquivo_entrada = open(sys.argv[1], "r")
    #arquivo_entrada = open("C:\Users\migue\Dropbox\UFABC\PDPD\Programas\Programas Pesquisa\LZ77\os_lusiadas_compactado.txt", "r")
    #arquivo_entrada = open("/home/joao/Área de Trabalho/os_lusiadas_descompactado.txt", "r")


else:
   sys.exit("Programa executado sem arquivo a ser compactado")

#direciona cursos para o inicio do arquivo
arquivo_entrada.seek(0)

char = leCaractereDoArquivo()

#EOF no Python é uma string de len = 0
EOF = 0

if len(char) == EOF:
    sys.exit("Arquivo Vazio!")

#Cria Arquivo novo no modo append
#arquivo_saida = open("C:\Users\migue\Dropbox\UFABC\PDPD\Programas\Programas Pesquisa\LZ77\os_lusiadas_descompactado.txt", "a")
#arquivo_saida = open("/home/joao/Área de Trabalho/os_lusiadas_descompactado.lz77", "a")
arquivo_saida = open(sys.argv[1][0 : len(sys.argv[1]) - 3] + "u77", "w")

janela = deque(maxlen = 128)

arquivo_entrada.seek(0)

#add aqui a obtencao do tamanho do dicionario {maxlen}

while True:

	str_compactada = ""

	char_lido = leCaractereDoArquivo()

	if len(char_lido) == EOF:
		break

	#descobre posicao, len e char da tripla {offset, len, char}
	while char_lido != "}":

		str_compactada += char_lido

		char_lido = leCaractereDoArquivo()

	else:
		str_compactada += char_lido


	offset = int((str_compactada[1:len(str_compactada)-1].split("|"))[0])
	tamanho = int((str_compactada[1:len(str_compactada)-1].split("|"))[1])
	char = (str_compactada[1:len(str_compactada)-1].split("|"))[2]

	if tamanho == 0:

		adicionaNaJanela(janela, char)

		arquivo_saida.write((char).encode("latin1"))

	else:

		str_descompactada = ""

		i = offset
		j = tamanho

		while j >= 1:

			str_descompactada += janela[i]

			i -= 1
			j -= 1

		str_descompactada += char

		adicionaNaJanela(janela, str_descompactada)

		arquivo_saida.write((str_descompactada).encode("latin1"))

#fecha o arquivo
arquivo_entrada.close()
arquivo_saida.close()