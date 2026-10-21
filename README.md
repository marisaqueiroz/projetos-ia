# Projetos de IA aplicados à gestão ambiental

**Marisa Queiroz Mendonça** · Engenheira Ambiental (UFC, 2026) · Fortaleza, CE

Repositório com projetos em que a IA foi aplicada a problemas reais de conformidade ambiental, gestão de resíduos, geoprocessamento e licenciamento. Em todos eles, a IA é direcionada por critérios técnicos definidos previamente, e os resultados passam por conferência humana antes de qualquer uso.

> **Demonstrações online:** [painel da ETE](https://SEU-USUARIO.github.io/projetos-ia/painel-ete-pici/) · [painel Dose Certa](https://SEU-USUARIO.github.io/projetos-ia/painel-dose-certa/)
> (substituir `SEU-USUARIO` pelo nome de usuário do GitHub)

## Projetos

| Projeto | O que faz | Pasta |
|---|---|---|
| **Painel de Diagnóstico da ETE do Campus do Pici** (TCC, UFC) | Painel interativo que avalia o desempenho e a conformidade legal de uma estação de tratamento de esgoto antes e depois da reforma, a partir de 27 campanhas laboratoriais. | [painel-ete-pici](painel-ete-pici/) |
| **Dose Certa** (2º lugar, Ciência de Dados, O-HACKA-TA-ON 2025, M. Dias Branco) | Análise do resíduo de terra de uma refinaria de óleos, comparando o volume real com o esperado e estimando perdas de óleo, de insumos e de transporte e destinação. | [dose-certa](dose-certa/) · [painel web](painel-dose-certa/) |
| **Agente de ART (CREA-CE)** | Preenchimento automático da ART no portal do CREA-CE, com parada antes da finalização e conferência final humana. Economia de cerca de 30 minutos por ART. | [agente-art-crea](agente-art-crea/) |
| **Agente de matrícula para shapefile** | Conversão de matrículas e memoriais de imóveis em poligonais georreferenciadas (shapefile, DXF e prévia), com validação de área e perímetro. Economia de cerca de 1 dia de trabalho. | [agente-matricula-shapefile](agente-matricula-shapefile/) |
| **Complemento de IA para QGIS** | Apoio de IA na produção de mapas no QGIS, com automação de layouts em desenvolvimento. Economia de cerca de 3 dias de trabalho na elaboração. | [complemento-qgis](complemento-qgis/) |

## Como a IA é usada

- **Direcionamento:** definição prévia do problema, das fontes de dados e dos critérios técnicos (por exemplo, a legislação vigente em cada época no painel da ETE).
- **Verificação:** comparação dos resultados com as fontes originais e com os valores declarados (por exemplo, área calculada × área da matrícula, com tolerância de até cerca de 0,5%).
- **Limite de autonomia:** o agente de ART interrompe o processo antes de finalizar o cadastro, e a conferência final é do profissional responsável.

## Ferramentas

Python, Power BI, QGIS, SAP, Claude (skills e automações no navegador), JavaScript (Chart.js).

## Privacidade

Dados de empresas, clientes e proprietários de imóveis não são publicados. Os exemplos das ferramentas usam dados fictícios, e as bases do Dose Certa permanecem restritas à empresa.

## Contato

marisaam44@gmail.com · [LinkedIn](https://www.linkedin.com/in/marisa-queiroz-a52b301b6)
