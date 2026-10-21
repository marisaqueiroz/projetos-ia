# Modo B — referência detalhada

## Sumário
1. Lendo medidas e confrontações
2. Referencial s/t
3. Formato do config.json
4. Fator de escala UTM: área plana x elipsoidal
5. Armadilhas conhecidas
6. Exemplo completo (caso fictício: Loteamento Exemplo, Município Exemplo/CE)

---

## 1. Lendo medidas e confrontações

Formato típico de uma matrícula urbana:

> Ao LESTE, frente, medindo 15,00m, com a Avenida A; Ao OESTE, fundos, medindo 15,00m, com parte do lote 18; Ao NORTE, lado esquerdo, medindo 27,40m, com o lote 21; Ao SUL, lado direito, medindo 27,40m, com o lote 19; área total de 411,00m².

Convenções:
- "Lado esquerdo" e "lado direito" são vistos de quem está na rua, olhando para o lote.
- Os pontos cardeais descrevem a posição relativa dentro da quadra. Na prática, eles correspondem aos lados da quadra, e não ao norte verdadeiro. Ex.: "LESTE" = o lado da quadra voltado para a Av. A, que pode ter azimute 17° em vez de 0°.
- "Com parte do lote X" indica que o lado confronta só um trecho do vizinho. Isso ajuda a montar o arranjo (ex.: o lote 18 tem 30 m de lado leste, encostado nos fundos do 19 e do 20, que têm 15 m cada).
- Rua citada como confrontante → aquele lado está no alinhamento da quadra.

Monte uma tabela de lotes × lados × confrontantes e verifique se todas as relações de vizinhança fecham antes de desenhar.

## 2. Referencial s/t

O script não usa Norte/Leste diretamente. Ele usa:
- **origem**: um canto da quadra (ou um ponto conhecido);
- **eixo s**: direção ao longo de uma rua (definida por um ponto de direção ou um azimute);
- **eixo t**: direção ao longo da outra rua.

Um ponto do lote é `origem + k·(s·û_s + t·û_t)`. Com `geometria: "paralela"`, os eixos seguem exatamente as ruas (podem formar 89,5°, 91°, etc.). Com `"retangular"`, t é forçado a ficar perpendicular a s.

Para escolher os pontos de direção, use a saída de `inspecionar`: se a origem é o vértice v2, os pontos de direção são v1 e v3 (os vizinhos de v2).

Modo local (sem `origem`): s = Leste, t = Norte, origem em (0,0) e sem `.prj`.

## 3. Formato do config.json

```json
{
  "saida": "/mnt/user-data/outputs/Lotes_17_a_20_Qd15",
  "titulo": "Lotes 17 a 20 / Qd 15 – Loteamento Exemplo",
  "epsg": 31984,
  "prj_de": "/mnt/user-data/uploads/QUADRAS.prj",
  "quadra_shp": "/mnt/user-data/uploads/QUADRAS.shp",
  "quadra_indice": 2,
  "origem": [500365.855, 9600227.962],
  "eixo_s_para": [500231.257, 9600271.291],
  "eixo_t_para": [500383.172, 9600283.547],
  "geometria": "paralela",
  "escala": "terreno",
  "comum": {"quadra": "15", "lotea": "Loteamento Exemplo", "municipio": "Município Exemplo",
            "uf": "CE", "proprietar": "Proprietário Exemplo",
            "cartorio": "Cartório Exemplo"},
  "lotes": [
    {"lote": "17", "matricula": "1001", "insc_pmp": "9001", "area_mat": 360, "frente": "Rua 13", "s": [39.4, 51.4], "t": [0, 30]},
    {"lote": "18", "matricula": "1002", "insc_pmp": "9002", "area_mat": 360, "frente": "Rua 13", "s": [27.4, 39.4], "t": [0, 30]},
    {"lote": "19", "matricula": "1003", "insc_pmp": "9003", "area_mat": 411, "frente": "Av. A",  "s": [0, 27.4],    "t": [0, 15]},
    {"lote": "20", "matricula": "1004", "insc_pmp": "9004", "area_mat": 411, "frente": "Av. A",  "s": [0, 27.4],    "t": [15, 30]}
  ]
}
```

Campos opcionais: `azimute_s` / `azimute_t` (em vez de `eixo_*_para`), `quadra_shp`, `prj_de`, `titulo`. Os campos de `comum` valem para todos os lotes, e um campo definido dentro do lote prevalece sobre o de `comum`. Lote irregular: `"vertices_st": [[s,t], ...]` em ordem.

Saídas: `<saida>_shapefile.zip` (camadas `_lotes` e `_vertices`), `<saida>.dxf` e `<saida>_previa.png`.

## 4. Fator de escala UTM: área plana x elipsoidal

A projeção UTM distorce as distâncias pelo fator de escala `k`. O valor é 0,9996 no meridiano central e cresce à medida que o ponto se afasta dele (a ~16 km a oeste do meridiano central de −39°, k ≈ 0,999603). Consequências:
- A distância real (no terreno ou no elipsoide) é igual à distância UTM dividida por k.
- A área real é igual à área UTM dividida por k² (+0,08% nessa distância; 411 m² → ~411,3 m²).

O QGIS, por padrão, mede áreas sobre o elipsoide. Se as medidas da matrícula forem aplicadas direto no plano UTM (`escala: "plano"`), o usuário verá no QGIS ~0,3 m² a mais por lote de 400 m². Foi exatamente o que aconteceu no caso original: o usuário mediu 411,301 e 411,309 m² onde a matrícula dizia 411,00 m².

Recomendação: use `escala: "terreno"`, porque as medidas da matrícula são medidas de campo e as normas de georreferenciamento (SIGEF, NBR 14166) trabalham com distâncias e áreas reais. A exceção é quando a quadra de referência foi claramente vetorizada com medidas planas em CAD e o usuário quer coerência com ela; nesse caso use `"plano"` e ensine a configurar o QGIS em *Projeto > Propriedades > Geral > Elipsoide: Nenhum/Planimétrico*.

Em qualquer caso, informe as duas áreas (plana e elipsoidal). O script já as calcula.

## 5. Armadilhas conhecidas

- **Coordenada atribuída ao canto errado**: compare sempre a coordenada informada com os vértices da quadra (distância < ~0,5 m indica que é o canto da quadra). Prefira o croqui e explique.
- **Lote vizinho com medida desconhecida**: se a posição do lote depende de um vizinho sem matrícula (ex.: o lote 19 entre o canto e o 20), estime a medida pelo croqui (proporção em pixels) e declare a suposição. Peça a matrícula do vizinho, se possível.
- **Canto da quadra fora do esquadro**: use `paralela` e explique que a área varia em centésimos de m².
- **Croqui por imagem**: para extrair proporções, meça em pixels a largura dos lotes e o comprimento dos lados da quadra. Confira se a razão bate com as medidas da matrícula. Se bater, a interpretação está certa.
- **Lote fora da quadra ou sobreposição**: o script avisa (`dentro False` / `SOBREPOSICAO DETECTADA`). Revise os intervalos s/t.
- **Profundidade total**: a soma das profundidades dos lotes ao longo de um eixo não pode passar do lado da quadra.

## 6. Exemplo completo (caso fictício: Loteamento Exemplo, Município Exemplo/CE)

Entradas: matrículas 1001 (lote 17), 1002 (lote 18), 1003 (lote 19) e 1004 (lote 20) da quadra 15; shapefile QUADRAS (3 feições, SIRGAS2000 UTM 24S); print do QGIS com o croqui; coordenada E 500365,88 / N 9600228,00.

Raciocínio:
1. Lote 20: 15 × 27,40 = 411 → retângulo. Frente leste na Av. A, fundos na parte do lote 18, norte no 21, sul no 19.
2. Lote 19: idem, mas o sul é a Rua 13 → ocupa o canto SE da quadra.
3. Lote 18: 12 × 30, frente na Rua 13, lado leste nos fundos do 19 e do 20 (30 = 15 + 15). Lote 17: 12 × 30, a oeste do 18.
4. `inspecionar` mostrou que a coordenada coincidia com o vértice v2 da feição 2 (canto SE da quadra), e não com o "V3 do lote 20" que o usuário tinha indicado.
5. Origem = v2; eixo s → v3 (Rua 13, az 287,84°); eixo t → v1 (Av. A, az 17,30°); ângulo entre eixos de 89,46° → `paralela`.
6. Resultado: 4 lotes dentro da quadra, sem sobreposição, 10 vértices compartilhados e medidas lineares exatas.
