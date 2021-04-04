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
								  [99, 99, 99, 99, 99, 99, 99, 99]]

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
 ['', '1111011','111111110110','1111111110100110','1111111110100111','1111111110101000','1111111110101001','1111111110101010','1111111110101011','11111111101011001111111110101101',],
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
  ['','111111111000011','111111111010110','1111111111110111','1111111111111000','1111111111111001','1111111111111010','1111111111111011','1111111111111100','1111111111111101','1111111111111110']]									  


############################################## Funcoes que searo usadas ###############################################

def leLinhaDoArquivo():
	return (imagem_original.readline()).decode("latin1")

#le a matriz de pixels do arquivo texto
def leImagemDoArquivo():
	
	matrizImagemOriginal = []

	#le a primeira linha de pixels do arquivo original
	linhaArquivo = leLinhaDoArquivo()

	i = 0

	while linhaArquivo:

		#linhas inteiras serao lidas do arquivo, subdivididas em pixels e convertidos, os valores, em inteiros
		if tipoImagem == "TOMCINZA": 
			
			matrizImagemOriginal.append(map(int,linhaArquivo.split(";")))
		
		#se a imagem do arquivo for colorida entao sao necessarios dois splits, um para o pixel (";") e outros para as cores (",")
		elif tipoImagem == "COLORIDA":			
			
			matrizImagemOriginal.insert(i, [])

			for pixel in linhaArquivo.split(";"):
				matrizImagemOriginal[i].append(map(int,pixel.split(",")),)

		i += 1

		linhaArquivo = leLinhaDoArquivo()

	return matrizImagemOriginal

#recebe a matriz de pixels RGB e converte para pixels Y Cb Cr na mesma matriz
def ConverteCores(matrizImagem):

	for i in range(8):

		for j in range(8):

			R = matrizImagem[i][j][0]
			G = matrizImagem[i][j][1]
			B = matrizImagem[i][j][2]

			Y  = 77./256*R + 150./256*G + 29./256*B
			Cb = -(44./256*R) - (87./256*G) + 131./256*B + 128
			Cr = 131./256*R - (110./256*G) - (21./256*B) + 128

			matrizImagem[i][j][0]  = Y
			matrizImagem[i][j][1] = Cb
			matrizImagem[i][j][2] = Cr

#recebe uma matriz de pixels coloridos Y Cb Cr
def SeparaCores(matrizImagemYCbCr):
	
	matrizY = np.zeros((8,8))
	matrizCb = np.zeros((8,8))
	matrizCr = np.zeros((8,8))

	listaMatrizesComponentes = []

	for i in range(8):

		for j in range(8):

			matrizY[i][j]  = matrizImagemYCbCr[i][j][0]
			matrizCb[i][j] = matrizImagemYCbCr[i][j][1]
			matrizCr[i][j] = matrizImagemYCbCr[i][j][2]

	listaMatrizesComponentes.append(matrizY)
	listaMatrizesComponentes.append(matrizCb)
	listaMatrizesComponentes.append(matrizCr)

	return listaMatrizesComponentes
	#retorna uma lista de matrizes componentes Y Cb e Cr	

def preCalculaCossenos():
	
	posicoes = []

	#aqui, o que e feito para i e x e valido e igual para j e y
	for i in range(8):
		for x in range(8):
			posicoes.append( (2*x+1)*i )

	for posicao in posicoes:
		TABELA_COSSENOS[posicao] = np.cos(posicao * np.pi / 16)


#recebe uma matriz componente e aplica a transformacao discreta dos cossenos
def transformacaoDiscretaCossenos(matrizComponente):
	
	#cria uma matriz de mesma ordem da matrizComponente, inicialmente zerada, para receber os valores transformados em cossenos
	matrizTDC = np.zeros((8,8))

	#para cada posicao i,j da matriz convertida em cossenos, com 0 <= i,j <= 7, percorreremos x e y de 0 a 7
	#i, j aqui referem-se a  posicao do pixel na matriz TDC (transformada)
	for i in range(8):
		for j in range(8):

			somacossenos = 0

			#x, y aqui refere-se a posicao do pixel na matriz tomdecinza ou Y ou Cb ou Cr
			for x in range(8):
				for y in range(8):

					somacossenos += matrizComponente[x][y] * TABELA_COSSENOS[(2*x+1)*i] * TABELA_COSSENOS[(2*y+1)*j]

			Ci = 1 if i > 0 else 1/np.sqrt(2)

			Cj = 1 if j > 0 else 1/np.sqrt(2)

			matrizTDC[i][j] = 0.25 * Ci * Cj * somacossenos

	return matrizTDC

#recebe uma matriz componente transformada em cossenos e aplica a quantizacao 
def quantizacaoMatriz(matrizTDC):

	matrizQuantizada = np.zeros((8,8), dtype = np.int8)

	matrizQuantizacao = []

	if tipoImagem == "TOMCINZA":

		matrizQuantizacao = MATRIZ_QUANTIZACAO_LUMINANCIA

	elif tipoImagem == "COLORIDA":

		matrizQuantizacao = MATRIZ_QUANTIZACAO_CROMINANCIA

	for i in range(8):

		for j in range(8):

			valorQuantizado = round(matrizTDC[i][j] / matrizQuantizacao[i][j])

			matrizQuantizada[i][j] = valorQuantizado

	return matrizQuantizada

#recebe uma matriz componente quantizada e aplica a compressao e "grava no arquivo??"
def compressaoMatriz(matrizQuantizada, ehMatrizCromatica):

	str_matrizCompactada = ""

	listaCoeficientesAC_DC = zigzag(matrizQuantizada)

	#remove o DC, sobra apenas AC na lista
	coeficienteDC = listaCoeficientesAC_DC.pop(0) 

	parLinhaColunaDC = buscaLinhaColunaCoeficiente(coeficienteDC)

	str_DC_compactado = codificaCoeficienteDC(parLinhaColunaDC)

	str_AC_compactados = codificaCoeficientesAC(listaCoeficientesAC_DC, ehMatrizCromatica)

	str_matrizCompactada = str_DC_compactado + str_AC_compactados

	return str_matrizCompactada

def zigzag(matrizComprimir):
	listaCoeficientesAC_DC = []

	for posicao in LISTA_ZIGZAG:

		linha = posicao[0]

		coluna = posicao[1]

		listaCoeficientesAC_DC.append(matrizComprimir[linha][coluna])

	return listaCoeficientesAC_DC

#recebe um inteiro em decimal e converte para binario e completa de zeros a esquerda ate tamanho desejado
def inteiroParaBinario(inteiro, tamanho):

	binario = bin(inteiro)[2:]

	zeros = ""

	if len(binario) < tamanho:

		for i in range(tamanho - len(binario)):

			zeros += "0"

		return zeros + binario

	return binario

#recebe um coeficienteDC por meio do parLinhaColuna e o codifica por Huffman
def codificaCoeficienteDC(parLinhaColuna):

	linhaEncontrada = parLinhaColuna[0]

	colunaEncontrada = parLinhaColuna[1]

	codigoBinarioLinha = TABELA_COEFICIENTES[linhaEncontrada][0]

	codigoBinarioColuna = inteiroParaBinario(colunaEncontrada, linhaEncontrada)

	return codigoBinarioLinha + codigoBinarioColuna

def buscaLinhaColunaCoeficiente(coeficienteAC_DC):

	linhaEncontrada = -1

	colunaEncontrada = 0

	linha = 0

	#percorre a tabela de coeficientes e encontra a primeira linha a que o DC pertence
	while linhaEncontrada == -1:

		inicioIntervaloPositivo = TABELA_COEFICIENTES[linha][2][0]
		
		fimIntervaloPositivo    = TABELA_COEFICIENTES[linha][2][1]

		#quando o coeficiente for encontrado no primeiro intervalo, grava o codigo da linha
		if (abs(coeficienteAC_DC) >= inicioIntervaloPositivo and abs(coeficienteAC_DC) <= fimIntervaloPositivo):

			linhaEncontrada = linha

			#para coeficiente negativo, transformo a coluna encontrada do intervalo positivo em coluna do intervalo negativo
			if coeficienteAC_DC < 0:

				colunaEncontrada = fimIntervaloPositivo - abs(coeficienteAC_DC)

			#para coeficiente positivo, a coluna possui o mesmo valor do coeficiente
			if coeficienteAC_DC > 0:

				colunaEncontrada = coeficienteAC_DC

		linha += 1

	parLinhaColuna = (linhaEncontrada, colunaEncontrada)

	return parLinhaColuna

#recebe uma lista de 63 coeficientes AC, zeros e nao zeros e codifica - Ha duas tabelas de cod AC : para luminancia e para crominancia
def codificaCoeficientesAC(listaCoeficientesAC, ehMatrizCromatica):

	str_AC_compactados = ""

	EOB = "00" if ehMatrizCromatica == True else "1010" 

	zerosPrecedentes = 0

	#para cada AC nao zero, conta Z zeros antes dele
	for coeficienteAC in listaCoeficientesAC:

		if coeficienteAC == 0:
			zerosPrecedentes += 1 

		else:
			
			Z = zerosPrecedentes

			parLinhaColunaAC = buscaLinhaColunaCoeficiente(coeficienteAC)

			R = parLinhaColunaAC[0]

			C = parLinhaColunaAC[1]

			#se eh uma matriz componente tomcinza ou Y, entao a tabela de codigos AC eh a de Luminancia
			if ehMatrizCromatica == False:

				codigoBinarioAC = TABELA_COD_COEFICIENTES_AC_LUMINANCIA[Z][R]

			#se eh uma matriz componente cromatica Cb ou Cr, entao a tabela de codigo AC eh a crominancia
			elif ehMatrizCromatica == True:

				codigoBinarioAC = TABELA_COD_COEFICIENTES_AC_CROMINANCIA[Z][R]

			codigoBinarioColuna = inteiroParaBinario(C, R)

			str_AC_compactados += codigoBinarioAC + codigoBinarioColuna

			#zera a contadora de zeros precendentes para o proximo coeficiente AC nao zero
			zerosPrecedentes = 0

	zerosFinais =  zerosPrecedentes

	return str_AC_compactados + EOB

################################################## Inicio do Programa ####################################################

num_argv = 0

for elemento in sys.argv:
	num_argv += 1

if num_argv > 1:
	imagem_original = open(sys.argv[1], "r")
else:
	sys.exit("Programa executado sem arquivo a ser executado")

linhaArquivo = leLinhaDoArquivo()

if len(linhaArquivo) == 0:
	sys.exit("Arquivo Vazio!")

imagem_compactada = open(sys.argv[1][:-3] + "j_peg", "w")

#descobre que tipo de iamgem sera compactada
tipoImagem = "COLORIDA" if int(linhaArquivo[0]) == 1 else "TOMCINZA" 

#le imagem do arquivo e retorna a matrizImagem a imagem lida
matrizImagem = leImagemDoArquivo()

listaMatrizesComponentes = []

if tipoImagem == "COLORIDA":

	ConverteCores(matrizImagem)

	listaMatrizesComponentes = SeparaCores(matrizImagem)

elif tipoImagem == "TOMCINZA":

	#se for imagem tom de cinza, a propria matrizImagem sera considera como uma componente, a unica componente
	listaMatrizesComponentes.append(matrizImagem)

#pre calcula os cossenos e ja armazena na tabela de cossenos
preCalculaCossenos()

#para saber qual componente esta sendo compactada: 1-tom de cinza/Y / 2-Cb / 3-Cr
ordemProcessamento = 0

#para cada componente: TDC, Quantizacao e Compressao
for matrizComponente in listaMatrizesComponentes:

	ehMatrizCromatica = True if ordemProcessamento > 0 else False

	matrizTDC = transformacaoDiscretaCossenos(matrizComponente)

	matrizQuantizada = quantizacaoMatriz(matrizTDC)

	str_matrizCompactada = compressaoMatriz(matrizQuantizada, ehMatrizCromatica)

	imagem_compactada.write("M" + str_matrizCompactada)

	ordemProcessamento += 1


imagem_original.close()
imagem_compactada.close()