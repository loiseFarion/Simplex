#Helena e Loise
#TDE Otimização de sistemas lineares

import math
import numpy as np
import sys

# Função para imprimir a tabela do simplex a cada iteração
def printSimplexTable(matriz, variaveis_base, variaveis_nao_base):
    variaveis = len(variaveis_base) + len(variaveis_nao_base)
    matriz_formatada = [] # Cria uma matriz para armazenar os dados formatados
    cabecalho = [f'x{i+1}' for i in range(variaveis)] + ['b'] # Cabeçalho das variáveis
    print("  |", " ".join(cabecalho))
    # Loop para cada linha da matriz
    for i in range(len(variaveis_base)):
        linha_formatada = []
        print(f'x{variaveis_base[i]+1} ', end=' ') 
        linha_formatada.append(f'x{variaveis_base[i]+1}') # Adiciona a variável de base à linha formatada

        # Adiciona os valores da matriz à linha formatada
        for valor in matriz[i+1]:
            valor_formatado = int(valor) if valor.is_integer() else f'{valor:.2f}' # Atribui o valor inteiro, caso contrário coloca duas casas decimais
            print(valor_formatado, end='  ')
            linha_formatada.append(valor_formatado) 
        
        # Adiciona a linha formatada à matriz
        matriz_formatada.append(linha_formatada)
        print()  # Quebra de linha para o próximo print
    return matriz_formatada # Retorna a matriz formatada

# Função para definir o coeficiente das variaveis base 
def coeficienteVariaveisBase(matriz_com_folga,variaveis_base):
  coeficientes = []
  for i in range(len(variaveis_base)):
    coeficientes.append(matriz_com_folga[0][variaveis_base[i]]) # Identifica o coeficiente de cada variavel base
  return coeficientes # Retorna os coeficientes

# Função para cálculo do Zj
def calculoZj(matriz_com_folga,variaveis_base, coef_variaveis_base):
  resultados = np.zeros(matriz_com_folga.shape[1]) # Vetor inicializado para armazenar os resultados
  matriz_sem_primeira_linha = np.delete(matriz_com_folga, 0, axis=0) # Removendo a primeira linha referente ao Z ou C
  for i in range(matriz_sem_primeira_linha.shape[0]):
      resultados += matriz_sem_primeira_linha[i] * coef_variaveis_base[i] # Multiplica cada coluna da linha com o coeficiente da base e realiza a soma
  return resultados # Retorna os resultados de Zj

# Função para cálculo da diferença entre Cj e Zj
def calculoDifCjZj(matriz_com_folga,Zj):
  linha = matriz_com_folga[0] # Vetor contendo os valores de Cj
  resultadoDif = linha - Zj # Vetor com o calculo Cj - Zj
  resultadoDif = resultadoDif[:-1] # Remove o último elemento pois não deve ser calculado a diferença para o b
  return resultadoDif # Retorna o resultado de  Cj - Zj

# Função para cálculo do teta
def calculaTeta(matriz_com_folga,indice_maior_valor):
  teta = []
  matriz_sem_primeira_linha = np.delete(matriz_com_folga, 0, axis=0) # Removendo a primeira linha referente ao Z ou C
  linhas, colunas = matriz_sem_primeira_linha.shape
  for i in range(len(matriz_sem_primeira_linha)): # Percorre as demais linhas
    if matriz_sem_primeira_linha[i][indice_maior_valor] == 0: # Verifica se o elemento da coluna de maior indice é o
      valor = float('inf') # Atribui o inf, pois não é permitido divisão por 0
    else:
      valor = matriz_sem_primeira_linha[i][colunas-1]/matriz_sem_primeira_linha[i][indice_maior_valor] # Calculo do teta divide o b pela coluna de maior índice do Cj-Zj
    semFronteira = verificaSemFronteira(valor) # Verificação de problema sem fronteira
    teta.append(valor)
  return teta,semFronteira # Retorna os teta calculo e se o problema é sem fronteira

# Função de cálculo do simplex
def manipulacaoSimplex(matriz, indexLinhaPivo, indexColunaPivo):
    primeira_linha = matriz[0, :]
    matriz = np.delete(matriz, 0, axis=0) # Removendo a primeira linha referente ao Z ou C
    linhaPivot = matriz[indexLinhaPivo] # Identificando a linha pivo
    pivo = matriz[indexLinhaPivo, indexColunaPivo] # Identifica o pivo
    matriz[indexLinhaPivo] = linhaPivot / pivo # Linha pivo dividida pelo valor do pivo
    numLinhas, numColunas = matriz.shape 
    for i in range(numLinhas): # Atualizando as outras linhas para zerar a coluna pivo
        if i != indexLinhaPivo:  # Não mexer na linha pivo
            linha = matriz[i] # Identifica a linha que será atualizada
            fator = linha[indexColunaPivo] # Identifica o fator de multiplicação
            matriz[i] = linha - fator * matriz[indexLinhaPivo] # Atualiza a linha

    matriz = np.vstack([primeira_linha, matriz])# Adicionando a primeira linha da função objetivo a matriz
    return matriz # Retorna a matriz

# Função de verificação de problema sem fronteira
def verificaSemFronteira(teta):
  if teta <= 0 or math.isinf(teta):
    return True  # Retorna True se encontrar teta igual a 0, negativo ou infinito
  return False  # Retorna False se não encontrar teta com valores indesejados

# Função de verificação de sistema degenerado
def verificaSistemaDegenerado(teta,variaveis_base,matriz_com_folga):
  if len(set(teta)) == 1: # Verifica se apresenta valores de teta iguais
    print("Sistema degenerado!")
    primeiraLinha = matriz_com_folga[0] # Identifica os coeficientes da função objetivo
    listaTeta = []
    for x in variaveis_base:
      listaTeta.append(primeiraLinha[x]) # Cria uma lista com os coeficientes da função objetivo das variáveis básicas
    maiorItem = max(listaTeta) # Identifica o maior coeficiente
    indicemaiorItem = listaTeta.index(maiorItem) # Obtém o índice do maior coeficiente
    teta[indicemaiorItem] = maiorItem+1 # Incrementa o valor de teta correspondente ao maior coeficiente para realizar o critério de menor subscrito
    return True,teta # Retorna que o problema é degenerado e o teta com o critério de menor subscrito
  else:
    return False,teta # Retorna que o problema não é degenerado e o teta original

# Função para verificar restrições redundantes
def verificaRestricoesRedundantes(matriz):
  restricoes = np.delete(matriz, 0, axis=0) # Removendo a primeira linha  referente ao Z ou C
  numRestricoes = len(restricoes) # Identifica a quantidade de restrições
  redundantes = False
  # Percorrendo todas as combinações de linhas das restrições
  for i in range(numRestricoes):
      for j in range(i+1, numRestricoes):
        relacao = np.array(restricoes[j]) / np.array(restricoes[i]) # Calcula a proporcionalidade entre as linhas das retrições
        if np.allclose(relacao, relacao[0]): # Verifica se a proporcionalidade de todos os itens da linha é constante
          print(f"\nRestrição {j+1} é redundante em relação à restrição {i+1}") # Informa a restrição reduntante
          redundantes = True
          return redundantes, j
  if redundantes == False: 
     print("\nNão há restrições redundantes.") # Informa que o problema não possui restrições redundantes
     return redundantes, None
# MAIN
print("TDE OSL SIMPLEX DE MAXIMIZAÇÃO NA FORMA CANÔNICA")
while(1):
  # Solicita que o usuário informe se o problema de maximixar é de lucro ou custo
  tipoFuncaoObjetivo = input("A função objetivo deve maximizar o lucro ou custo? (Z ou C): ")
  if tipoFuncaoObjetivo.upper() == "Z":
    print("Função objetivo: Lucro")
    break

  elif tipoFuncaoObjetivo.upper() == "C":
    print("Função objetivo: Custo")
    break

variaveis = input("Quantas variáveis existem? ") # Usuário deve informar a quantidade de variáveis
try:
  variaveis = int(variaveis)
except:
  raise SystemExit("Valor inválido")

restricoes = input("Quantas restrições existem? ") # Usuário deve informar a quantidade de restrições
try:
  restricoes = int(restricoes)
except:
  raise SystemExit("Valor inválido")

# Cria matriz zerada com base na quantidade de restrições e variaveis
linhas  = (restricoes + 1)
colunas = (variaveis + 1)
matriz = np.zeros((linhas, colunas))

# Solicita que o usuário informe os coeficientes da função objetivo
if tipoFuncaoObjetivo.upper() == "C":
  print("Informe os dados da função objetivo CUSTO ")
if tipoFuncaoObjetivo.upper() == "Z":
  print("Informe os dados da função objetivo LUCRO ")

for i in range(colunas):  # Loop pelas colunas da linha 1 correspondente da função objetivo
  if(i == colunas-1):
    matriz[0][i] = 0 # Não possui lado direito
  else:
    matriz[0][i] = float(input(f"(x{i+1}): ")) # Usuário insere os dados

# Solicita que o usuário informe os coeficientes das restrições
print("Informe os dados das restrições ")
for i in range(linhas):  
    for j in range(colunas): 
        if (i>0):
          if(j == colunas-1):
            matriz[i][j] = float(input(f"(Lado direito da equação): ")) 
          else:
            matriz[i][j] = float(input(f"(x{j+1}): "))

# Imprime o problema com os dados informados
print("\nProblema:")
print("Maximização: ",tipoFuncaoObjetivo.upper()," =", end=" ")
for j in range(colunas):  # loop pelas colunas
  if (matriz[0][j] != 0):
    if (j == colunas - 2):
      if(matriz[0][j]>= 0):
        print(f"{matriz[0][j]} x{j+1}", end=" ")
      else:
        print(f"({matriz[0][j]}) x{j+1}", end=" ")
    else:
      if (matriz[0][j] >= 0):
        print(f"{matriz[0][j]} x{j+1} + ", end=" ")
      else: 
        print(f"({matriz[0][j]}) x{j+1} + ", end=" ")

print('\n')
for i in range(linhas):  # loop pelas linhas
    for j in range(colunas):  # loop pelas colunas
      if (i>0):
        if (j == colunas-1):
          if (matriz[i][j] >= 0):
            print(f" <= {matriz[i][j]} ")
          else:
            print(f" <= ({matriz[i][j]}) ")
        elif (j == colunas-2):
          if (matriz[i][j] >= 0):
            print(f"{matriz[i][j]} x{j+1}", end=" ")
          else:
            print(f"({matriz[i][j]}) x{j+1}", end=" ")
        else:
          if (matriz[i][j] >= 0):
            print(f"{matriz[i][j]} x{j+1} + ", end=" ")
          else:
            print(f"({matriz[i][j]}) x{j+1} + ", end=" ")

#  Verificação se existem restrições redundantes
redundante, j = verificaRestricoesRedundantes(matriz)
if redundante == True:
  j += 1
  matriz = np.delete(matriz, j, axis=0)
  num_variaveis_folga = restricoes-1
  linhas  -= 1
if redundante == False:
  num_variaveis_folga = restricoes
# Equacionando e inserindo variáveis de folga
print("\n===============================================")
print("Equacionando e inserindo variáveis de folga")


colunas_com_folga = variaveis + num_variaveis_folga + 1  # +1 para o lado direito
matriz_com_folga = np.zeros((linhas, colunas_com_folga))
variaveis_base = []
variaveis_nao_base = []

# Copia a função objetivo
for j in range(colunas):
    matriz_com_folga[0][j] = matriz[0][j]

# Adiciona variáveis de folga
for i in range(1, linhas):
    for j in range(colunas - 1):
        matriz_com_folga[i][j] = matriz[i][j]

    # Define a variável de folga correspondente
    matriz_com_folga[i][variaveis + (i - 1)] = 1  # Variável de folga
    variaveis_base.append(variaveis + (i - 1)) # Define as variáveis de base
    matriz_com_folga[i][colunas_com_folga - 1] = matriz[i][colunas - 1]  # Lado direito

listaVariaveisFolga =[]
# Atualiza a função objetivo para incluir as variáveis de folga
for i in range(num_variaveis_folga):
    matriz_com_folga[0][variaveis + i] = 0  # Adiciona coeficiente da variável de folga na função objetivo
    listaVariaveisFolga.append(variaveis + i)

# Exibe o problema após a adição das variáveis de folga
print("\nProblema equacionado:")
print("Maximização: ", tipoFuncaoObjetivo.upper(), " =", end=" ")
for j in range(colunas_com_folga):
  if (j == colunas_com_folga - 2):
    if (matriz_com_folga[0][j] >= 0):
      print(f"{matriz_com_folga[0][j]} x{j+1}", end=" ")
    else:
      print(f"({matriz_com_folga[0][j]}) x{j+1}", end=" ")
  elif (j < colunas_com_folga - 2):
    if (matriz_com_folga[0][j] >= 0):
      print(f"{matriz_com_folga[0][j]} x{j+1} + ", end=" ")
    else:
      print(f"({matriz_com_folga[0][j]}) x{j+1} + ", end=" ")
print('\n')
for i in range(linhas): 
    for j in range(colunas_com_folga):
        if (i > 0):
            if (j == colunas_com_folga - 1):
              if (matriz_com_folga[i][j] >= 0):
                print(f" = {matriz_com_folga[i][j]} ")
              else:
                print(f" = ({matriz_com_folga[i][j]}) ")
            elif (j == colunas_com_folga - 2):
              if (matriz_com_folga[i][j] >= 0):
                print(f"{matriz_com_folga[i][j]} x{j+1}", end=" ")
              else:
                print(f"({matriz_com_folga[i][j]}) x{j+1}", end=" ")
            else:
              if (matriz_com_folga[i][j] >= 0):
                print(f"{matriz_com_folga[i][j]} x{j+1} + ", end=" ")
              else:
                print(f"({matriz_com_folga[i][j]}) x{j+1} + ", end=" ")


# Identificando as variáveis não basicas
for i in range (colunas_com_folga-1):
  if i not in variaveis_base:
    variaveis_nao_base.append(i) # Identifica as variáveis não base

# Inicia a resolução do simplex
iteracao = 1
print("\n===============================================")
print("Iteração ",iteracao,": ")
matrizImpressa = printSimplexTable(matriz_com_folga, variaveis_base, variaveis_nao_base) # Imprime o início da tabela do simplex

while True:
  iteracao += 1
  coef_variaveis_base = coeficienteVariaveisBase(matriz_com_folga,variaveis_base) # Identifica os coeficientes das variaveis base
  Zj = calculoZj(matriz_com_folga,variaveis_base,coef_variaveis_base) # Calculo do Zj
  print("Zj ", '  '.join(f"{z:.1f}" for z in Zj))
  difCjZj = calculoDifCjZj(matriz_com_folga,Zj) # Calculo da diferença de Cj - Zj
  print("Cj-Zj ", '  '.join(f"{d:.1f}" for d in difCjZj))
  if (np.any(difCjZj > 0)): # Verifica de Cj - Zj tem maiores que zero
    maiorValor = np.max(difCjZj) # Identifica o Cj - Zj com maior valor 
    indice_maior_valor = np.argmax(difCjZj) # Identifica o indice do Cj - Zj com maior valor 
    teta,semFronteira = calculaTeta(matriz_com_folga,indice_maior_valor) # Realiza o cálculo do teta
    contadorTeta = 0
    for t in teta:
      print(f"θ x{variaveis_base[contadorTeta] + 1}    {t:.2f}")
      contadorTeta +=1

    # Verificação de problema sem fronteira
    if semFronteira == True:
      print("Problema sem fronteira!")
      break

    # Verificação degeneração
    degenerado, teta = verificaSistemaDegenerado(teta,variaveis_base,matriz_com_folga)

    print("\nIteração ",iteracao,": ") # Informa a iteração 
    menor_teta = np.min(teta) # Identifica o menor teta
    indice_menor_teta = np.argmin(teta) # Identifica a indice do menor teta, correspondente a linha pivo
    variaveis_base[indice_menor_teta] = indice_maior_valor # Atualiza a variavel base após a troca da linha pivo
    matriz_com_folga = manipulacaoSimplex(matriz_com_folga, indice_menor_teta, indice_maior_valor) # Realiza o cálculo do simplex
    matrizImpressa = printSimplexTable(matriz_com_folga, variaveis_base, variaveis_nao_base) # Imprime a tabela do simplex
  else: # Fim do simplex
    zResposta = Zj[-1] # Coloca o último Z ou C calculado
    print("\nResposta:")
    if tipoFuncaoObjetivo.upper() == "Z":
      print("Z = ",zResposta) # Imprimindo Z ótimo
    if tipoFuncaoObjetivo.upper() == "C":
      cResposta = zResposta
      print("C = ",cResposta) # Imprimindo C ótimo
    b = [float(linha[-1]) for linha in matrizImpressa] # Cria uma lista com os valores da coluna b (resultados)
    for i in range(len(variaveis_base)):
      x = variaveis_base[i] # Obtém o índice da variável básica atual
      if x in listaVariaveisFolga: # Verifica se a variável básica é uma variável de folga
        for j in range(variaveis):
          if j not in listaVariaveisFolga and j not in variaveis_base: # Se a variável não é de folga nem básica
            variaveis_base[i] = j # Substitui a variável de folga na base pela primeira variável não básica encontrada
    
    if len(variaveis_base) > variaveis:
      variaveis_base = variaveis_base[:variaveis] # Mantém apenas as variáveis base da função objetivo original
    while len(variaveis_base) < variaveis and len(b) < variaveis: # Enquanto b não está definido preenche ele como 0
      tamanho = len(variaveis_base)
      variaveis_base.append(tamanho)
      b.append(0.0)
    contadorAuxiliar = 0
    for x in variaveis_base:
      print(f"x{x + 1} =", b[contadorAuxiliar]) # Imprime a resposta de cada variavel básica
      contadorAuxiliar +=1
    break
  