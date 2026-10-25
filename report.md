# Relatório de Análise — Festa em Cena

## Resumo da limpeza e validação
Foram lidos 1.500 pedidos. Na padronização de texto, 18 categorias vazias foram preenchidas com "sem categoria" e 55 categorias não vazias sofreram alteração de conteúdo. 45 canais de venda precisaram ser padronizados para os valores oficiais (Web, Loja física e Mercado).  

Na validação numérica, identificamos 7 erros de quantidade (valores não inteiros ou ≤ 0) e 12 erros de preço (ausentes ou negativos), totalizando 19 pedidos com problema. Não houve sobreposição entre os dois tipos de erro. Quatro datas de venda eram inválidas e foram marcadas, sem substituição.

## Hipótese de negócio
A hipótese de que todo pedido sem data de entrega seria Cancelado mostrou-se falsa. Dos 143 pedidos sem data de entrega, 109 eram de fato Cancelados, mas 34 estavam com status Concluído. Esses 34 casos constituem contraexemplos claros e devem ser investigados antes de qualquer uso dos dados em modelos ou relatórios gerenciais.

## Descobertas
**Por canal:** o canal Web lidera em volume de pedidos (666), seguido pela Loja física (551) e pelo Mercado (283). Embora o Mercado tenha menos pedidos, análises complementares indicam que ele apresenta maior quantidade média de unidades por pedido. As contagens refletem pedidos registrados, não receita nem vendas concluídas.

**Por período:** outubro concentra o pico de pedidos nos dois anos analisados (393 em 2024 e 410 em 2025), coerente com a proximidade do Halloween. A base cobre apenas os meses de agosto a novembro; portanto, não é possível afirmar o comportamento sazonal no restante do ano. Quatro pedidos foram excluídos da contagem mensal por data inválida.

## Conclusão
A qualidade dos dados exige atenção antes de qualquer análise ou modelagem. Marcar problemas em vez de imputar valores preserva a transparência e evita a introdução de viés. Os 34 pedidos concluídos sem data de entrega e os erros numéricos identificados são pontos que devem ser resolvidos na origem dos dados. Com a limpeza documentada, a base fica adequada para análises descritivas e, futuramente, para experimentos de Machine Learning, desde que as limitações de representatividade e o período coberto sejam considerados.