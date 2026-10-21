---
name: matricula-para-shapefile
description: "Gera shapefile (polígono + vértices), DXF e prévia a partir de matrículas de imóveis brasileiras, em dois modos: (A) memorial descritivo georreferenciado, com coordenadas/azimutes/distâncias; (B) matrícula só com MEDIDAS E CONFRONTAÇÕES (ex.: \"Ao LESTE, frente, medindo 15,00m com a Avenida A...\"), desenhando os lotes e alocando-os dentro de uma quadra, gleba ou área de referência (shapefile de quadras, croqui/print do QGIS, coordenada de um canto ou azimute). Use sempre que o usuário enviar PDF de matrícula, certidão de registro de imóveis ou memorial e pedir shapefile, poligonal, área do imóvel, \"desenhar o lote\", \"colocar o lote na quadra\", \"alocar os lotes\", \"encaixar no polígono\", georreferenciar ou converter matrícula em .shp/.dxf, mesmo sem dizer \"shapefile\". Também acionar para validar área/perímetro de matrícula contra a poligonal, ou para explicar diferenças de área entre o desenho e o QGIS (fator de escala UTM, área plana x elipsoidal). Não usar para gerar apenas KML/KMZ sem relação com matrícula.\n"
---

# Matrícula para Shapefile

Converte a descrição do imóvel em uma matrícula de registro de imóveis brasileira em arquivos GIS/CAD prontos para QGIS, ArcGIS e AutoCAD, com validação de área e perímetro contra os valores declarados.

## Escolha do modo

Leia a matrícula (skill `pdf-reading` se o conteúdo não estiver no contexto) e decida:

- **Modo A — memorial georreferenciado**: a descrição traz vértices com coordenadas (E/N), datum e projeção. Siga a seção "Modo A".
- **Modo B — medidas e confrontações**: a descrição traz apenas lados ("Ao LESTE, frente, medindo 15,00m, com a Avenida A..."), área e confrontantes, sem coordenadas. Típico de lotes urbanos de loteamento. Siga a seção "Modo B" e leia `references/modo_medidas.md`.

Se houver as duas coisas, prefira o Modo A.

---

## Modo A — memorial georreferenciado

### A1. Extrair os dados

- **Vértices**: código de cada vértice (ex.: "EGH P C317"), coordenadas Norte e Este.
- **Sistema de referência** → EPSG: SIRGAS2000 UTM 23S → 31983; SIRGAS2000 UTM 24S → 31984; SAD-69 UTM 24S → 29194 (conferir caso a caso).
- **Área e perímetro declarados**, para validação.
- **Metadados**: matrícula, nome do imóvel, município/UF, proprietário atual (usar o registro R- mais recente; desconsiderar registros superados), código INCRA/CCIR, cartório, data da matrícula.

**Erros de digitação do cartório**: é comum um dígito extra ou trocado no fechamento (o último vértice deve coincidir com o primeiro). Se a diferença for um dígito óbvio (ex.: "96719443,53" vs "9671943,53"), use o valor do vértice inicial e avise o usuário. Inconsistências mais sérias (poligonal que não fecha, coordenadas fora da faixa plausível do município) devem ser sinalizadas antes de prosseguir.

### A2. Gerar

Use `scripts/gerar_shapefile.py` (requer `geopandas`, `shapely`, `fiona`). Preencha VERTICES e METADADOS e execute. O script monta o polígono nas coordenadas originais (sem reprojetar), gera polígono e vértices, grava o `.prj` e compara área/perímetro com os declarados.

### A3. Validar

Reporte sempre calculado x declarado. Até ~0,5% é normal; acima disso, revise a transcrição dos vértices.

---

## Modo B — lotes só com medidas e confrontações

O objetivo é desenhar o(s) lote(s) com as medidas exatas da matrícula e posicioná-los corretamente dentro de uma área de referência. Detalhes, armadilhas e o formato do arquivo de configuração estão em `references/modo_medidas.md` — leia antes de começar.

### B1. Extrair e conferir as medidas

Para cada matrícula: lote, quadra, loteamento, inscrição municipal, cada lado (orientação cardeal, se é frente/fundos/lateral, medida, confrontante), área declarada e proprietário atual (R- mais recente).

Confira antes de desenhar:
- **Forma**: "forma regular" com frente × lateral = área → retângulo. Se não fechar, o lote é irregular; sinalize.
- **Coerência entre matrículas vizinhas**: os confrontantes têm que se encaixar. Ex.: lote 18 com lado leste de 30 m "com os fundos dos lotes 19 e 20", e os lotes 19 e 20 com 15 m de fundos cada (15 + 15 = 30). Use essas relações para montar o arranjo e aponte qualquer conflito.

### B2. Entregar o desenho local primeiro (se não houver referência)

Sem nenhum dado de posição, gere o lote em coordenadas locais (origem no canto SO, X = Leste, Y = Norte), em DXF e shapefile sem `.prj`. Deixe claro que ele não está georreferenciado e peça o que falta para posicioná-lo.

### B3. Obter a referência de posição

Aceite qualquer combinação destas fontes, da mais à menos confiável:
1. **Shapefile/DXF da quadra ou gleba** (melhor: dá os cantos e o rumo das ruas).
2. **Croqui ou print** (QGIS, Google Earth, planta) mostrando onde ficam os lotes dentro da quadra.
3. **Coordenada de um canto** + qual canto é + azimute da frente (ou um segundo ponto).

Se o usuário der só uma coordenada sem dizer de qual canto é, pergunte (use `ask_user_input_v0` com os cantos do lote como opções).

**Sempre confronte a coordenada informada com os vértices da quadra.** No caso real que originou este modo, o usuário disse que o ponto era o canto SO do lote 20, mas ele coincidia (4,5 cm) com o canto SE da quadra, que pelo croqui era o canto SE do lote 19. A posição certa era a do croqui. Quando houver conflito, siga a geometria (quadra + croqui), explique a correção ao usuário e destaque-a na resposta.

### B4. Montar o referencial e posicionar os lotes

1. Inspecione a quadra: `python3 scripts/alocar_lotes.py inspecionar QUADRAS.shp` (lista vértices, lados, azimutes e ângulos internos). Identifique a feição certa (aquela cujo canto coincide com a coordenada informada ou que corresponde ao croqui).
2. Escolha a **origem** (o canto da quadra do qual os lotes partem) e os **dois eixos**: `s` ao longo de uma rua e `t` ao longo da outra, usando os vértices vizinhos da quadra como pontos de direção. A orientação das ruas vem do shapefile, não dos pontos cardeais da matrícula: "Leste" e "Sul" na matrícula são nominais e quase nunca coincidem com o norte verdadeiro.
3. Escreva cada lote como intervalos `s` e `t` em metros a partir da origem, acumulando as medidas pelos confrontantes (ex.: lote 19 em s 0–27,4 / t 0–15; lote 20 em s 0–27,4 / t 15–30; lote 18 em s 27,4–39,4 / t 0–30). Para lotes irregulares, use `vertices_st`.
4. Crie o `config.json` (modelo em `references/modo_medidas.md`) e rode `python3 scripts/alocar_lotes.py gerar config.json`.

### B5. Decisões que precisam ser explícitas

- **Geometria** (`geometria`):
  - `paralela` (padrão): os lados acompanham as duas ruas. Use quando o canto da quadra não for 90° exatos. As medidas lineares batem e a área varia pelo seno do ângulo (desprezível, centésimos de m²).
  - `retangular`: força 90°. O lote fica perfeitamente retangular, mas se afasta de uma das ruas (ex.: ~0,26 m em 27,4 m para um canto de 89,46°).
- **Escala** (`escala`) — leia a seção correspondente em `references/modo_medidas.md`:
  - `terreno` (recomendado): as medidas da matrícula são medidas reais. O script aplica o fator de escala UTM `k`, e a área elipsoidal (a que o QGIS mostra por padrão) bate com a matrícula.
  - `plano`: as medidas são aplicadas direto no plano UTM. A área plana bate com a matrícula, mas o QGIS (elipsoidal) mostra ~0,08% a mais, perto do meridiano central da zona 24S.

  Se o usuário não disser, use `terreno` e informe. Se ele reclamar de diferença de área depois, a explicação é essa (ver referência).

### B6. Validar e entregar

O script reporta, por lote: área plana, área elipsoidal, área da matrícula, perímetro, medida real de cada lado e azimute, se o lote está dentro da quadra e se há sobreposição entre lotes. Confira tudo isso e veja a prévia PNG (`view`) para comparar com o croqui antes de entregar.

---

## Entrega (ambos os modos)

- Shapefile compactado em `.zip` (polígono + vértices, `.prj` e `.cpg`). No Modo B, copie o `.prj` do shapefile de quadras do usuário quando houver (`prj_de`).
- DXF com camadas separadas (QUADRA, LOTES, VERTICES, TEXTO) no Modo B.
- PNG de prévia para conferência rápida.
- Salvar em `/mnt/user-data/outputs/` e usar `present_files`.
- Na resposta, traga uma tabela de vértices (E/N, com os cantos de cada lote que compartilham o ponto), a comparação de áreas e todas as suposições feitas (canto de partida, medida de lote vizinho assumida, geometria, escala).
- KML, se pedido: reprojete para EPSG:4326 a partir do EPSG de origem.

## Atributos padrão

**Modo A — polígono**: matricula, nome, municipio, uf, area_ha, perim_m, cod_incra, proprietar, cartorio, matr_data.
**Modo B — lotes**: matricula, lote, quadra, insc_pmp, lotea, municipio, uf, frente, proprietar, cartorio, area_mat, area_plan, area_elip, perim_m.
**Vértices**: vertice, (matricula | cantos), este, norte.

Ajuste conforme o pedido, mantendo esse conjunto como mínimo.
