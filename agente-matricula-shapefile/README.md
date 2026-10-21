# Agente de matrícula para shapefile

Skill de IA que converte matrículas e memoriais descritivos de imóveis brasileiros em arquivos GIS e CAD (shapefile, DXF e prévia em PNG), com validação de área e perímetro. **Economia de cerca de 1 dia de trabalho por matrícula extensa.**

## Problema

As matrículas costumam ser extensas e trazer todo o histórico do imóvel. Anteriormente, o processo exigia leitura, interpretação, extração dos dados, plotagem em planilha e importação para o software de GIS.

## Dois modos de trabalho

- **Modo A: memorial georreferenciado.** A descrição traz vértices com coordenadas, datum e projeção. O agente extrai os vértices, identifica o EPSG e gera polígono e vértices (`scripts/gerar_shapefile.py`).
- **Modo B: medidas e confrontações.** A descrição traz apenas os lados ("Ao LESTE, frente, medindo 15,00 m, com a Avenida A..."). O agente desenha os lotes com as medidas exatas e os aloca dentro de uma quadra de referência (`scripts/alocar_lotes.py`).

## Validação

- Comparação entre área e perímetro calculados e os declarados na matrícula (diferença de até cerca de 0,5% é esperada; acima disso, os vértices são revisados).
- Detecção de erros de digitação do cartório no fechamento da poligonal.
- No Modo B: conferência da coerência entre matrículas vizinhas, verificação de lotes dentro da quadra, ausência de sobreposição e comparação da coordenada informada com os vértices da quadra.
- Explicação da diferença entre área plana e área elipsoidal (fator de escala UTM), que costuma causar divergência entre o desenho e o QGIS.

## Arquivos

| Arquivo | Função |
|---|---|
| `SKILL.md` | Fluxo de trabalho do agente |
| `references/modo_medidas.md` | Detalhes do Modo B: referencial, configuração, escala UTM e armadilhas |
| `scripts/gerar_shapefile.py` | Geração de shapefile no Modo A |
| `scripts/alocar_lotes.py` | Desenho e alocação de lotes no Modo B |

## Execução dos scripts

```bash
pip install geopandas shapely fiona pyshp ezdxf pyproj matplotlib
python3 scripts/gerar_shapefile.py           # Modo A (editar vértices e metadados no início do arquivo)
python3 scripts/alocar_lotes.py inspecionar QUADRAS.shp
python3 scripts/alocar_lotes.py gerar config.json
```

Os exemplos incluídos usam **dados fictícios**. Nenhuma matrícula, proprietário ou coordenada real é publicada neste repositório.
