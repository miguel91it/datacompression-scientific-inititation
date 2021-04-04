#include: utf-8

import sys

def leCaractereArquivo():
    return (arquivo_entrada.read((1))).decode("latin1")

num_argv = 0

for elemento in sys.argv:
    num_argv += 1


if num_argv > 1:
    arquivo_entrada = open(sys.argv[1], "r")
else:
   sys.exit("Programa executado sem arquivo a ser compactado")

char = leCaractereArquivo()

if len(char) == 0:
    sys.exit("Arquivo Vazio!")

arquivo_saida = open(sys.argv[1][0 : len(sys.argv[1]) - 3] + "uhuf", "w")

########################## Bloco para remontar a tabela de codificacao #####################################
#cria uma string temp contendo todos os dados de codificacao
tempDadosCodificacao = ""

while  char != '}':

    tempDadosCodificacao += char

    char = leCaractereArquivo()

#retira o ultimo "|"
tempDadosCodificacao = tempDadosCodificacao[:len(tempDadosCodificacao) - 1]

#splita a string em uma lista
tempDadosCodificacao = tempDadosCodificacao.split('|')

caracteresCodificados = []

for dado in tempDadosCodificacao:

    caracteresCodificados.append( (dado.split('_')[0], dado.split('_')[1]) )

########################## FIM - Bloco para remontar a tabela de codificacao #####################################


########################## Bloco para descompactar #####################################

char = leCaractereArquivo()

codigoMontado = char

i = 0

#para cada bit concatenado, varre a tabela de codificacao e busca a correspondencia por prefixo
#somente quando o tamanho listaCodigosEncontrados for igual a um, ai sim, encontrou o codigo correto a decodificar
while char:

    listaCodigosEncontrados = []

    codigoEncontrado = ""

    for codigo in caracteresCodificados:

        if codigoMontado == codigo[1][:len(codigoMontado)]:

            listaCodigosEncontrados.append(codigo)

    if len(listaCodigosEncontrados) == 1:

        codigoEncontrado = listaCodigosEncontrados[0][0]

        arquivo_saida.write(codigoEncontrado.encode('latin1'))

        codigoMontado = ""

    char = leCaractereArquivo()

    codigoMontado += char

    i+=1

########################## FIM - Bloco para descompactar #####################################

arquivo_entrada.close()
arquivo_saida.close()