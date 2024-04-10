# ControleQualidade
Projeto da disciplina de Controle Estatístico da Qualidade avaliado com nota máxima. Consiste em um estudo de caso de "Controle da Qualidade na Produção de Transformadores da Empresa Transformer", no qual foi criado um código pyhton para realizar diagnóstico do poder estatístico e custos do plano de inspeção em vigor, para assim, recomendar se possível, novos planos com no mínimo o mesmo poder estatístico (riscos associados às duas partes) mas com custo total reduzido.

## Contexto
A Transformer é uma empresa que fabrica transformadores de uso doméstico, realizando inspeções de recebimento em vários componentes eletrônicos adquiridos de seus fornecedores. Um componente crucial usado na montagem dos transformadores é fornecido pela Resistok, em lotes de 10.000 unidades que são entregues diariamente. Historicamente, a Resistok tem uma taxa de defeito de 2% para esse componente.

Atualmente, a Transformer exige que cada lote seja avaliado pela Resistok, na presença de um funcionário da Transformer, usando um plano de amostragem simples com nível geral de inspeção II e Nível de Qualidade Aceitável (NQA) de 1,5%. Os custos de inspeção são cobertos pela Resistok. Devido a problemas de qualidade atribuídos aos componentes da Resistok, a Transformer decidiu mudar a inspeção dos lotes para suas próprias instalações, na esperança de reduzir os defeitos. Em ambos os cenários, o custo de inspeção por item é de $0,50, a despesa de deslocamento de um funcionário da Resistok para a Transformer é de $500 e a Transformer considera inaceitável taxas de defeitos acima de 5%.

## Importante
Apesar de ter o exemplo como base, o código foi adaptado para suportar entradas de diferentes planos de inspeção e com isso ser flexível para propor melhores planos para diferentes e contextos.
