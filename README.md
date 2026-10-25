# Festa em Cena — Análise de Pedidos de Halloween

## Objetivo

   Limpar e explorar o dataset de pedidos da rede fictícia **Festa em Cena** (fantasias e acessórios de Halloween), identificando e tratando problemas de qualidade de dados antes de qualquer análise ou uso em modelos de Machine Learning.

   O projeto aplica técnicas de leitura controlada, padronização de texto, validação de valores e tratamento de datas, sempre documentando as decisões e evitando a invenção de dados.

## O que representa uma linha

   Cada linha do arquivo `halloween_vendas.csv` representa **um pedido de um único produto** (que pode conter várias unidades).  
   Os dados são fictícios e contêm problemas intencionais para fins de aprendizado.  
   A base possui 1.500 pedidos registrados entre agosto e novembro de 2024 e 2025.

## Colunas principais

- `pedido_id`: identificador único do pedido
- `data_venda`: data e hora da venda (formato original `YYYY-MM-DD HH:MM:SS`)
- `produto`: nome do produto vendido
- `categoria`: categoria do produto (pode vir suja ou vazia)
- `canal_venda`: canal pelo qual o pedido foi feito
- `quantidade`: quantidade de unidades no pedido
- `preco_unitario`: preço unitário do produto
- `status_pedido`: status do pedido (Concluído, Cancelado, Devolvido)
- `data_entrega`: data de entrega (pode estar vazia)

## Regras de tratamento adotadas

   ### Categoria
   - Aplicados `.strip()` e `.lower()`.
   - Uso de `re.sub(r"[^a-z ]", "", ...)` para remover pontuação indevida.
   - Valores vazios após a limpeza foram preenchidos com `"sem categoria"`.
   - **Resultado**: 18 categorias vazias preenchidas e 55 categorias não vazias alteradas.

   ### Canal de venda
   - Padronizado para os valores oficiais: `Mercado`, `Loja física` e `Web`.
   - **Resultado**: 45 canais precisaram de padronização.

   ### Quantidade e preço
   - `quantidade` deve ser um inteiro maior que zero.
   - `preco_unitario` deve estar preenchido e ser não negativo.
   - Registros com problemas foram marcados com flags, sem imputação de valores.
   - **Resultado**: 7 erros de quantidade, 12 erros de preço e 19 pedidos com algum problema (sem sobreposição).

   ### Datas
   - `data_venda` convertida com `pd.to_datetime(errors="coerce")`.
   - Criada coluna no formato brasileiro (`dd/mm/aaaa`).
   - Datas inválidas foram marcadas, sem substituição.
   - **Resultado**: 4 datas de venda inválidas.

## Resultados principais

   ### Hipótese de negócio
   **Hipótese testada**: todo pedido sem `data_entrega` tem status `Cancelado`.

   **Conclusão**: a hipótese é **falsa** nesta base.  
   - 143 pedidos sem data de entrega  
   - 109 são Cancelados  
   - 34 são Concluídos (contraexemplos)

   ### Contagem por canal (todos os status)
   | Canal       | Pedidos |
   |-------------|---------|
   | Web         | 666     |
   | Loja física | 551     |
   | Mercado     | 283     |

   ### Contagem por ano-mês (apenas datas válidas)
   | Ano  | Ago | Set | Out | Nov |
   |------|-----|-----|-----|-----|
   | 2024 | 77  | 104 | 393 | 174 |
   | 2025 | 62  | 94  | 410 | 182 |

   **Observação**: 4 pedidos foram excluídos desta contagem por data inválida.

## Descobertas

   ### Descoberta 1 — Por canal

   O canal **Web** concentra o maior volume de pedidos (666), seguido pela Loja física (551). O Mercado tem menos pedidos (283), mas, segundo análises complementares da turma, apresenta maior quantidade média de unidades por pedido.  
   **Limitação**: as contagens representam pedidos registrados, não receita nem vendas concluídas.

   ### Descoberta 2 — Por período

   Outubro é claramente o mês de pico nos dois anos (393 pedidos em 2024 e 410 em 2025), coerente com a proximidade do Halloween (31 de outubro).  
   **Limitação**: a base cobre apenas os meses de agosto a novembro; não é possível afirmar o comportamento no restante do ano.

## Reflexão sobre qualidade de dados e Machine Learning

A qualidade dos dados é determinante para o desempenho de modelos de Machine Learning. Problemas como valores ausentes, inconsistências de texto, datas inválidas e regras de negócio não verificadas podem introduzir viés, reduzir a capacidade de generalização e gerar previsões enganosas. Neste projeto, optamos por marcar e separar os problemas em vez de imputar valores, preservando a transparência. Em um cenário real, a etapa de limpeza e validação documentada é tão importante quanto a escolha do algoritmo, pois “lixo entra, lixo sai”.

## Como executar o projeto

1. Clone o repositório e entre na pasta.
2. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
4. Execute o script principal (a partir da raiz do projeto):
   ```bash
   python src/main.py

## Estrutura do projeto
```
festa_em_cena/
├── dados/
│   └── halloween_vendas.csv
├── src/
│   ├── funcoes.py
│   └── main.py
├── README.md
├── report.md
├── requirements.txt
└── .gitignore
```
