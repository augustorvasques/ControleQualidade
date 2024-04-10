import scipy.stats

# Perguntas relacionadas à qualidade
N = int(input("\033[1;34m Qual o tamanho do lote? "))  # tamanho do lote
NQA = float(input("\033[1;34m Qual o NQA (Nível de qualidade aceito pelo cliente? "))  # NQA
PTDL = float(input("\033[1;34m Qual o PTDL (Nível de qualidade ináceitavel ao cliente? "))  # PTDL
P0 = float(input("\033[1;34m Qual a taxa de defeitos histórica do fornecedor? "))
n = int(input("\033[1;34m Quantos itens são inspecionados por lote atualmente? "))  # tamanho da amostra
a = int(input("\033[1;34m Quantos itens defeituosos são tolerados por lote para ser aceito? "))  # tamanho da amostra

# Perguntas relacionadas aos custos
custoU_insp = float(input("\033[1;34m Qual o custo de inspeção por unidade (em R$)? "))  # custo de inspeção por item
custoU_desloc = float(
    input("\033[1;34m Qual o custo de deslocamento em caso de rejeição de lote (em R$)? "))  # custo de deslocamento
num_lotes = int(input("\033[1;34m Para qual horizonte de número de lotes deseja que seja feita a análise?\033[0;0m "))  # horizonte de lotes

# Cálculo do nível de aceitação
print()
Pa = float(scipy.stats.binom.cdf(a, n, P0))
PaPer = 100 * Pa
print("A probabilidade de aceitação de lote no cenário atual é {:.2f}".format(PaPer), "%")
print()

# Cálculo dos riscos associados
risco1 = 1 - scipy.stats.binom.cdf(a, n, NQA)  # Risco do fornecedor
risco2 = scipy.stats.binom.cdf(a, n, PTDL)  # Risco do consumidor
print("\033[0;0m No cenário atual, o risco para o fornecedor é \033[1;31m {:.2f}%\033[0;0m e para o consumidor \033[1;31m{:.2f}%\033[0;0m".format(100 * risco1,
                                                                                                 100 * risco2))
print()

# Cálculo da quantidade média inspecionada por lote e qualidade resultante
ITM = n + (N - n) * (1 - Pa)  # Calcula a quantidade média de itens inspecionada por lote
QMR = Pa * P0 * (N - n) / N  # Indica a qualidade média resultante considerando a inspeção total de lotes rejeitados
print(
    "Além disso, são inspecionados por lote em média {:.2f} itens resultando em uma qualidade média de {:.2f}%".format(
        ITM, 100 * QMR))
print()

# Cálculo dos custos de inspeção no cenário de ocorrer na própria Transformer
custo_insp = num_lotes * ITM * custoU_insp
custo_desloc_transf = num_lotes * (1 - Pa) * custoU_desloc
custo_total_transf = custo_insp + custo_desloc_transf
print("O custo atual no caso de realizá-lo \033[1;31mna sua própria empresa (cliente) é:\033[0;0m \n"
      "custo dos itens inspecionados = R${:.2f}, \n"
      "custo de deslocamento = R${:.2f}, \n"
      "e \033[1;31mcusto total da inspeção = R${:.2f}\033[0;0m".format(custo_insp, custo_desloc_transf, custo_total_transf))
print()


# Cálculo dos custos de inspeção no cenário de ocorrer na Resistok
custo_desloc_resistok = 0
custo_total_resistok = custo_insp + custo_desloc_resistok
print("O custo atual no caso de realizá-lo \033[1;31mno seu fornecedor é:\033[0;0m \n"
      "custo dos itens inspecionados = R${:.2f},\n"
      "custo de deslocamento = R${:.2f}, \n"
      "e \033[1;31mcusto total da inspeção = R${:.2f}\033[0;0m".format(custo_insp, custo_desloc_resistok, custo_total_resistok))
print()
print()

# Calcula o menor tamanho de amostra (n) que satisfaça às restrições dos Erros tipo I e II
# N = 10000  # tamanho do lote
# NQA = 0.03  # NQA
# PTDL = 0.06  # PTDL

alfa_max = risco1  # risco máximo aceito pelo fornecedor
beta_max = risco2  # risco máximo aceito pelo consumidor

custo_min = custo_total_transf #Joga os mínimos para valores altos para iniciar a comparação
alfa_min = 1000000
beta_min = 100000
contagem = 0 #Inicia a contagem de planos propostos com custo menor

print("Segue abaixo opções com planos que possuem custos cada vez menores, e riscos iguais ou menores aos atuais:")
for n2 in range(1, N + 1):  # varre todos os possíveis tamanho de amostra no lote
    for a2 in range(0, n2 + 1):  # varre todos os possíveis índices de aceitação para um tamanho de amostra
        Pa = float(scipy.stats.binom.cdf(a2, n2, P0))
        ITM = n2 + (N - n2) * (1 - Pa)  # Calcula a quantidade média de itens inspecionada por lote
        custo_insp2 = num_lotes * ITM * custoU_insp
        custo_desloc_transf2 = num_lotes * (1 - Pa) * custoU_desloc
        custo_total_transf2 = custo_insp2 + custo_desloc_transf2
        if custo_total_transf2 < custo_min:
            alfa_calc = 1 - scipy.stats.binom.cdf(a2, n2, NQA)  # calcula o risco do fornecedor
            beta_calc = scipy.stats.binom.cdf(a2, n2, PTDL)  # calcula o risco do consumidor
            if alfa_calc <= alfa_max and beta_calc <= beta_max:
                contagem = contagem + 1 #Aumenta o valor da contagem a cada plano encontrado que atenda as condições
                custo_min = custo_total_transf2 #As linhas daqui para baixo guardam os dados do plano que obtiver o custo mínimo para que possam continuar os testes sem perder os valores
                alfa_min = alfa_calc
                beta_min = beta_calc
                n_min = n2
                a_min = a2
                Pa_min = Pa
                print("{})   Custo = R${:.2f}, Risco Fornecedor = {:.2f}%, Risco Consumidor = {:.2f}%, Tamanho da amostra = {}, Limite de defeituosos aceitável = {}, Probabilidade de aceitação do lote = {:.2f}%".format(contagem, custo_min, alfa_min*100, beta_min*100, n_min, a_min,Pa_min*100))
                print("\033[1;36m_\033[0;0m"*130)
        if a2>n2-1:
            break  # quebra o loop interno
    if N>5000: #Para lotes muito grandes, limita-se a busca por tamanhos de amostra de até 10 vezes menor que o lote
        if n2>N/10:
            break # sai do for externo
    else:
        if n2>N/5: #Para lotes menores, limita-se a busca por tamanhos de amostra de até 5 vezes menor que o lote
            break  # sai do for externo

print()
print()

print("\033[0;32mPortanto, o plano de inspeção que minimiza os custos de inspeção mantendo os riscos máximos é:\n"
      "Custo mínimo total de inspeção: R${:.2f} \n"
      "Risco mínimo fornecedor: {:.2f}% \n"
      "Risco mínimo consumidor: {:.2f}\n".format(custo_min, alfa_min*100, beta_min*100))



print(
    "Este novo plano de inspeção proposto pode ser traçado inspecionando {} itens por lote na empresa do cliente, aceitando no máximo {} defeituosos.".format(n_min, a_min))
print()


# Cálculo dos custos associados ao novo plano proposto
# Cálculo do nível de aceitação
PaPer = 100 * Pa_min
print("A probabilidade de aceitação de lote no novo plano proposto é {:.2f}".format(PaPer), "%")
print()

# Cálculo da quantidade média inspecionada por lote e qualidade resultante
ITM = n_min + (N - n_min) * (1 - Pa_min)  # Calcula a quantidade média de itens inspecionada por lote do novo plano
QMR = Pa_min * P0 * (N - n_min) / N  # Indica a qualidade média resultante considerando a inspeção total de lotes rejeitados
print(
    "Além disso, serão inspecionados por lote em média {:.2f} itens resultando em uma qualidade média de {:.2f}%".format(
        ITM, 100 * QMR))
print()

#Desdobrando os custos do plano com custo mínimo
custo_insp_min = num_lotes * ITM * custoU_insp
custo_desloc_min = num_lotes * (1 - Pa_min) * custoU_desloc

# Cálculo dos custos de inspeção no cenário de ocorrer na própria Transformer
print("O custo do novo plano proposto no caso de realizá-lo na sua própria empresa (cliente) é:\n"
      "custo dos itens inspecionados = R${:.2f}, \n"
      "custo de deslocamento = R${:.2f}, \n"
      "e custo total da inspeção = R${:.2f},\n"
      "economizando ao todo R${:.2f} em comparação ao plano anterior\033[0;0m".format(custo_insp_min, custo_desloc_min,
                                                                              custo_min,
                                                                              custo_total_transf - custo_min))
print()
print()
print("\033[1;36m _ \033[0;0m"*80)

print("Agora analisando novos planos para o cenário da inspeção ser feita no fornecedor: \n")
custo_min = custo_total_transf  # Joga os mínimos para valores altos para iniciar a comparação
alfa_min = 1000000
beta_min = 100000
contagem = 0 #Inicia a contagem de planos propostos com custo menor

print( "Segue abaixo opções com planos que possuem custos cada vez menores, e riscos iguais ou menores aos atuais:")
for n2 in range(1, N + 1):  # varre todos os possíveis tamanho de amostra no lote
    for a2 in range(0, n2 + 1):  # varre todos os possíveis índices de aceitação para um tamanho de amostra
        Pa = float(scipy.stats.binom.cdf(a2, n2, P0))
        ITM = n2 + (N - n2) * (1 - Pa)  # Calcula a quantidade média de itens inspecionada por lote
        custo_insp2 = num_lotes * ITM * custoU_insp
        custo_total_resistok2 = custo_insp2 #Some o custo de deslocament pois no cenário da empresa fornecedora é 0
        if custo_total_resistok2 < custo_min:
            alfa_calc = 1 - scipy.stats.binom.cdf(a2, n2, NQA)  # calcula o risco do fornecedor
            beta_calc = scipy.stats.binom.cdf(a2, n2, PTDL)  # calcula o risco do consumidor
            if alfa_calc <= alfa_max and beta_calc <= beta_max:
                contagem = contagem + 1
                custo_min = custo_total_resistok2  # As linhas daqui para baixo guardam os dados do plano que obtiver o custo mínimo para que possam continuar os testes sem perder os valores
                alfa_min = alfa_calc
                beta_min = beta_calc
                n_min = n2
                a_min = a2
                Pa_min = Pa
                print(
                    "{})   Custo = R${:.2f}, Risco Fornecedor = {:.2f}%, Risco Consumidor = {:.2f}%, Tamanho da amostra = {}, Limite de defeituosos aceitável = {}, Probabilidade de aceitação do lote = {:.2f}%".format(
                        contagem, custo_min, alfa_min * 100, beta_min * 100, n_min, a_min, Pa_min * 100))
                print("\033[1;36m_\033[0;0m" * 130)
        if a2 > n2 - 1:
            break  # quebra o loop interno
    if N > 5000:  # Para lotes muito grandes, limita-se a busca por tamanhos de amostra de até 10 vezes menor que o lote para diminuir o tempo de processamento
        if n2 > N / 10:
            break  # sai do for externo
    else:
        if n2 > N / 5:  # Para lotes menores, limita-se a busca por tamanhos de amostra de até 10 vezes menor que o lote
            break  # sai do for externo


print()
print()

print("\033[0;32mPortanto, o plano de inspeção que minimiza os custos de inspeção mantendo os riscos máximos é:\n"
      "Custo mínimo total de inspeção: R${:.2f}\n"
      "Risco mínimo fornecedor: {:.2f}% \n"
      "Risco mínimo consumidor: {:.2f}".format(custo_min, alfa_min*100, beta_min*100))
print()

print("Este novo plano de inspeção proposto pode ser traçado inspecionando {} itens por lote na empresa do fornecedor, aceitando no máximo {} defeituosos.".format(n_min, a_min))
print()

# Cálculo dos custos associados ao novo plano proposto
# Cálculo do nível de aceitação
PaPer = 100 * Pa_min
print("A probabilidade de aceitação de lote no novo plano proposto é {:.2f}".format(PaPer), "%")
print()

# Cálculo dos custos de inspeção no cenário de ocorrer na Resistok (fornecedor)
print("O custo do novo plano proposto no caso de realizá-lo na sua própria empresa (cliente) é:\n"
      "custo dos itens inspecionados = R${:.2f},\n"
      "custo de deslocamento = R$ 0,00,\n"
      "e custo total da inspeção = R${:.2f},\n"
      "economizando ao todo R${:.2f} em comparação ao plano anterior caso estiver sendo executado no fornecedor atualmente.\033[0;0m".format(custo_min,
                                                                              custo_min,
                                                                              custo_total_resistok - custo_min))
