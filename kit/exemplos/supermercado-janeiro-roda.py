import json, sys, urllib.request, collections
sys.path.insert(0, sys.argv[0].rsplit("/", 1)[0])
from nota import L

NCM = {"Peito de frango congelado": "02071411", "Coxa e sobrecoxa congelada": "02071412",
       "Bebida láctea": "04039000", "Pão de alho": "19059090", "Pepino em conserva": "20011000",
       "Sobremesa láctea": "21069090", "Iogurte grego": "04032000", "Café torrado e moído": "09012100",
       "Batata palha": "20052000", "Açúcar cristal 5 kg": "17019900", "Sal 1 kg": "25010020",
       "Óleo de soja": "15079011", "Achocolatado em pó": "18069000", "Papel toalha": "48182000",
       "Leite integral UHT": "04012010", "Água mineral": "22011000", "Gelatina em pó": "21069090",
       "Leite condensado": "04029900", "Creme de leite": "04015029", "Farinha de trigo": "11010010",
       "Milho em conserva": "20058000", "Ervilha em conserva": "20054000", "Fermento biológico": "21021090",
       "Palito de dente": "44219900", "Vela de aniversário": "34060000", "Ketchup": "21032010",
       "Maionese": "21039011", "Doce de leite": "19019020", "Mostarda": "21033010",
       "Bicarbonato de sódio": "28363000", "Sagu (tapioca)": "19030000", "Amido de milho": "11081200"}
CLS = {"cesta": ("200", "200003"), "red60_lacteo": ("200", "200034"), "red60_2005": ("000", "000001"),
       "red60_amido": ("200", "200034"), "oleo": ("200", "200034"), "padrao": ("000", "000001"),
       "creme": ("000", "000001")}

def op(cbs):
    itens = []
    for i, (p, q, v, g) in enumerate(L, 1):
        cst, cl = CLS[g]
        itens.append({"numero": i, "ncm": NCM[p], "cst": cst, "cClassTrib": cl, "baseCalculo": v,
                      "quantidade": q, "unidade": "KG" if q % 1 else "UN",
                      "aliquotasNominais": {"cbs": cbs, "ibsEstadual": 0.05, "ibsMunicipal": 0.05}})
    return {"id": "nota-canela-janeiro", "versao": "1.0.0", "dhFatoGerador": "2027-01-15T17:03:10-03:00",
            "municipio": 4304408, "uf": "RS", "itens": itens}

def chama(o):
    r = urllib.request.Request("http://127.0.0.1:8180/api/calculadora/observabilidade/regime-geral",
                               data=json.dumps(o).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=60))

def acha(d, chave):
    if isinstance(d, dict):
        if chave in d: return d[chave]
        for v in d.values():
            x = acha(v, chave)
            if x is not None: return x
    if isinstance(d, list):
        for v in d:
            x = acha(v, chave)
            if x is not None: return x

out = {}
for cbs in (8.8, 11.3):
    o = op(cbs); res = chama(o)
    json.dump(o, open(f"op-{cbs}.json", "w"), ensure_ascii=False, indent=1)
    json.dump(res, open(f"resp-{cbs}.json", "w"), ensure_ascii=False, indent=1)
    itens = acha(res, "objetos") or acha(res, "itens")
    estados = collections.Counter(); por = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
    for it, (p, q, v, g) in zip(itens, L):
        estados[str(acha(it, "estadoItem"))] += 1
        vcbs = acha(it, "vCBS"); vibsuf = acha(it, "vIBSUF") or 0; vibsm = acha(it, "vIBSMun") or 0
        k = {"cesta": "cesta", "padrao": "cheia", "creme": "cheia", "red60_2005": "cheia"}.get(g, "red60")
        por[k][0] += v; por[k][1] += float(vcbs or 0); por[k][2] += float(vibsuf) + float(vibsm)
    print(f"CBS {cbs}%  estados={dict(estados)}")
    for k, (b, c, ib) in por.items():
        print(f"  {k:6s} base {b:9.2f}  CBS {c:8.2f}  IBS {ib:6.2f}")
    print(f"  TOTAL base {sum(x[0] for x in por.values()):.2f} CBS {sum(x[1] for x in por.values()):.2f} IBS {sum(x[2] for x in por.values()):.2f}")
    print("  totais do motor:", json.dumps(acha(res, "total"), ensure_ascii=False)[:600])
