# encoding: utf-8

import sys

num_argv = 0

for elemento in sys.argv:
    num_argv += 1

if num_argv > 1:
    arquivo_entrada = open(sys.argv[1], "r")
    #arquivo_entrada = open("/home/joao/Área de Trabalho/os_lusiadas.txt", "r")
else:
    sys.exit("Programa executado sem arquivo a ser compactado")


#arquivo_entrada = open("/home/joao/Área de Trabalho/arquivo_novo.txt", "r")

#direciona cursos para o inicio do arquivo
arquivo_entrada.seek(0)

char = (arquivo_entrada.read(1)).decode("latin1")

#EOF no Python é uma string de len = 0
EOF = 0

if len(char) == EOF:
    arquivo_entrada.close()
    sys.exit("Arquivo Vazio!")

#Cria Arquivo novo no modo append
#arquivo_saida = open("C:\Users\migue\Dropbox\UFABC\PDPD\Programas\Programas Pesquisa\RLE\os_lusiadas_compactado.txt", "a")
#arquivo_saida = open("/home/joao/Área de Trabalho/os_lusiadas_compactado.rle", "a")
arquivo_saida = open(sys.argv[1][0 : len(sys.argv[1]) - 3] + "rle", "w")

arquivo_entrada.seek(0)

#proximo_char é sempre o char seguinte ao char corrente (char) pois o python a cada leitura do arquivo
#automaticamente adianta o cursor
proximo_char = (arquivo_entrada.read((1)).decode)("latin1")

#loop para fixar um char e verificar se os seguintes se repetem
while True:

    char = proximo_char

    #Fim do arquivo
    if len(char) == EOF:
        print "Fim do programa"

        break

    str_gravar = ""

    str_compactada = ""

    str_char = char

    num_repeticoes = 1

    #loop nos caracteres seguintes para verificar repetição de caracter
    while True:
        proximo_char = (arquivo_entrada.read(1)).decode("latin1")

        if char == proximo_char:
            num_repeticoes += 1

            str_char += proximo_char

        #quando a repetição acaba, a string compactada é criada sempre em pares de bytes
        else:
            while True:

                if num_repeticoes - 9 <= 0:

                    str_compactada += str(num_repeticoes) +  char

                    break

                else:

                    str_compactada += "9" +  char

                    num_repeticoes -= 9

            break


    str_gravar += str_compactada

    #gravo no arquivo
    arquivo_saida.write((str_gravar).encode("latin1"))

#fecha o arquivo
arquivo_entrada.close()
arquivo_saida.close()