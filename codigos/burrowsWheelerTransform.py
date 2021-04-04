#include: utf-8

import sys

num_argv = 0

for elemento in sys.argv:
    num_argv += 1

if num_argv > 1:
    arquivo_entrada = open(sys.argv[1], "r")
else:
   sys.exit("Programa executado sem arquivo a ser compactado")

char = arquivo_entrada.read(1).decode("latin1")

if len(char) == 0:
    sys.exit("Arquivo Vazio!")

arquivo_saida = open(sys.argv[1][:-3] + "bwt", "w")

arquivo_entrada.seek(0)

tamanhoString = 1024

stringS = ""

i = 1

stringS = arquivo_entrada.read(1).decode("latin1")

#entra ou continua no laco somente se stringS possui algum caractere nao nulo
while stringS:

    #quando a stringS possui o tamanho do vetor desejado
    if i == tamanhoString:

        matrizPermutacoes = []

        stringL = ""

        #gera a matriz de permutacoes
        for j in range(len(stringS)):

            permutaStringS = stringS[1:] + stringS[0]

            matrizPermutacoes.append(permutaStringS)

            stringS = permutaStringS

        #ordena lexicograficamente a matriz
        matrizPermutacoes.sort()

        indiceI = matrizPermutacoes.index(stringS)

        #obtem a ulima coluna da matriz
        for permutacao in matrizPermutacoes:

            stringL += permutacao[len(permutacao) - 1]

        arquivo_saida.write("{" + str(indiceI) + "}" + (stringL).encode('latin1'))

        stringS = ""

        i = 0

    stringS +=  arquivo_entrada.read(1).decode("latin1")

    i += 1


arquivo_entrada.close()
arquivo_saida.close()