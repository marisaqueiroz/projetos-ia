"""
Gera shapefile (poligono + vertices) a partir dos vertices extraidos
de uma matricula de imovel (memorial descritivo).

Uso: edite as secoes VERTICES e METADADOS abaixo com os dados extraidos
do PDF da matricula, ajuste o EPSG_ORIGEM, e execute:

    pip install geopandas shapely fiona --break-system-packages
    python3 gerar_shapefile.py

Gera:
    <saida>_poligono.shp/.shx/.dbf/.prj/.cpg
    <saida>_vertices.shp/.shx/.dbf/.prj/.cpg

E imprime a comparacao entre area/perimetro calculados e declarados.
"""

import geopandas as gpd
from shapely.geometry import Polygon, Point

# ---------------------------------------------------------------------------
# EDITE AQUI: dados extraidos do PDF da matricula (valores abaixo sao FICTICIOS)
# ---------------------------------------------------------------------------

# EPSG de origem, conforme o datum/projecao/meridiano declarados na matricula:
#   SIRGAS2000 UTM 23S -> 31983
#   SIRGAS2000 UTM 24S -> 31984
#   SAD-69     UTM 24S -> conferir codigo especifico
EPSG_ORIGEM = "EPSG:31984"

# Lista de vertices na ordem em que aparecem no memorial descritivo.
# (nome_do_vertice, coordenada_Este, coordenada_Norte)
# NAO repita o vertice inicial no final -- o script fecha o poligono automaticamente.
VERTICES = [
    ("V01", 500120.40, 9600850.10),
    ("V02", 500310.75, 9600842.30),
    ("V03", 500325.10, 9600610.55),
    ("V04", 500298.60, 9600405.20),
    ("V05", 500142.35, 9600398.80),
    ("V06", 500110.90, 9600620.45),
]

# Valores DECLARADOS na matricula, para validacao (em ha e metros)
AREA_DECLARADA_HA = 8.6190
PERIMETRO_DECLARADO_M = 1239.90

# Metadados a incluir nos atributos do shapefile de poligono
METADADOS = {
    "matricula": "0001",
    "nome": "Sitio Exemplo",
    "municipio": "Municipio Exemplo",
    "uf": "CE",
    "area_ha": AREA_DECLARADA_HA,
    "perim_m": PERIMETRO_DECLARADO_M,
    "cod_incra": "0000000000000",
    "proprietar": "Proprietario Exemplo",
    "cartorio": "Cartorio Exemplo",
    "matr_data": "01/01/2020",
}

# Prefixo dos arquivos de saida
SAIDA = "Matricula_Exemplo"

# ---------------------------------------------------------------------------
# Nao precisa editar daqui para baixo
# ---------------------------------------------------------------------------

def main():
    coords = [(e, n) for _, e, n in VERTICES]
    poly = Polygon(coords)

    gdf_poly = gpd.GeoDataFrame(
        {k: [v] for k, v in METADADOS.items()},
        geometry=[poly],
        crs=EPSG_ORIGEM,
    )
    gdf_poly.to_file(f"{SAIDA}_poligono.shp", driver="ESRI Shapefile", encoding="utf-8")

    gdf_pts = gpd.GeoDataFrame(
        {
            "vertice": [nome for nome, _, _ in VERTICES],
            "matricula": [METADADOS.get("matricula", "")] * len(VERTICES),
            "norte": [n for _, _, n in VERTICES],
            "este": [e for _, e, _ in VERTICES],
        },
        geometry=[Point(e, n) for _, e, n in VERTICES],
        crs=EPSG_ORIGEM,
    )
    gdf_pts.to_file(f"{SAIDA}_vertices.shp", driver="ESRI Shapefile", encoding="utf-8")

    area_calc_ha = gdf_poly.geometry.area.iloc[0] / 10000
    perim_calc_m = gdf_poly.geometry.length.iloc[0]

    print(f"Area calculada:      {area_calc_ha:.4f} ha")
    print(f"Area declarada:      {AREA_DECLARADA_HA:.4f} ha")
    print(f"Diferenca:           {abs(area_calc_ha - AREA_DECLARADA_HA):.4f} ha "
          f"({abs(area_calc_ha - AREA_DECLARADA_HA) / AREA_DECLARADA_HA * 100:.3f}%)")
    print()
    print(f"Perimetro calculado: {perim_calc_m:.2f} m")
    print(f"Perimetro declarado: {PERIMETRO_DECLARADO_M:.2f} m")
    print(f"Diferenca:           {abs(perim_calc_m - PERIMETRO_DECLARADO_M):.2f} m "
          f"({abs(perim_calc_m - PERIMETRO_DECLARADO_M) / PERIMETRO_DECLARADO_M * 100:.3f}%)")
    print()
    print("Se a diferenca percentual for > ~0.5%, revise os vertices extraidos do memorial.")


if __name__ == "__main__":
    main()
