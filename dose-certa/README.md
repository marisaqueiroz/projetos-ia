# Dose Certa — análise do resíduo de terra da refinaria

**2º lugar na categoria Ciência de Dados do O-HACKA-TA-ON 2025 (M. Dias Branco).** Projeto em dupla, com continuidade em andamento.

> As bases de dados detalhadas e o arquivo do Power BI não são publicados, por pertencerem à empresa. Este README descreve o método e os resultados. Uma versão web do painel, com valores consolidados por mês, está em [painel-dose-certa](../painel-dose-certa/) ([demonstração online](https://SEU-USUARIO.github.io/projetos-ia/painel-dose-certa/)).

## Problema

Geração, em vários meses, de resíduo de terra da refinaria muito acima do volume esperado, com perdas no processo produtivo e aumento dos custos de transporte e destinação.

## Fontes de dados

- **SAP:** consumo sistêmico de insumos.
- **SINIR/MTR:** resíduos gerados, transporte e destinação (mais de 900 manifestos, jan/2024 a set/2025; 19 meses com dados completos na análise).
- **ST-One:** vazão do processo e set-point de dosagem.
- **Quadro mensal da refinaria:** produção e dosagem real.

## Como a IA foi usada

Integração de dados dos sistemas nativos (SAP, SINIR e ST-One) em Python para cálculo do volume de terra esperado, com base na aplicação dos insumos e da receita de fabricação, e comparação com o resíduo real gerado. Elaboração de painéis em Power BI, software adotado pela empresa, desenvolvidos com apoio de IA para definição das informações relevantes do painel, design e interpretação dos dados.

## Método

1. **Resíduo esperado:** soma dos insumos dosados no mês (terra, perlita, catalisador de níquel, sílica e metilato) mais o óleo retido no resíduo, estimado em 30% do resíduo gerado.
2. **Excesso de resíduo:** resíduo real (SINIR) menos o resíduo esperado.
3. **Perda de óleo estimada:** excesso × 30% de óleo × R$ 6,60/kg de óleo de palma bruto (premissas a validar com análise de composição).
4. **Dosagem:** quantidade real × quantidade sistêmica (SAP) × quantidade calculada (vazão × set-point, ST-One), valorizadas pelo R$/kg de cada insumo.
5. **Logística do excesso:** toneladas excedentes de cada mês × custo real por tonelada de transporte e destinação do mesmo mês.

## Resultados (jan/2024 a jul/2025)

- Resíduo acima do esperado em **15 de 19 meses**, com excesso líquido de **265,5 t** (224,8 t em 2024, 12,3% acima do esperado; 40,6 t em jan–jul/2025, 4,1% acima).
- Em 2025, o excesso se concentra em junho, mês que responde por 52% da perda de óleo estimada do ano.

| Item | Valor estimado |
|---|---|
| Perda de óleo (79,6 t) | R$ 526 mil |
| Terra Natural dosada acima do calculado (218 t) | R$ 252 mil |
| Transporte e destinação do excesso de resíduo | R$ 78 mil |
| **Total** | **≈ R$ 856 mil** |

- A Terra Natural (B3) foi dosada 18,5% acima do sistêmico em 2024.
- A Terra Acidificada ficou abaixo do calculado no período, de modo que o prejuízo é específico da Terra Natural.
- Os custos de transporte e destinação somaram cerca de R$ 0,82 mi reportados no período (R$ 0,89 mi com a estimativa de destinação das MTRs sem custo), equivalentes a R$ 270 a R$ 293 por tonelada.
- Índice de geração de resíduos de **16,2 kg por tonelada produzida** no período.

## Validação e correção das bases

A revisão das bases antes da publicação identificou e corrigiu:

- método de cálculo do excesso diferente entre 2024 e 2025, unificado pelo método descrito acima;
- lançamentos de produção em unidade errada ou divergentes da fonte (jun/2024, set/2024, abr/2025, jun/2025);
- MTRs canceladas e linhas duplicadas somadas ao resíduo gerado;
- MTRs de destinação sem custo registrado (jan–abr/2024), tratadas por estimativa com tarifa explícita e resultado também apresentado sem a estimativa;
- indicador de geração de resíduos do painel (17,84 kg/t) calculado com períodos desalinhados e MTRs canceladas, substituído por 16,2 kg/t. As medidas corrigidas estão em [medidas-powerbi.md](medidas-powerbi.md).

## Painéis (Power BI)

1. **Visão geral:** resíduo por mês, custos de transporte e destinação, filtros por ano, mês e tipo de tratamento.
2. **Dosagem de insumos:** quantidade real × sistêmica × calculada, por insumo e por mês, e custo total dos insumos.

## Limitações e próximos passos

- Os valores em reais são estimativas, dependentes das premissas de 30% de óleo no excesso e R$ 6,60/kg.
- Resíduo do quadro (SINIR) e soma das MTRs divergem em alguns meses de 2024 (diferença líquida de 55 t), pendentes de conferência na fonte.
- Meses de ago e set/2025 fora da análise, até a confirmação dos dados de produção.
- Custo de destinação das MTRs de jan–abr/2024 a substituir pela tarifa contratual.
- Análise da composição do resíduo de terra, para validar a premissa de óleo.
- Cálculo de dosagem teórica para Hidro/Inter e comparativos de consumo físico × sistêmico × especificação técnica.
- Revisão da lógica de abertura do sistema de copo (B3).
- Monitoramento do indicador de geração por produção, diferenciando os prédios 1 e 2.
- Automação da coleta de dados para visualização em tempo real.
