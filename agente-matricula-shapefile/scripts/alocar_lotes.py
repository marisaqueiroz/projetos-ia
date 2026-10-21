"""
Desenha lotes a partir das MEDIDAS E CONFRONTACOES da matricula (sem coordenadas)
e os aloca dentro de uma quadra/area de referencia em UTM.

Dependencias:
    pip install pyshp shapely ezdxf pyproj matplotlib --break-system-packages

Dois subcomandos:

  1) Inspecionar a quadra de referencia (vertices, lados, azimutes, angulos):
       python3 alocar_lotes.py inspecionar QUADRAS.shp

  2) Gerar os lotes a partir de um arquivo de configuracao JSON:
       python3 alocar_lotes.py gerar config.json

Modelo do config.json (ver references/modo_medidas.md para detalhes):

{
  "saida": "/mnt/user-data/outputs/Lotes_17_a_20_Qd15",
  "epsg": 31984,
  "prj_de": "/mnt/user-data/uploads/QUADRAS.prj",        # opcional: copia o .prj
  "quadra_shp": "/mnt/user-data/uploads/QUADRAS.shp",    # opcional: desenho, checagem e DXF
  "quadra_indice": 2,                                     # opcional: indice da feicao (0-based)

  "origem": [500365.855, 9600227.962],   # canto de partida (ex.: canto da quadra)
  "eixo_s_para": [500231.257, 9600271.291],  # ponto que da a direcao do eixo s (rua 1)
  "eixo_t_para": [500383.172, 9600283.547],  # ponto que da a direcao do eixo t (rua 2)
  #  alternativa a eixo_*_para:  "azimute_s": 287.84, "azimute_t": 17.30
  #  sem nenhum dos dois: modo LOCAL (origem 0,0, s = Oeste->Leste, t = Sul->Norte)

  "geometria": "paralela",   # "paralela": lados paralelos as duas ruas (segue a quadra)
                             # "retangular": t forcado perpendicular a s (lotes 90 graus)
  "escala": "terreno",       # "terreno": distancias da matricula = medidas reais
                             #   (aplica fator de escala UTM k; QGIS elipsoidal mostra a area exata)
                             # "plano": distancias aplicadas direto no plano UTM

  "comum": {"quadra": "15", "lotea": "Loteamento Exemplo", "municipio": "Município Exemplo",
            "uf": "CE", "proprietar": "...", "cartorio": "..."},
  "lotes": [
    {"lote": "19", "matricula": "1003", "insc_pmp": "9003", "area_mat": 411.00,
     "frente": "Av. A", "s": [0, 27.4], "t": [0, 15]},
    {"lote": "X",  "matricula": "...", "area_mat": 300,
     "vertices_st": [[0,0],[20,0],[20,15],[0,14]]}       # lote irregular
  ]
}

Cada lote e definido em metros, no referencial da quadra:
  s = distancia ao longo do eixo s a partir da origem
  t = distancia ao longo do eixo t a partir da origem
"""

import json
import math
import os
import shutil
import sys
import zipfile

import shapefile
from shapely.geometry import Polygon
from shapely.ops import unary_union


# ---------------------------------------------------------------------------
# utilitarios
# ---------------------------------------------------------------------------

def azimute(p, q):
    return math.degrees(math.atan2(q[0] - p[0], q[1] - p[1])) % 360


def unit_from_az(az):
    r = math.radians(az)
    return (math.sin(r), math.cos(r))


def unit(p, q):
    d = math.dist(p, q)
    return ((q[0] - p[0]) / d, (q[1] - p[1]) / d)


def fator_escala(epsg, e, n):
    """Fator de escala combinado (ponto) da projecao no local."""
    from pyproj import Proj, Transformer
    lon, lat = Transformer.from_crs(epsg, 4674, always_xy=True).transform(e, n)
    return Proj(f"EPSG:{epsg}").get_factors(lon, lat).meridional_scale


def area_elipsoidal(epsg, pts):
    from pyproj import Geod, Transformer
    t = Transformer.from_crs(epsg, 4674, always_xy=True)
    ll = [t.transform(*p) for p in pts]
    a, _ = Geod(ellps="GRS80").polygon_area_perimeter(*zip(*ll))
    return abs(a)


# ---------------------------------------------------------------------------
# inspecionar
# ---------------------------------------------------------------------------

def inspecionar(path):
    r = shapefile.Reader(path)
    print("Campos:", [f[0] for f in r.fields[1:]])
    for i, (s, rec) in enumerate(zip(r.shapes(), r.records())):
        p = s.points
        if p[0] == p[-1]:
            p = p[:-1]
        print(f"\nFeicao indice {i}  atributos={list(rec)}  area={Polygon(p).area:.2f} m2")
        n = len(p)
        for k in range(n):
            a, b, prev = p[k], p[(k + 1) % n], p[k - 1]
            ang = (azimute(a, prev) - azimute(a, b)) % 360
            ang = min(ang, 360 - ang)
            print(f"  v{k}: E {a[0]:.3f} N {a[1]:.3f} | angulo interno ~{ang:.2f} | "
                  f"lado v{k}->v{(k+1)%n}: {math.dist(a, b):.2f} m, az {azimute(a, b):.2f}")


# ---------------------------------------------------------------------------
# gerar
# ---------------------------------------------------------------------------

def gerar(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    epsg = cfg.get("epsg")
    saida = cfg["saida"]
    comum = cfg.get("comum", {})
    local = "origem" not in cfg

    O = tuple(cfg.get("origem", (0.0, 0.0)))
    if "eixo_s_para" in cfg:
        us = unit(O, cfg["eixo_s_para"])
    elif "azimute_s" in cfg:
        us = unit_from_az(cfg["azimute_s"])
    else:
        us = (1.0, 0.0)
    if "eixo_t_para" in cfg:
        ut = unit(O, cfg["eixo_t_para"])
    elif "azimute_t" in cfg:
        ut = unit_from_az(cfg["azimute_t"])
    else:
        ut = (0.0, 1.0)

    if cfg.get("geometria", "paralela") == "retangular":
        # perpendicular a s, do mesmo lado em que estava t
        c1, c2 = (-us[1], us[0]), (us[1], -us[0])
        ut = c1 if c1[0] * ut[0] + c1[1] * ut[1] > 0 else c2

    k = 1.0
    if cfg.get("escala", "plano") == "terreno" and epsg and not local:
        k = fator_escala(epsg, *O)

    ang_st = math.degrees(math.acos(max(-1, min(1, us[0] * ut[0] + us[1] * ut[1]))))
    print(f"Eixo s az {azimute((0,0), us):.2f} | eixo t az {azimute((0,0), ut):.2f} | "
          f"angulo entre eixos {ang_st:.2f} | fator de escala aplicado k={k:.6f}")

    def P(s, t):
        return (round(O[0] + k * (s * us[0] + t * ut[0]), 3),
                round(O[1] + k * (s * us[1] + t * ut[1]), 3))

    # monta lotes
    lotes = []
    for L in cfg["lotes"]:
        if "vertices_st" in L:
            st = L["vertices_st"]
        else:
            (s0, s1), (t0, t1) = L["s"], L["t"]
            st = [(s0, t0), (s1, t0), (s1, t1), (s0, t1)]
        pts = [P(s, t) for s, t in st]
        poly = Polygon(pts)
        if not poly.exterior.is_ccw:
            pass
        ring = list(poly.exterior.coords)
        if poly.exterior.is_ccw:            # shapefile: anel externo horario
            ring = ring[::-1]
        lotes.append({**L, "pts": pts, "poly": poly, "ring": ring})

    # quadra de referencia
    quadra = None
    if cfg.get("quadra_shp"):
        qr = shapefile.Reader(cfg["quadra_shp"])
        quadras = [Polygon(s.points) for s in qr.shapes()]
        quadra = quadras[cfg.get("quadra_indice", 0)]

    # relatorio
    print()
    print(f"{'lote':>6} {'area plana':>11} {'area elips':>11} {'area mat':>9} {'perim':>8}  dentro")
    for L in lotes:
        ap = L["poly"].area
        ae = area_elipsoidal(epsg, L["pts"]) if epsg and not local else float("nan")
        L["area_plan"], L["area_elip"] = ap, ae
        dentro = quadra.buffer(0.01).contains(L["poly"]) if quadra else None
        print(f"{L['lote']:>6} {ap:11.3f} {ae:11.3f} {L.get('area_mat', float('nan')):9.2f} "
              f"{L['poly'].length:8.3f}  {dentro}")
        for a, b in zip(L["pts"], L["pts"][1:] + L["pts"][:1]):
            print(f"         lado {math.dist(a, b) / k:7.3f} m (medida real) az {azimute(a, b):7.2f}")
    soma = sum(L["poly"].area for L in lotes)
    uniao = unary_union([L["poly"] for L in lotes]).area
    print(f"\nSoma das areas {soma:.3f} | uniao {uniao:.3f} | "
          f"{'sem sobreposicao' if abs(soma - uniao) < 0.01 else 'SOBREPOSICAO DETECTADA'}")

    # vertices unicos
    uniq = {}
    for L in lotes:
        for i, p in enumerate(L["pts"]):
            uniq.setdefault(p, []).append(f"L{L['lote']}-v{i+1}")
    nomes = {p: f"P{i+1:02d}" for i, p in enumerate(sorted(uniq, key=lambda p: (-p[1], p[0])))}

    # ------------------------------------------------------------------ shp
    tmp = saida + "_shp_tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    base = os.path.basename(saida)
    campos = ["matricula", "lote", "quadra", "insc_pmp", "lotea", "municipio", "uf",
              "frente", "proprietar", "cartorio"]
    w = shapefile.Writer(f"{tmp}/{base}_lotes", shapeType=shapefile.POLYGON, encoding="utf-8")
    for c in campos:
        w.field(c, "C", 80)
    for c in ["area_mat", "area_plan", "area_elip", "perim_m"]:
        w.field(c, "N", 14, 3)
    for L in lotes:
        w.poly([L["ring"]])
        rec = [str(L.get(c, comum.get(c, ""))) for c in campos]
        rec += [L.get("area_mat", 0) or 0, round(L["area_plan"], 3),
                0 if math.isnan(L["area_elip"]) else round(L["area_elip"], 3),
                round(L["poly"].length, 3)]
        w.record(*rec)
    w.close()

    v = shapefile.Writer(f"{tmp}/{base}_vertices", shapeType=shapefile.POINT, encoding="utf-8")
    v.field("vertice", "C", 6); v.field("cantos", "C", 120)
    v.field("este", "N", 14, 3); v.field("norte", "N", 14, 3)
    for p, nm in sorted(nomes.items(), key=lambda x: x[1]):
        v.point(*p); v.record(nm, ", ".join(uniq[p]), p[0], p[1])
    v.close()

    prj = None
    if cfg.get("prj_de"):
        prj = open(cfg["prj_de"], encoding="utf-8").read()
    elif epsg and not local:
        from pyproj import CRS
        prj = CRS.from_epsg(epsg).to_wkt("WKT1_ESRI")
    for b in [f"{base}_lotes", f"{base}_vertices"]:
        if prj:
            open(f"{tmp}/{b}.prj", "w").write(prj)
        open(f"{tmp}/{b}.cpg", "w").write("UTF-8")
    with zipfile.ZipFile(f"{saida}_shapefile.zip", "w") as z:
        for f in sorted(os.listdir(tmp)):
            z.write(f"{tmp}/{f}", f)
    shutil.rmtree(tmp)

    # ------------------------------------------------------------------ dxf
    try:
        import ezdxf
        doc = ezdxf.new("R2010", setup=True)
        doc.units = ezdxf.units.M
        msp = doc.modelspace()
        for l, c in [("QUADRA", 3), ("LOTES", 1), ("TEXTO", 7), ("VERTICES", 4)]:
            doc.layers.add(l, color=c)
        if cfg.get("quadra_shp"):
            for s in shapefile.Reader(cfg["quadra_shp"]).shapes():
                msp.add_lwpolyline(s.points, close=True, dxfattribs={"layer": "QUADRA"})
        rot = -azimute((0, 0), us) + 90 + 180   # texto ao longo do eixo s
        rot = ((rot + 90) % 180) - 90
        for L in lotes:
            msp.add_lwpolyline(L["pts"], close=True, dxfattribs={"layer": "LOTES"})
            c = L["poly"].centroid
            msp.add_text(f"LOTE {L['lote']}", height=0.8, rotation=rot,
                         dxfattribs={"layer": "TEXTO"}).set_placement(
                (c.x, c.y), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
            if L.get("matricula"):
                msp.add_text(f"Mat. {L['matricula']}", height=0.45, rotation=rot,
                             dxfattribs={"layer": "TEXTO"}).set_placement(
                    (c.x, c.y - 1.2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
        for p, nm in nomes.items():
            msp.add_circle(p, 0.2, dxfattribs={"layer": "VERTICES"})
            msp.add_text(nm, height=0.45, dxfattribs={"layer": "TEXTO"}).set_placement(
                (p[0] + 0.3, p[1] + 0.3))
        doc.saveas(f"{saida}.dxf")
    except ImportError:
        print("ezdxf nao instalado: DXF nao gerado")

    # ------------------------------------------------------------------ previa
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(9, 6.5))
        if cfg.get("quadra_shp"):
            for s in shapefile.Reader(cfg["quadra_shp"]).shapes():
                x, y = zip(*s.points); ax.plot(x, y, color="green", lw=1.5)
        for L in lotes:
            x, y = zip(*(L["pts"] + L["pts"][:1]))
            ax.fill(x, y, color="red", alpha=.2); ax.plot(x, y, color="red", lw=1.8)
            c = L["poly"].centroid
            ax.text(c.x, c.y, f"LOTE {L['lote']}", ha="center", va="center", fontsize=8)
        for p, nm in nomes.items():
            ax.plot(*p, "k.", ms=3)
            ax.annotate(nm, p, xytext=(3, 3), textcoords="offset points", fontsize=6)
        U = unary_union([L["poly"] for L in lotes]).bounds
        m = max(U[2] - U[0], U[3] - U[1]) * 0.25 + 5
        ax.set_xlim(U[0] - m, U[2] + m); ax.set_ylim(U[1] - m, U[3] + m)
        ax.set_aspect("equal"); ax.grid(alpha=.3)
        ax.ticklabel_format(useOffset=False, style="plain"); ax.tick_params(labelsize=7)
        ax.set_title(cfg.get("titulo", os.path.basename(saida)), fontsize=10)
        plt.tight_layout(); plt.savefig(f"{saida}_previa.png", dpi=130)
    except ImportError:
        print("matplotlib nao instalado: previa nao gerada")

    print("\nVertices:")
    for p, nm in sorted(nomes.items(), key=lambda x: x[1]):
        print(f"  {nm}  E {p[0]:.3f}  N {p[1]:.3f}  ({', '.join(uniq[p])})")
    print(f"\nArquivos: {saida}_shapefile.zip, {saida}.dxf, {saida}_previa.png")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("inspecionar", "gerar"):
        print(__doc__); sys.exit(1)
    inspecionar(sys.argv[2]) if sys.argv[1] == "inspecionar" else gerar(sys.argv[2])
