# encoding: utf-8

import sys

def leCaractereDoArquivo():
	return (arquivo_entrada.read((1)).decode)("latin1")

#adiciona uma string no dicionario
def adicionaNoDicionario(dicionario, str):

	dicionario.append(str)

num_argv = 0

for elemento in sys.argv:
    num_argv += 1

if num_argv > 1:
    arquivo_entrada = open(sys.argv[1], "r")
    #arquivo_entrada = open("C:\Users\migue\Dropbox\UFABC\PDPD\Programas\Programas Pesquisa\LZ78\compactado.txt", "r")
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
#arquivo_saida = open("C:\Users\migue\Dropbox\UFABC\PDPD\Programas\Programas Pesquisa\LZ78\os_lusiadas_descompactado.txt", "a")
#arquivo_saida = open("/home/joao/Área de Trabalho/os_lusiadas_descompactado.lz78", "a")
arquivo_saida = open(sys.argv[1][0 : len(sys.argv[1]) - 3] + "u78", "w")

#cria objeto dicionario lz78
dicionario78 = [""]

arquivo_entrada.seek(0)

while True:

	str_compactada = ""

	char_lido = leCaractereDoArquivo()

	if len(char_lido) == EOF:
		break

	#descobre posicao e char da dupla [pos, char]
	while char_lido != "}":

		str_compactada += char_lido

		char_lido = leCaractereDoArquivo()

	else:
		str_compactada += char_lido


	posicao = str_compactada[1 : str_compactada.find("|") ]
	char = str_compactada[str_compactada.find("|") + 1 : len(str_compactada) - 1]

	if char == "/EOF/":
		print "Fim da descompressao LZ78"

		break

	#print posicao, str_compactada#, str_compactada[1], str_compactada[1: str_compactada.find("|")], char

	if posicao == 0:

		str_descompactada = char

		adicionaNoDicionario(dicionario78, str_descompactada)

		arquivo_saida.write((str_descompactada).encode("latin1"))

	else:

		str_descompactada = dicionario78[int(posicao)] + char

		adicionaNoDicionario(dicionario78, str_descompactada)

		arquivo_saida.write((str_descompactada).encode("latin1"))



	#print dicionario78

#fecha o arquivo
arquivo_entrada.close()
arquivo_saida.close()