# encoding: utf-8

import sys

num_argv = 0

for elemento in sys.argv:
    num_argv += 1

if num_argv > 1:
    arquivo_entrada = open(sys.argv[1], "r")
else:
    sys.exit("Programa executado sem arquivo a ser descompactado")

#aponta para o inicio do arquivo
arquivo_entrada.seek(0)

#pega primeiro caractere do arquivo
char = (arquivo_entrada.read(1)).decode("latin1")

EOF = 0

#verifica se arquivo esta vazio
if len(char) == EOF:
    arquivo_entrada.close()
    sys.exit("Arquivo Vazio!")

#Cria Arquivo novo no modo append
#arquivo_saida = open("C:\Users\migue\Dropbox\UFABC\PDPD\Programas\Programas Pesquisa\RLE\os_lusiadas_descompactado.txt", "a")
#arquivo_saida = open("/home/joao/Área de Trabalho/os_lusiadas_descompactado.txt", "a")
arquivo_saida = open(sys.argv[1][0 : len(sys.argv[1]) - 3] + "unrle", "w")

#aponta novamente para o inicio do arquivo
arquivo_entrada.seek(0)

while True:

    #obtem primeiro a repeticao
    char = (arquivo_entrada.read(1)).decode("latin1")

    #obtem o proximo caractere
    proximo_char = (arquivo_entrada.read(1)).decode("latin1")

    if len(char) == EOF or len(proximo_char) == EOF:
        arquivo_entrada.close()
        arquivo_saida.close()
        sys.exit("Programa finalizado!")

    num_repeticoes = char
    char_repetido = proximo_char

    i = 0

    str_descompactada = ""

    while i < int(num_repeticoes):

        str_descompactada += char_repetido

        i += 1

    #gravo no arquivo
    arquivo_saida.write((str_descompactada).encode("latin1"))

#fecha arquivos abertos
arquivo_entrada.close()
arquivo_saida.close()