# Painel de Diagnóstico da ETE do Campus do Pici (UFC)

Painel interativo desenvolvido como apoio ao TCC em Engenharia Ambiental (UFC). O arquivo `index.html` funciona direto no navegador, sem instalação.

**Demonstração:** https://marisaqueiroz.github.io/projetos-ia/painel-ete-pici/

## Problema

Avaliação da melhoria da estação de tratamento de esgoto (ETE) do Campus do Pici após a reforma de 2023, o que exigiu comparar 27 campanhas laboratoriais mensais (jan/2024 a mai/2026) com o diagnóstico de 2008, avaliando tanto o desempenho operacional quanto o atendimento à conformidade legal sob legislações que se atualizaram.

## Como a IA foi usada

Fornecimento dos laudos de entrada e saída e da legislação de cada época (CONAMA 357/2005 e Portaria SEMACE 154/2002 em 2008; COEMA 02/2017 atualmente) e direcionamento da construção do painel interativo para facilitar a análise: obtenção de insights, confronto de informações e compreensão do que os dados indicavam sobre o funcionamento da ETE e sobre o atendimento aos parâmetros de conformidade legal.

## Decisões metodológicas

- **Comparação pela concentração do efluente frente ao limite legal**, e não pelo percentual de remoção, porque a eficiência depende da concentração de entrada, que era muito maior em 2008 e não é controlada pela ETE.
- **Média geométrica para coliformes**, prática padrão em saneamento e mesma base usada no diagnóstico de 2008, para que picos pontuais não distorçam o valor representativo.
- **Legislação de cada época:** Portaria SEMACE 154/2002 e CONAMA 357/2005 em 2008; COEMA 02/2017 no período atual.

## Resultados

| Indicador | 2008 | Pós-reforma |
|---|---|---|
| DBO do efluente | 105 mg/L (acima do limite da época) | 19 mg/L (limite atual: 120 mg/L) |
| Coliformes termotolerantes (média geométrica) | 9,5×10⁴ NMP/100 mL | 1,8 NMP/100 mL |
| SST do efluente | 11,5 mg/L | 38,1 mg/L (conforme; limite atual: 100 mg/L) |

- Efluente em conformidade com os 5 parâmetros da COEMA 02/2017 (DBO, SST, coliformes, sulfetos e óleos e graxas) em 100% das campanhas.
- Operação a 98,8% da capacidade hidráulica de projeto (456,72 de 462,24 m³/dia em mai/2026), o que reduz a margem para picos de vazão na quadra chuvosa.
- Substituição de planilhas e da conferência manual de parâmetros por painel que se atualiza a cada nova campanha.

## Seções do painel

Visão geral · 2008 × situação atual · indicadores de evolução · capacidade hidráulica · conformidade legal · desempenho do tratamento · estabilidade operacional · evolução temporal.

## Limitações

- O monitoramento atual contempla 5 parâmetros. O diagnóstico de 2008 avaliou também DQO, nitrogênio, fósforo e sólidos dissolvidos, ausentes hoje.
- Dez/2023 e fev/2024 não possuem tabela laboratorial e aparecem como lacunas.
- A média de SST atual é elevada por episódios pontuais de arraste de sólidos no decantador (mediana de 26 mg/L).

## Como atualizar

Os dados ficam no arranjo `SERIES` dentro do `index.html`. Para incluir novas campanhas, basta acrescentar um objeto no mesmo formato.

## Fontes

Relatórios mensais de operação (Rede Ambiental) e laudos laboratoriais (TECH LAB), de dez/2023 a mai/2026. Diagnóstico de 2008: PEIXOTO, M. S. *Diagnóstico operacional do sistema de lodos ativados da ETE do Campus do Pici*. Dissertação de Mestrado, UFC, 2008.
