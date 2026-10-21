#!/usr/bin/env python3
"""Extrai de um KML/KMZ o ponto (lat, lon em graus decimais) para o campo
"Coordenadas Geográficas" da ART.

Regras:
- Point: usa o próprio ponto.
- Polygon: usa o centroide de área; se ele cair fora do polígono (formatos
  em L, U etc.), usa o meio do maior trecho interno na latitude do centroide,
  que fica garantidamente dentro da área.
- Vários polígonos: usa o de maior área (e avisa).
- LineString: usa o vértice do meio.
Saída: "-2.797025, -40.516805" (6 casas, formato das ARTs do SITAC) + avisos.
Uso: python3 kml_ponto.py arquivo.kml|kmz [--uf CE]
"""
import sys, zipfile, re
import xml.etree.ElementTree as ET

# Envelopes aproximados das UFs (lat_min, lat_max, lon_min, lon_max) para alerta
UF_BBOX = {"CE": (-7.90, -2.75, -41.45, -37.20)}

def ler_kml(caminho):
    if caminho.lower().endswith(".kmz"):
        with zipfile.ZipFile(caminho) as z:
            nome = next(n for n in z.namelist() if n.lower().endswith(".kml"))
            return z.read(nome)
    with open(caminho, "rb") as f:
        return f.read()

def coords(txt):
    pts = []
    for tok in txt.split():
        p = tok.split(",")
        if len(p) >= 2:
            pts.append((float(p[0]), float(p[1])))  # (lon, lat)
    return pts

def area_centroide(anel):
    a = cx = cy = 0.0
    n = len(anel)
    for i in range(n):
        x0, y0 = anel[i]; x1, y1 = anel[(i + 1) % n]
        c = x0 * y1 - x1 * y0
        a += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c
    a /= 2.0
    if a == 0:
        xs, ys = zip(*anel); return 0.0, (sum(xs)/n, sum(ys)/n)
    return abs(a), (cx / (6 * a), cy / (6 * a))

def dentro(pt, anel):
    x, y = pt; ins = False; n = len(anel)
    for i in range(n):
        x0, y0 = anel[i]; x1, y1 = anel[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            ins = not ins
    return ins

def ponto_interno(anel, y):
    xs = []; n = len(anel)
    for i in range(n):
        x0, y0 = anel[i]; x1, y1 = anel[(i + 1) % n]
        if (y0 > y) != (y1 > y):
            xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
    xs.sort()
    trechos = [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]
    a, b = max(trechos, key=lambda t: t[1] - t[0])
    return ((a + b) / 2, y)

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    uf = sys.argv[sys.argv.index("--uf") + 1].upper() if "--uf" in sys.argv else "CE"
    raiz = ET.fromstring(ler_kml(sys.argv[1]))
    tag = lambda e: re.sub(r"\{.*\}", "", e.tag)
    poligonos, pontos, linhas = [], [], []
    for e in raiz.iter():
        t = tag(e)
        if t == "Polygon":
            for sub in e.iter():
                if tag(sub) == "outerBoundaryIs":
                    for c in sub.iter():
                        if tag(c) == "coordinates":
                            poligonos.append(coords(c.text))
        elif t == "Point":
            for c in e.iter():
                if tag(c) == "coordinates": pontos.append(coords(c.text)[0])
        elif t == "LineString":
            for c in e.iter():
                if tag(c) == "coordinates": linhas.append(coords(c.text))
    avisos = []
    if poligonos:
        calc = [(area_centroide(p), p) for p in poligonos]
        (_, cen), anel = max(calc, key=lambda t: t[0][0])
        if len(poligonos) > 1:
            avisos.append(f"{len(poligonos)} polígonos no arquivo; usei o de maior área.")
        pt = cen if dentro(cen, anel) else ponto_interno(anel, cen[1])
        if pt is not cen:
            avisos.append("Centroide caía fora do polígono; usei ponto interno.")
    elif pontos:
        pt = pontos[0]
        if len(pontos) > 1: avisos.append(f"{len(pontos)} pontos no arquivo; usei o primeiro.")
    elif linhas:
        l = linhas[0]; pt = l[len(l) // 2]; avisos.append("Só havia linha; usei o vértice do meio.")
    else:
        print("ERRO: nenhuma geometria encontrada."); sys.exit(2)
    lon, lat = pt
    if uf in UF_BBOX:
        la0, la1, lo0, lo1 = UF_BBOX[uf]
        if not (la0 <= lat <= la1 and lo0 <= lon <= lo1):
            avisos.append(f"ATENÇÃO: ponto parece estar FORA de {uf}. A ART deve ser registrada no CREA do local da obra/serviço.")
    print(f"{lat:.6f}, {lon:.6f}")
    for a in avisos: print("AVISO:", a)

if __name__ == "__main__":
    main()
