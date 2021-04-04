# encoding: utf-8

import sys

from collections import deque

#recebe uma lista de triplas e escolhe a melhor : sempre a que tiver o maior len
def escolheDadosParaCompactacao(lista_dados_a_compactar):

	lista_dados_a_compactar.sort(key = lambda x: x[2])

	return lista_dados_a_compactar[len(lista_dados_a_compactar) - 1]


def listaDeOffsets(janela, char):

	offsets = []

	i = -1

	for elemento in janela:

		i += 1

		if elemento == char:

			offsets.append(i)

	return offsets

def leCaractereDoArquivo():
	return (arquivo_entrada.read((1)).decode)("latin1")

#adiciona uma string no dicionario
def adicionaNaJanela(janela, string):

	if len(string) == 1:
		janela.appendleft(string)

	elif len(string) > 1:

		for char in string:

			janela.appendleft(char)


num_argv = 0

for elemento in sys.argv:
    num_argv += 1

if num_argv > 1:
    arquivo_entrada = open(sys.argv[1], "r")
    #arquivo_entrada = open("C:\Users\migue\Dropbox\UFABC\PDPD\Programas\Programas Pesquisa\LZ77\os_lusiadas.txt", "r")
    #arquivo_entrada = open("/home/joao/Área de Trabalho/os_lusiadas.txt", "r")
else:
   sys.exit("Programa executado sem arquivo a ser compactado")

#direciona cursos para o inicio do arquivo
arquivo_entrada.seek(0)

char = leCaractereDoArquivo()

EOF = 0

if len(char) == EOF:
    sys.exit("Arquivo Vazio!")

#Cria Arquivo novo no modo append
#arquivo_saida = open("C:\Users\migue\Dropbox\UFABC\PDPD\Programas\Programas Pesquisa\LZ77\os_lusiadas_compactado.txt", "a")
#arquivo_saida = open("/home/joao/Área de Trabalho/os_lusiadas_compactado.lz77", "a")
arquivo_saida = open(sys.argv[1][0 : len(sys.argv[1]) - 3] + "l77", "w")

janela = deque(maxlen = 128)

arquivo_entrada.seek(0)

while True:

	char = leCaractereDoArquivo()

	if len(char) == 0:

		print "Programa Finalizado"

		break

	#busca a(s) posição do char no dicionario: [] se nao esta la...
	lista_de_offsets = listaDeOffsets(janela, char)

	#print "lista_de_offsets", lista_de_offsets

	#se o char nao existe no dicionario
	if len(lista_de_offsets) == 0:

		#adiciona
		adicionaNaJanela(janela, char)

		str_compactada = "{0|0|" + char + "}"

	#se existe pelo menos uma correspondencia no dicionario
	else:

		#guarda a posicao do  proximo caractere depois do char para fazer o loop a partir dele em cada offset
		posicao_proximo_char = arquivo_entrada.tell()

		#print "n_r_p ", posicao_proximo_char

		lista_dados_a_compactar = []

		#print janela, char

		#descobrir qual offset usar
		for offset in lista_de_offsets:

			#print "offset em uso ", offset

			arquivo_entrada.seek(posicao_proximo_char - 1)

			char = leCaractereDoArquivo()

			#print "char depois de voltar ", char

			str_caracteres_repetidos = ""

			i = offset

			#esse loop serve p comparar os caracteres seguintes: no dicionario -> offset decresce de 1 | no look-ahead -> pega o proximo char
			while True:

				if i < 0 or janela[i] != char:
					"""
					if i < 0:

						char = leCaractereDoArquivo()
					"""
					break

				elif janela[i] == char:

					str_caracteres_repetidos += char

				char = leCaractereDoArquivo()

				i -= 1

			proximo_char = arquivo_entrada.tell()

			lista_dados_a_compactar.append([offset, str_caracteres_repetidos, len(str_caracteres_repetidos), char, proximo_char])


		dados_a_compactar = escolheDadosParaCompactacao(lista_dados_a_compactar)


		adicionaNaJanela(janela, dados_a_compactar[1] + dados_a_compactar[3])

		str_compactada = "{" + str(dados_a_compactar[0]) + "|" + str(dados_a_compactar[2]) + "|" + dados_a_compactar[3] + "}"

		arquivo_entrada.seek(dados_a_compactar[4])

	arquivo_saida.write((str_compactada).encode("latin1"))


arquivo_entrada.close()
arquivo_saida.close()