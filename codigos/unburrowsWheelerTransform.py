#include: utf-8

import sys

def ordemAparicaoStringF (stringF, posicao):

    ordemAparicao = 0

    i = 0

    char = stringF[posicao]

    for elemento in stringF:

        if elemento == char:

            ordemAparicao += 1

            if i == posicao:

                break

        i += 1

    return ordemAparicao


def posicaoNaStringL (stringL, charStringF, ordemAparicaoStringF):

    i = 0

    ordemAparicao = 0

    for elemento in stringL:

        if elemento == charStringF:

            ordemAparicao += 1

            if ordemAparicao == ordemAparicaoStringF:

                return i

        i += 1


num_argv = 0

for elemento in sys.argv:
    num_argv += 1

if num_argv > 1:
    arquivo_entrada = open(sys.argv[1], "r")
else:
   sys.exit("Programa executado sem arquivo a ser compactado")

char = arquivo_entrada.read(1).decode('latin1')

if len(char) == 0:
    sys.exit("Arquivo Vazio!")

arquivo_entrada.seek(0)

arquivo_saida = open(sys.argv[1][:-3] + "unbwt", "w")

tamanhoString = 1024

stringL = ""

i = 1

stringL = arquivo_entrada.read(1).decode('latin1')

while stringL:

    if '{' in stringL and '}' in stringL:

        if i - len( stringL[ : stringL.index('}') + 1] ) == tamanhoString:

            indiceI = int(stringL[1 : stringL.index('}')])

            stringL = stringL[stringL.index('}') + 1 : ]

            stringF = "".join(sorted(stringL))

            stringS = stringF[indiceI]

            posicaoEmF = indiceI

            for j in range(1, len(stringL)):

                posicaoProxChar = posicaoNaStringL (stringL, stringF[posicaoEmF], ordemAparicaoStringF (stringF, posicaoEmF))

                stringS += stringF[posicaoProxChar]

                posicaoEmF = posicaoProxChar

            arquivo_saida.write((stringS).encode('latin1'))

            stringL = ""

            i = 0

    stringL += arquivo_entrada.read(1).decode('latin1')

    i += 1

arquivo_entrada.close()
arquivo_saida.close()