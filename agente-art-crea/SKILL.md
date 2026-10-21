---
name: "art-crea"
description: Preenche ARTs (Anotação de Responsabilidade Técnica) direto nos portais dos CREAs pelo navegador (Claude in Chrome), começando pelo CREA-CE (sistema SITAC). A partir do CNPJ do contratante, endereço da obra/serviço, estudo ou termo de referência e KML/KMZ do empreendimento, seleciona as atividades técnicas, calcula as coordenadas e preenche o formulário inteiro, parando antes de finalizar o cadastro. Use SEMPRE que o usuário falar em ART, anotação de responsabilidade técnica, CREA, SITAC, "emitir/preencher/registrar ART", "quais atividades colocar na ART" ou mandar um KML pedindo coordenadas para ART, mesmo sem dizer "skill".
---

# ART nos CREAs — preenchimento direto

Modo de trabalho:
- Ir direto ao site e preencher tudo. Sem ficha prévia, sem quadro, sem pedir
  autorização campo a campo: a ativação da skill já é a autorização para preencher.
- NUNCA finalizar: não clicar em salvar definitivo / cadastrar / emitir / gerar boleto.
  O profissional confere e finaliza.
- O profissional responsável já está logado. Não perguntar o nome: ler da tela quem é.
- Perguntar só se for impossível seguir (ex.: falta o KML e o endereço não permite
  localizar, ou a pessoa não está logada). Todo o resto: aplicar padrão e relatar no fim.

## Qual CREA
A ART é do CREA da UF da obra/serviço. Referências:
- CE → `references/crea-ce.md` (ler antes de começar: padrões, catálogo de atividades,
  mapa estudo → atividades, responsáveis)
UF sem referência: avisar que ainda não foi mapeada e propor mapear (fim do arquivo).

## Passo 1 — Preparar os dados (sem mostrar ao usuário)
1. Contratante: usar o cartão CNPJ se enviado; senão buscar razão social e endereço do
   CNPJ exato (matriz/filial) na web.
2. Coordenada: `python3 scripts/kml_ponto.py <arquivo.kml|kmz> --uf CE`. Se avisar que o
   ponto está fora da UF, pare e avise (CREA errado provável) — é o único aviso que
   interrompe.
3. Atividades: se vier documento (TR, proposta, estudo), ler inteiro, listar o que ele
   exige e mapear pelo catálogo da referência, guardando o item/página que justifica
   cada atividade. Sem documento, usar o escopo descrito. Não inventar códigos: o que
   não estiver no catálogo, procurar na árvore do portal durante o preenchimento; se
   não achar com segurança, deixar de fora e relatar.
4. Valores ausentes: aplicar os padrões da referência (valor, prazo, proprietário etc.).

## Passo 2 — Preencher no site
1. Ver a aba atual (tabs_context) e confirmar que o portal está logado; ler o nome do
   profissional na tela. Escolher o título profissional pelo critério da referência.
2. Abrir nova ART de Obra/Serviço (inicial) e preencher seção a seção, na ordem da tela.
   Ler a página antes de cada seção; usar preenchimento em lote quando possível
   (browser_batch / form_input) para ganhar tempo.
3. Se um campo não existir ou uma opção não bater com o padrão, escolher a opção mais
   próxima e anotar para o relatório final.
4. Ao terminar a última seção, parar na tela anterior à finalização.

## Passo 3 — Relatório final (curto)
Em poucas linhas:
- "Preenchido, falta só você conferir e finalizar."
- Atividades lançadas, cada uma com o trecho do documento que a justifica (item/página).
- O que foi assumido por padrão (valor, prazo, proprietário, título, coordenada e de qual
  polígono veio).
- O que ficou de fora ou precisa de atenção (atividade não encontrada, parte que parece
  de outro profissional da equipe — cada ART cobre só a participação de quem a emite).
- Se algo novo foi aprendido sobre o portal, atualizar a referência da UF no próximo
  ajuste da skill (mencionar em uma linha).

## Mapear um CREA novo
Pedir 2–3 ARTs emitidas naquele CREA e uma sessão no portal (logado) para ler campos e
árvore de atividades sem salvar nada. Criar `references/crea-<uf>.md` com a mesma
estrutura de `crea-ce.md`.
