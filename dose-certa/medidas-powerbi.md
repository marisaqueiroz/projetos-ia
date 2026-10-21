# Dose Certa — medidas e ajustes do modelo no Power BI

Ajustes aplicados ao painel após a validação das bases. Não há dados neste arquivo, apenas a lógica.

## 1. Remoção de linhas duplicadas (Power Query)

Na tabela `Transporte e Destinação`, após o passo de tipos de dados, incluir um novo passo:

```
= Table.Distinct(<passo anterior>)
```

Registros 100% repetidos (mesmo MTR, data, quantidade e custos) são removidos antes do carregamento.

## 2. Relacionamentos

Relacionar a tabela `Calendario` às duas tabelas de fatos pela coluna `ChaveAnoMes` (um para muitos, filtro em direção única, do calendário para as tabelas):

- `Calendario[ChaveAnoMes]` → `Transporte e Destinação[ChaveAnoMes]`
- `Calendario[ChaveAnoMes]` → `Acompanhamento produção[ChaveAnoMes]`

Com isso, os filtros de ano e mês do painel passam a valer para resíduo e produção ao mesmo tempo. Para limitar a análise aos meses com dados completos, aplicar filtro de página em `Calendario[ChaveAnoMes]` até 202507.

## 3. Medidas

```DAX
Resíduo gerado (kg) =
CALCULATE (
    SUM ( 'Transporte e Destinação'[Qntd Indicada (kg)] ),
    'Transporte e Destinação'[Situação] <> "Cancelado"
)
```

```DAX
Produção total (t) =
CALCULATE (
    SUM ( 'Acompanhamento produção'[Quantidade Real (t)] ),
    'Acompanhamento produção'[Tipo] = "Produção"
)
```

```DAX
Índice de geração (kg/t) =
DIVIDE ( [Resíduo gerado (kg)], [Produção total (t)] )
```

## 4. Por que a medida anterior estava incorreta

A medida original dividia a soma de todas as MTRs (incluindo canceladas, duplicadas e de meses sem produção correspondente) pela produção de todos os meses, sem relacionamento de período entre as tabelas. O resultado (17,84 kg/t) ficava acima do valor real do período (16,2 kg/t).
