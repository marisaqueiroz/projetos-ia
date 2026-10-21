# Agente de ART (CREA-CE)

Agente de IA para preenchimento da ART (Anotação de Responsabilidade Técnica) no portal do CREA-CE (sistema SITAC), executado pelo navegador com o Claude in Chrome. **Economia de cerca de 30 minutos por ART.**

Uma *skill* é um conjunto de instruções, referências e scripts que o Claude carrega quando a tarefa pede. Aqui, o arquivo `SKILL.md` define o fluxo, e a pasta `references` guarda o conhecimento do portal.

## Problema

O preenchimento da ART exige digitar dados do contratante, endereço da obra, coordenadas, atividades técnicas e declarações, e escolher, em uma árvore extensa, as atividades corretas para cada estudo. O processo é repetitivo e sujeito a erros de transcrição.

## O que o agente faz

1. **Prepara os dados:** lê o cartão CNPJ do contratante, extrai as coordenadas do KML/KMZ do empreendimento (`scripts/kml_ponto.py`) e mapeia as atividades técnicas a partir do estudo ou termo de referência, guardando o item que justifica cada uma.
2. **Preenche o formulário no portal**, seção por seção, aplicando padrões previamente definidos para os campos ausentes.
3. **Para antes da finalização.** O agente não salva definitivamente, não emite e não gera boleto.
4. **Entrega um relatório curto:** atividades lançadas com o trecho do documento que as justifica, valores assumidos por padrão e pontos que exigem atenção.

## Salvaguardas

- **Conferência final humana:** o profissional responsável confere e finaliza a ART.
- **Alerta de UF:** se a coordenada estiver fora do estado, o agente interrompe, porque o CREA provável é outro.
- **Sem invenção de códigos:** atividades fora do catálogo são buscadas na árvore do portal e, se não houver segurança, ficam de fora e são relatadas.
- **Sem dados pessoais:** o repositório não guarda nome, RNP ou registro de profissionais.

## Arquivos

| Arquivo | Função |
|---|---|
| `SKILL.md` | Fluxo de trabalho do agente |
| `references/crea-ce.md` | Ordem dos campos, padrões, catálogo de atividades e mapa estudo → atividades do CREA-CE |
| `scripts/kml_ponto.py` | Extração de ponto (lat, lon) de KML/KMZ, com centroide seguro para polígonos em L ou U |

## Limitações

- Mapeado apenas o CREA-CE. Outros CREAs exigem mapeamento prévio, descrito no fim do `SKILL.md`.
- O catálogo de atividades cobre as usadas até o momento, e itens marcados como `[A MAPEAR]` dependem de confirmação no portal.
