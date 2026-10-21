# CREA-CE — ART de Obra/Serviço (sistema SITAC)

Portal: sistema SITAC do CREA-CE (verificação pública em https://crea-ce.sitac.com.br/publico/).
Este arquivo foi montado a partir de ARTs de obra/serviço já emitidas no CREA-CE.
Itens marcados [A MAPEAR] ainda precisam ser confirmados na tela do portal, numa
sessão com o Chrome.

## Sumário
1. Ordem dos campos (como aparecem na ART)
2. Padrões adotados
3. Responsáveis técnicos cadastrados
4. Catálogo de atividades já usadas
5. Mapa estudo → atividades
6. Pendências

## 1. Ordem dos campos

**Tipo**: ART OBRA / SERVIÇO — INICIAL.

**1. Responsável Técnico** — vem do cadastro do profissional logado. Pode haver mais
de um título profissional (ex.: com e sem especialização); escolher conforme o estudo.

**2. Dados do Contrato**
- Contratante (razão social), CPF/CNPJ
- Endereço do contratante: logradouro, nº, complemento, bairro, cidade, UF, CEP
  (endereço do CNPJ exato informado: matriz ou filial)
- Contrato (nº) — padrão "Não especificado"; Celebrado em — em branco
- Valor (R$)
- Tipo de Contratante — "Pessoa Jurídica de Direito Privado" (PF/PJ público se for o caso)
- Ação Institucional — "NENHUMA - NÃO OPTANTE"

**3. Dados da Obra/Serviço**
- Logradouro, nº (pode ser "S/N" ou "QUADRA 09"), complemento (ex.: "LOTE 08"), bairro
  ("ZONA RURAL" para áreas rurais), cidade, UF, CEP (CEP geral do município quando não
  há CEP de logradouro)
- Data de Início; Previsão de término
- Coordenadas Geográficas — "lat, lon" em graus decimais, 6 casas (ex.: -4.000000, -39.000000)
- Finalidade — "Ambiental" nos estudos ambientais
- Código — "Não Especificado"
- Proprietário + CPF/CNPJ — nas três amostras, igual ao contratante

**4. Atividade Técnica** — cada linha: nível de atuação > atividade > grupo > subgrupo > obra/serviço,
quantidade 1,00, unidade "un".

**5. Observações** — texto livre e curto, ex.:
- "Elaboração de planta georreferenciada, estudos ambientais e técnicos."
- "Elaboração de estudos ambientais, mapas, memorial descritivo e planta georreferenciada."

**6. Declarações** — acessibilidade (ABNT / Decreto 5.296/2004), marcada nas amostras.

**7. Entidade de Classe** — "NENHUMA - NÃO OPTANTE".

**10. Valor da ART** — calculado pelo sistema (valor fixo da faixa de contrato até R$ 2.000). Pagamento por boleto: sempre feito pelo profissional.

## 2. Padrões adotados (pré-preencher e relatar no fim)

| Campo | Padrão |
|---|---|
| Tipo de ART | Obra/Serviço — Inicial |
| Contrato nº / data | Não especificado / em branco |
| Valor do contrato | R$ 1.000,00 se não informado (já houve R$ 2.000) — relatar |
| Tipo de contratante | PJ de Direito Privado |
| Ação institucional | Nenhuma — não optante |
| Finalidade | Ambiental |
| Código | Não especificado |
| Proprietário | = contratante, salvo se o documento indicar outro — relatar |
| Nível de atuação | 14 - Elaboração |
| Quantidade / unidade | 1,00 / un |
| Datas | Início = data do preenchimento; término = início + 6 meses, se não informado — relatar |
| Entidade de classe | Nenhuma — não optante |
| Declaração de acessibilidade | Marcada |

## 3. Responsável técnico

O profissional responsável já está logado no portal. A skill identifica o nome na tela
e escolhe o título profissional conforme o cadastro dele. Nenhum dado pessoal de
profissional (nome, RNP, número de registro) é guardado neste repositório.

Critério provisório para o título: usar o título com especialização em
georreferenciamento quando a ART tiver #34.5.4 ou planta georreferenciada; senão,
o título simples. A escolha é sempre relatada no fim.

## 4. Catálogo de atividades já usadas (todas com "14 - Elaboração")

Prefixo A = "40 - Estudo"; prefixo B = "79 - Produção técnica e especializada".

| Código | Caminho | Usado com |
|---|---|---|
| #7.6.6 | MEIO AMBIENTE > GESTÃO AMBIENTAL > DE ESTUDOS AMBIENTAIS | A |
| #7.6.13 | MEIO AMBIENTE > GESTÃO AMBIENTAL > DE ESTUDO DE IMPACTO AMBIENTAL - EIA | A |
| #7.6.14 | MEIO AMBIENTE > GESTÃO AMBIENTAL > DE RELATÓRIO DE IMPACTO AMBIENTAL - RIMA | A |
| #7.1.2 | MEIO AMBIENTE > CONTROLE E MONITORAMENTO AMBIENTAL > DE MONITORAMENTO AMBIENTAL | A |
| #7.2.1.1 | MEIO AMBIENTE > DIAGNÓSTICO E CARACTERIZAÇÃO AMBIENTAL > DE DIAGNÓSTICO E CARACTERIZAÇÃO AMBIENTAL > CARACTERIZAÇÃO DO MEIO FÍSICO | A |
| #7.2.1.2 | … > CARACTERIZAÇÃO DO MEIO BIÓTICO | A |
| #7.2.1.4 | … > CARACTERIZAÇÃO DO MEIO ANTRÓPICO | A |
| #7.2.1.6 | … > DIAGNÓSTICO AMBIENTAL | A |
| #7.2.1.7 | … > PROGNÓSTICO AMBIENTAL | A |
| #7.2.1.9 | … > IDENTIFICAÇÃO E POTENCIALIZAÇÃO DE IMPACTOS AMBIENTAIS | A |
| #34.5.4 | GEODÉSIA > GEOPROCESSAMENTO > DE MAPEAMENTO TEMÁTICO | A (maioria) e B |

Não invente códigos fora desta tabela (ex.: #7.2.1.3, #7.2.1.5, #7.2.1.8 existem na
sequência, mas os nomes não foram confirmados). Se o estudo pedir algo que não está
aqui, descreva a atividade e marque "[A LOCALIZAR NA ÁRVORE DO PORTAL]".

## 5. Mapa estudo → atividades (proposta a validar pelo profissional)

| Estudo informado | Atividades |
|---|---|
| Qualquer estudo com planta georreferenciada, mapas ou memorial | #34.5.4 |
| Estudo ambiental "genérico" / simplificado | #7.6.6 + #7.2.1.6 + #7.2.1.7 |
| Estudo com caracterização dos meios (físico, biótico, antrópico) | + #7.2.1.1, #7.2.1.2, #7.2.1.4 conforme os meios efetivamente estudados |
| Avaliação / identificação de impactos | + #7.2.1.9 |
| EIA/RIMA | #7.6.13 + #7.6.14 + diagnóstico dos meios + #7.2.1.6 + #7.2.1.7 (e #34.5.4 se houver mapas) |
| Monitoramento ambiental / programas de monitoramento | #7.1.2 |

Inclua só o que o escopo de fato prevê: atividade anotada sem execução também é problema.

## 6. Pendências [A MAPEAR]
- Árvore completa de atividades do portal (para ampliar o catálogo).
- Rótulos e ordem exata dos campos na tela (o PDF mostra o resultado, não a tela).
- Se o portal permite escolher o título profissional e como.
- #34.5.4: usar "40 - Estudo" por padrão (maioria das amostras); confirmar com o profissional.
