#include: utf-16

'''para trabalharmos bem, o arquivo precisa ser salvo com codificacao ANSI(ascii + 128 seguintes), pois inclui as acentuacoes nas letras usando APENAS UM BYTE para cada leCaractereArquivo
alem disso, o endline deve ser do UNIX/LINUX, que utiliza apenas um byte de dado tb...que eh o caractere 10 em decimal
'''

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

arquivo_saida = open(sys.argv[1][0 : len(sys.argv[1]) - 3] + "huf", "w")

################## Bloco para sumarizar as ocorrencias ##################
arquivo_entrada.seek(0)

caracteresOcorrencias = {}

char= leCaractereArquivo()

while char:

    if  char in caracteresOcorrencias:

        caracteresOcorrencias[char] += 1

    else:

        caracteresOcorrencias[char] = 1

    char = leCaractereArquivo()

ocorrenciasOrdenadas =  sorted(caracteresOcorrencias.iteritems(), key=lambda (chave,valor): (valor,chave))

################## FIM - Bloco para sumarizar as ocorrencias ##################


################## Bloco para codificar os caracteres ##################

#cria a estrutura para armazenar cada caractere e sua codificacao
#ocorrenciasOrdenadas = []
#ocorrenciasOrdenadas =[(u'e',30), (u'f',70), (u'd',170), (u'b',200), (u'c',230), (u'a',300) ]

caracteresCodificados = {}

#insere todos os caracteres
for ocorrencia in ocorrenciasOrdenadas:
    caracteresCodificados[ocorrencia[0]] = ""

#laco para montar a codificacao de cada caractere, dois a dois, comecando dos menos recorrentes
while len(ocorrenciasOrdenadas) > 1:

    #recupera caractere menos recorrente; remove da lista --- parOrdenado0 =([caractere], ocorrencia)
    parOrdenado0 = ocorrenciasOrdenadas.pop(0)

    #recupera segundo caractere menos recorrente; remove da lista --- parOrdenado1 =([caractere], ocorrencia)
    parOrdenado1 = ocorrenciasOrdenadas.pop(0)

    #print caracteresCodificados['f']

    #agrupa os itens menos recorrentes e soma suas ocorrencias
    #itemAgrupado = [todos caracteres dos dois primeiros itens de cada iteracao ]
    itemAgrupado = []

    for caractere in parOrdenado0[0]:
        itemAgrupado.append(caractere)

    for caractere in parOrdenado1[0]:
        itemAgrupado.append(caractere)

    #insere os itens agrupados formando um novo item unico
    ocorrenciasOrdenadas.insert(0,  (itemAgrupado, parOrdenado0[1]+parOrdenado1[1]))

    ocorrenciasOrdenadas.sort(key=lambda x: x[1])

    #como parOrdenado0 e o menos recorrente, receeb bit 1
    for caractere in parOrdenado0[0]:
        caracteresCodificados[caractere] = '0' + caracteresCodificados[caractere]

    #como parOrdenado1 e o mais recorrente, receeb bit 0
    for caractere in parOrdenado1[0]:
        caracteresCodificados[caractere] = '1' + caracteresCodificados[caractere]

################## FIM - Bloco para codificar os caracteres ##################

##################          Bloco para compactar o arquivo ##################

#grava a tabela de codificacao no arquivo compactado
for (caractere, codigo) in sorted(caracteresCodificados.iteritems(), key=lambda (caractere, codigo): (len(codigo))):
    arquivo_saida.write((caractere).encode('latin1') + '_' + codigo + '|')

arquivo_saida.write("}")

arquivo_entrada.seek(0)

char = ""

char = leCaractereArquivo()

while char :

    charCodificado = caracteresCodificados[char]

    arquivo_saida.write((charCodificado).encode('latin1') )

    char = leCaractereArquivo()

################## FIM - Bloco para compactar o arquivo ##################

arquivo_entrada.close()
arquivo_saida.close()