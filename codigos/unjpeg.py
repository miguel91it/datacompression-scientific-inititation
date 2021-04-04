#include: utf-8

import sys
import numpy as np

############################################# Dados globais ####################################################
TABELA_COSSENOS = {}

MATRIZ_QUANTIZACAO_LUMINANCIA = [[16, 11, 10, 16,  24,  40,  51,  61],
						 		 [12, 12, 14, 19,  26,  58,  60,  55],
						 		 [14, 13, 16, 24,  40,  57,  69,  56],
								 [14, 17, 22, 29,  51,  87,  80,  62],
								 [18, 22, 37, 56,  68, 109, 103,  77],
								 [24, 35, 55, 64,  81, 104, 113,  92],
								 [49, 64, 78, 87, 103, 121, 120, 101],
								 [72, 92, 95, 98, 112, 100, 103,  99]]

MATRIZ_QUANTIZACAO_CROMINANCIA = [[17, 18, 24, 47, 99, 99, 99, 99],
						 		  [18, 21, 26, 66, 99, 99, 99, 99],
						 		  [24, 26, 56, 99, 99, 99, 99, 99],
								  [47, 66, 99, 99, 99, 99, 99, 99],
								  [99, 99, 99, 99, 99, 99, 99, 99],
								  [99, 99, 99, 99, 99, 99, 99, 99],
								  [99, 99, 99, 99, 99, 99, 99, 99],
								  [99, 99, 99, 99, 99, 99, 99, 99],
 								 ]

LISTA_ZIGZAG = [ (0,0), (0,1), (1,0), (2,0), (1,1), (0,2), (0,3), (1,2), (2,1), (3,0), (4,0), (3,1), (2,2), (1,3), (0,4), 
   (0,5), (1,4), (2,3), (3,2), (4,1), (5,0), (6,0), (5,1), (4,2), (3,3), (2,4), (1,5), (0,6), (0,7), (1,6), (2,5), (3,4), 
   (4,3), (5,2), (6,1), (7,0), (7,1), (6,2), (5,3), (4,4), (3,5), (2,6), (1,7), (2,7), (3,6), (4,5), (5,4), (6,3), (7,2), 
   (7,3), (6,4), (5,5), (4,6), (3,7), (4,7), (5,6), (6,5), (7,4), (7,5), (6,6), (5,7), (6,7), (7,6), (7,7) ]

TABELA_COEFICIENTES = [	['0', [0, 0], [0, 0]],
						['10', [-1, -1], [1, 1]],
						['110', [-3, -2], [2, 3]],
						['1110', [-7, -4], [4, 7]],
						['11110', [-15, -8], [8, 15]],
						['111110', [-31, -16], [16, 31]],
						['1111110', [-63, -32], [32, 63]],
						['11111110', [-127, -64], [64, 127]],
						['111111110', [-255, -128], [128, 255]],
						['1111111110', [-511, -256], [256, 511]],
						['11111111110', [-1023, -512], [512, 1023]],
						['111111111110', [-2047, -1024], [1024, 2047]],
						['1111111111110', [-4095, -2048], [2048, 4095]],
						['11111111111110', [-8191, -4096], [4096, 8191]],
						['111111111111110', [-16383, -8192], [8192, 16383]],
						['1111111111111110', [-32767, -16384], [16384, 32767]]  ]

#cada linha da tabela corresponde a  0 <= Z <= 15
#cada coluna de uma linha corresponde a 1 <= R <= 10
TABELA_COD_COEFICIENTES_AC_LUMINANCIA = [ 
 ['', '00','01','100','1011','11010','1111000','11111000','1111110110','1111111110000010','1111111110000011'],
 ['', '1100','11011','11110001','1111110110','11111110110','1111111110000100','1111111110000101','1111111110000110','1111111110000111','1111111110001000'],
 ['', '11100','11111001','1111110111','111111110100','111111110001001','111111110001010','111111110001011','111111110001100','111111110001101','111111110001110'],
 ['', '111010','111110111','111111110101','1111111110001111','1111111110010000','1111111110010001','1111111110010010','1111111110010011','1111111110010100','1111111110010101'],
 ['', '111011','1111111000','1111111110010110','1111111110010111','1111111110011000','1111111110011001','1111111110011010','1111111110011011','1111111110011100','1111111110011101'],
 ['', '1111010','11111110111','1111111110011110','1111111110011111','1111111110100000','1111111110100001','1111111110100010','1111111110100011','1111111110100100','1111111110100101'],
 ['', '1111011','111111110110','1111111110100110','1111111110100111','1111111110101000','1111111110101001','1111111110101010','1111111110101011','1111111110101100', '1111111110101101',],
 ['', '11111010','111111110111','1111111110101110','1111111110101111','1111111110110000','1111111110110001','1111111110110010','1111111110110011','1111111110110100','1111111110110101'],
 ['', '111111000','111111111000000','1111111110110110','1111111110110111','1111111110111000','1111111110111001','1111111110111010','1111111110111011','1111111110111100','1111111110111101'],
 ['', '111111001','1111111110111110','1111111110111111','1111111111000000','1111111111000001','1111111111000010','1111111111000011','1111111111000100','1111111111000101','1111111111000110'],
 ['', '111111010','1111111111000111','1111111111001000','1111111111001001','1111111111001010','1111111111001011','1111111111001100','1111111111001101','1111111111001110','1111111111001111'],
 ['', '1111111001','1111111111010000','1111111111010001','1111111111010010','1111111111010011','1111111111010100','1111111111010101','1111111111010110','1111111111010111','1111111111011000'],
 ['', '1111111010','1111111111011001','1111111111011010','1111111111011011','1111111111011100','1111111111011101','1111111111011110','1111111111011111','1111111111100000','1111111111100001'],
 ['', '11111111000','1111111111100010','1111111111100011','1111111111100100','1111111111100101','1111111111100110','1111111111100111','1111111111101000','1111111111101001','1111111111101010'],
 ['', '1111111111101011','1111111111101100','1111111111101101','1111111111101110','1111111111101111','1111111111110000','1111111111110001','1111111111110010','1111111111110011','1111111111110100'],
 ['', '11111111001','1111111111110101','1111111111110110','1111111111110111','1111111111111000','1111111111111001','1111111111111010','1111111111111011','1111111111111101','1111111111111110']]

TABELA_COD_COEFICIENTES_AC_CROMINANCIA = [ 
  ['','01','100','1010','11000','11001','111000','1111000','111110100','1111110110','111111110100'],
  ['','1011','111001','11110110','111110101','11111110110','111111110101','111111110001000','111111110001001','111111110001010','111111110001011'],
  ['','11010','11110111','1111110111','111111110110','111111111000010','1111111110001100','1111111110001101','1111111110001110','1111111110001111','1111111110010000'],
  ['','11011','11111000','1111111000','111111110111','1111111110010001','1111111110010010','1111111110010011','1111111110010100','1111111110010101','1111111110010110'],
  ['','111010','111110110','1111111110010111','1111111110011000','1111111110011001','1111111110011010','1111111110011011','1111111110011100','1111111110011101','1111111110011110'],
  ['','111011','1111111001','1111111110011111','1111111110100000','1111111110100001','1111111110100010','1111111110100011','1111111110100100','1111111110100101','1111111110100110'],
  ['','1111001','11111110111','1111111110100111','1111111110101000','1111111110101001','1111111110101010','1111111110101011','1111111110101100','1111111110101101','1111111110101110'],
  ['','1111010','11111111000','1111111110101111','1111111110110000','1111111110110001','1111111110110010','1111111110110011','1111111110110100','1111111110110101','1111111110110110'],
  ['','11111001','1111111110110111','1111111110111000','1111111110111001','1111111110111010','1111111110111011','1111111110111100','1111111110111101','1111111110111110','1111111110111111'],
  ['','111110111','1111111111000000','1111111111000001','1111111111000010','1111111111000011','1111111111000100','1111111111000101','1111111111000110','1111111111000111','1111111111001000'],
  ['','111111000','1111111111001001','1111111111001010','1111111111001011','1111111111001100','1111111111001101','1111111111001110','1111111111001111','1111111111010000','1111111111010001'],
  ['','111111001','1111111111010010','1111111111010011','1111111111010100','1111111111010101','1111111111010110','1111111111010111','1111111111011000','1111111111011001','1111111111011010'],
  ['','111111010','1111111111011011','1111111111011100','1111111111011101','1111111111011110','1111111111011111','1111111111100000','1111111111100001','1111111111100010','1111111111100011'],
  ['','11111111001','1111111111100100','1111111111100101','1111111111100110','1111111111100111','1111111111101000','1111111111101001','1111111111101010','1111111111101011','1111111111101100'],
  ['','11111111100000','1111111111101101','1111111111101110','1111111111101111','1111111111110000','1111111111110001','1111111111110010','1111111111110011','1111111111110100','1111111111110101'],
  ['','111111111000011','111111111010110','1111111111110111','1111111111111000','1111111111111001','1111111111111010','1111111111111011','1111111111111100','1111111111111101','1111111111111110'],]									  



############################################## Funcoes que searo usadas ###############################################


def leCharDoArquivo():
	return (imagem_compactada.read(1)).decode("latin1")

#le os dados binarios do arquivo e retorna uma lista de componentes binarias
#inicializa variavel tipo imagem. Se lista de componentes = 1 -> tem cinza, se nao, colorida
def leImagemCompactada():
	
	listaComponentesBinarias = []

	imagemBinaria = ""

	char = leCharDoArquivo()

	while char:

		imagemBinaria += char

		char = leCharDoArquivo()

	return imagemBinaria.split("M")
	#retorna lista de componentes binarias para o main, para nao perder a referencia

#dada uma linha e uma coluna busca na tabela de coeficientes AC DC o coeficiente
def buscaCoeficienteTabelaCoeficiente(linha, coluna):
		
	coeficiente = 0

	totalCoeficientesNaLinha = 2 ** linha

	#se o indice da coluna esta no intervalo negativo
	if coluna < totalCoeficientesNaLinha/2:

		coeficiente = -(totalCoeficientesNaLinha - 1 - coluna)

	elif coluna >= totalCoeficientesNaLinha/2:

		coeficiente = coluna

	return coeficiente

#recebe uma string sequenciaBinaria somente de ACs, os decodifica (zeros e nao zeros) e os adiciona lista de coeficientes
def decodificaCoeficientesAC(sequenciaBinaria, listaCoeficientesAC_DC,ehMatrizCromatica):

	#se eh matriz cromatica, usa a tabela de codigos AC cromaticos, caso contrario, usa tabela de codigos de luminancias
	TABELA_CODIGOS_AC = TABELA_COD_COEFICIENTES_AC_LUMINANCIA if ehMatrizCromatica == False else TABELA_COD_COEFICIENTES_AC_CROMINANCIA

	coeficienteACcodificado = ""

	posicao = 0

	while posicao <= len(sequenciaBinaria) -1:

		coeficienteACcodificado += sequenciaBinaria[posicao]

		#percorre todos os codigosAC da tabela de codigos AC - linhas de 0 a F (16) | colunas de 1 a 10 (10)
		for i in range(16):

			for j in range(1, 11):

				#quando encontrar o codigo acumulado AC, pois nao ha codigos de mesmo prefixo
				if coeficienteACcodificado == TABELA_CODIGOS_AC[i][j]:

					Z = i

					R = j

					codigoColunaC = sequenciaBinaria[posicao + 1 : posicao + 1 + R]

					C = binarioParaInteiro(codigoColunaC)

					coeficienteAC = buscaCoeficienteTabelaCoeficiente(R, C)

					#adiciona na lista os Z coeficientes 0 seguido de AC
					for coeficienteACzero in range(Z):
						
						listaCoeficientesAC_DC.append(0)

					listaCoeficientesAC_DC.append(coeficienteAC)

					posicao += R

					coeficienteACcodificado = ""

		posicao += 1

	for coeficienteACzero in range(64 -len(listaCoeficientesAC_DC)):
						
		listaCoeficientesAC_DC.append(0)

	#print len(listaCoeficientesAC_DC), listaCoeficientesAC_DC

def reconstroiMatrizQuantizada(listaCoeficientesAC_DC):

	matrizQuantizadaReconstruida = np.zeros((8,8), dtype = np.int8)

	for i in range(len(LISTA_ZIGZAG)):

		linha = LISTA_ZIGZAG[i][0]

		coluna = LISTA_ZIGZAG[i][1]

		matrizQuantizadaReconstruida[linha][coluna] = listaCoeficientesAC_DC[i]

	return matrizQuantizadaReconstruida

#recebe uma componente binaria do main, decodifica DC nela mesma, chama decodificaAC e reconstroi a matriz quantizada Qlinha
def decodificaComponente(componenteBinaria, ehMatrizCromatica):
	
	listaCoeficientesAC_DC = []

	sequenciaBinaria = componenteBinaria

	#recupera o codigo binario da linha do coeficiente DC: uns e zero
	codigoLinhaDC = componenteBinaria[ : componenteBinaria.index("0") + 1]

	#recupera o indice da linha usando a contagem de uns, apenas, do codigo binario...-1 para excluir o zero
	#como explicado na secao teorica da linha DC
	linhaDC = len(codigoLinhaDC) - 1

	#retira os bits ja lidos da sequencia binaria, sobrando os bits da coluna e os bits dos coeficientes AC
	sequenciaBinaria = sequenciaBinaria[sequenciaBinaria.index("0") + 1 : ]

	#a coluna eh obtida lendo os os proximos R-bits,onde R = linhaDC, portanto, linhaDC - bits
	codigoColunaDC = sequenciaBinaria[ : linhaDC]

	#retira os linhaDC-bits lidos para identificar a coluna
	sequenciaBinaria = sequenciaBinaria[linhaDC : ]

	#a colunaDC e a conversao de binario para decimal do codigo da coluna
	colunaDC = binarioParaInteiro(codigoColunaDC)

	#com linha e coluna DC, basta recuperar o coefciente DC
	coeficienteDC = buscaCoeficienteTabelaCoeficiente(linhaDC, colunaDC)

	#adiciona DC na lista zigzag de coeficientes
	listaCoeficientesAC_DC.append(coeficienteDC)

	#decodifica a sequencia binaria restante, de ACs, e ja adiciona na lista de coeficientesAC_DC
	decodificaCoeficientesAC(sequenciaBinaria, listaCoeficientesAC_DC, ehMatrizCromatica)

	matrizQuantizadaReconstruida = reconstroiMatrizQuantizada(listaCoeficientesAC_DC)

	return matrizQuantizadaReconstruida

#recebe uma matriz quantizada e dequantiza
def dequantiza(matrizQuantizada, ehMatrizCromatica):
	
	matrizDequantizada = np.zeros((8,8))

	MATRIZ_DEQUANTIZACAO = MATRIZ_QUANTIZACAO_CROMINANCIA if ehMatrizCromatica == True else MATRIZ_QUANTIZACAO_LUMINANCIA

	for i in range(8):

		for j in range(8):

			matrizDequantizada[i][j] = MATRIZ_DEQUANTIZACAO[i][j] * matrizQuantizada[i][j]

	return matrizDequantizada

def preCalculaCossenos():
	
	posicoes = []

	#aqui, o que e feito para i e x e valido e igual para j e y
	for i in range(8):
		for x in range(8):
			posicoes.append( (2*x+1)*i )

	for posicao in posicoes:
		TABELA_COSSENOS[posicao] = np.cos(posicao * np.pi / 16)


#recebe uma matriz transformada pela TDC e desfaz a TDC
def invertetransformacaoDiscretaCossenos(matrizDequantizada):
	
	matrizITDC = np.zeros((8,8))#,  dtype = np.int8)

	#para cada posicao i,j da matriz convvertida em cossenos, com 0 <= i,j <= 7, percorreremos x e y de 0 a 7
	#i, j aqui referem-se a  posicao do pixel na matriz TDC (transformada)
	for x in range(8):
		for y in range(8):

			somacossenos = 0

			#x, y aqui refere-se a posicao do pixel na matriz tomdecinza ou Y ou Cb ou Cr
			for i in range(8):
				for j in range(8):

			
					Ci = 1 if i > 0 else 1/np.sqrt(2)

					Cj = 1 if j > 0 else 1/np.sqrt(2)

					somacossenos += Ci * Cj * matrizDequantizada[i][j] * TABELA_COSSENOS[(2*x+1)*i] * TABELA_COSSENOS[(2*y+1)*j]

			matrizITDC[x][y] = int(round(0.25 * somacossenos))

	return matrizITDC

#recebe uma lista de componentes e as une em uma matriz
def uneComponentes(listaComponentes):
	
	matrizYCbCr = []

	for i in range(8):
		
		matrizYCbCr.insert(i, [])

		for j in range(8):

			Y =  listaComponentes[0][i][j]
			Cb = listaComponentes[1][i][j]
			Cr = listaComponentes[2][i][j]

			matrizYCbCr[i].append([Y, Cb, Cr])

	return matrizYCbCr

#recebe a matriz de pixels YCbCr e converte para pixels RGB na mesma matriz
def ConverteCores(matrizImagem):

	for i in range(8):

		for j in range(8):

			Y  = matrizImagem[i][j][0]
			Cb = matrizImagem[i][j][1]
			Cr = matrizImagem[i][j][2]

			R = Y + 1.371 * (Cr - 128)
			G = Y - 0.698 * (Cr - 128) - 0.336  * (Cb - 128)
			B = Y + 1.732 * (Cr - 128)

			matrizImagem[i][j][0]  = R
			matrizImagem[i][j][1]  = G
			matrizImagem[i][j][2]  = B

def binarioParaInteiro(binario):

    decimal = 0

    binario = binario[::-1]

    tam = len(binario)

    for i in range(tam):
        
        if binario[i] == "1":
        
            decimal = decimal + 2**i
    
    return decimal


############################################## Funcoes que searo usadas ###############################################



################################################## Inicio do Programa ####################################################

num_argv = 0

for elemento in sys.argv:
	num_argv += 1

if num_argv > 1:
	imagem_compactada = open(sys.argv[1], "r")
else:
	sys.exit("Programa executado sem arquivo a ser executado")

char = leCharDoArquivo()

if len(char) == 0:
	sys.exit("Arquivo Vazio!")

imagem_descompactada = open(sys.argv[1][:-3] + "ujpeg", "w")

#se imagem tom de cinza - 1 componente | se imagem colorida - 3 componentes
listaComponentesBinarias = leImagemCompactada()

#pre calcula os cossenos e ja armazena na tabela de cossenos
preCalculaCossenos()

ordemProcessamento = 0

listaComponentesDecodificadas = []

#para cada componente binaria da lista de componentes binarias
for componenteBinaria in listaComponentesBinarias:

	ehMatrizCromatica = True if ordemProcessamento > 0 else False

	#decodifica a componente em uma matriz quantizada
	matrizQuantizadaReconstruida = decodificaComponente(componenteBinaria, ehMatrizCromatica)

	matrizDequantizada = dequantiza(matrizQuantizadaReconstruida, ehMatrizCromatica)
	#print matrizDequantizada
	matrizITDC = invertetransformacaoDiscretaCossenos(matrizDequantizada)

	#armazena essas componentes reconstruidas em uma lista de componentes reconstruidas
	listaComponentesDecodificadas.append(matrizITDC)

	ordemProcessamento += 1

#se a lista de componentes possui mais de uma matriz, entao eh imagem colorida
#executa a uniao e a conversao das cores
if len(listaComponentesDecodificadas) > 1:

	matrizColorida = uneComponentes(listaComponentesDecodificadas)

	ConverteCores(matrizColorida)

	imagem_descompactada.write(matrizColorida)

elif:

	imagem_descompactada.write(listaComponentesDecodificadas[0])

imagem_compactada.close()
imagem_descompactada.close()