# Painel Dose Certa (versão web)

Versão em página web do painel do projeto **Dose Certa** (2º lugar, Ciência de Dados, O-HACKA-TA-ON 2025, M. Dias Branco), com valores consolidados por mês e bases já validadas.

**Demonstração online:** https://SEU-USUARIO.github.io/projetos-ia/painel-dose-certa/

## O que o painel mostra

- Resíduo de terra real × esperado, por mês.
- Perda de óleo estimada (R$), com meses abaixo do esperado em verde.
- Dosagem de terra natural real × calculada (vazão × set-point).
- Índice de geração de resíduos (kg por tonelada produzida).
- Indicadores do período, com filtro por 2024, 2025 ou todo o período.

## Como foi feito

Página única (`index.html`) com gráficos em Chart.js, gerada com apoio de IA a partir da planilha de análise validada. Os dados estão no próprio arquivo, na constante `D`, com um registro por mês (19 meses).

## Dados publicados

Apenas valores consolidados por mês. Bases detalhadas, manifestos (MTR), fornecedores e preços unitários não fazem parte do repositório. O painel original em Power BI não é publicado, por pertencer à empresa.

## Atualização

Para incluir novos meses, acrescentar um registro à constante `D` do `index.html` (campos: rótulo, ano, resíduo real e esperado em t, excesso em t, perda de óleo em R$, logística em R$, índice kg/t, terra natural real e calculada em t e sobredose em R$). A planilha de análise gera esses valores por fórmula.

Método, premissas e correções das bases: ver [dose-certa](../dose-certa/).
