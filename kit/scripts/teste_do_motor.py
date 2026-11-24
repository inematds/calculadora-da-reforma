#!/usr/bin/env python3
"""Teste do motor oficial: o mesmo pedido no seu sistema e no motor aberto da Receita, lado a lado.

Uso:
  python3 kit/scripts/teste_do_motor.py OPERACAO.json                     # só calcula e mostra
  python3 kit/scripts/teste_do_motor.py OPERACAO.json --meu MEU.json      # compara com o seu sistema
  python3 kit/scripts/teste_do_motor.py OPERACAO.json --cbs 8.8 11.3      # mesma nota, alíquotas de CBS diferentes
Opções: --url (padrão http://127.0.0.1:8080/api/calculadora) --tolerancia 0.01 (R$)

MEU.json = o que o SEU sistema (ERP, planilha, emissor) calculou, por número do item:
  {"1": {"vCBS": "0.00", "vIBS": "0.00"}, "3": {"vCBS": "42.24", "vIBS": "0.48"}}
Sai com código 1 se algum item diferir mais que a tolerância ou vier com erro.
Só biblioteca padrão do Python. Não substitui a lei nem a revisão do seu contador.
"""
import argparse, copy, json, sys, urllib.request, urllib.error
from decimal import Decimal


def calcula(url, op):
    req = urllib.request.Request(url.rstrip("/") + "/observabilidade/regime-geral",
                                 data=json.dumps(op).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"O motor recusou o pedido (HTTP {e.code}): {e.read().decode()[:400]}")
    except urllib.error.URLError as e:
        sys.exit(f"Motor fora do ar em {url} ({e.reason}). Rode antes: bash kit/scripts/subir-calculadoras.sh")


def itens(resp):
    out = {}
    for o in resp.get("objetos", []):
        g = ((o.get("tribCalc") or {}).get("IBSCBS") or {}).get("gIBSCBS") or {}
        out[str(o["nObj"])] = {
            "estado": o.get("estadoItem"),
            "vBC": g.get("vBC"),
            "vCBS": (g.get("gCBS") or {}).get("vCBS"),
            "vIBS": g.get("vIBS"),
            "erros": [f'{e.get("code")}: {e.get("title")}' for e in o.get("erros", [])],
        }
    return out


def total(resp):
    t = ((resp.get("total") or {}).get("tribCalc") or {}).get("IBSCBSTot") or {}
    return (t.get("gCBS") or {}).get("vCBS"), (t.get("gIBS") or {}).get("vIBS")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("operacao")
    ap.add_argument("--meu")
    ap.add_argument("--cbs", nargs="+", type=float)
    ap.add_argument("--url", default="http://127.0.0.1:8080/api/calculadora")
    ap.add_argument("--tolerancia", default="0.01")
    a = ap.parse_args()
    op = json.load(open(a.operacao, encoding="utf-8"))

    if a.cbs:
        print(f"{'CBS %':>7} {'total CBS (R$)':>15} {'total IBS (R$)':>15}")
        for taxa in a.cbs:
            o2 = copy.deepcopy(op)
            for it in o2.get("itens", []):
                if "aliquotasNominais" in it:
                    it["aliquotasNominais"]["cbs"] = taxa
            c, i = total(calcula(a.url, o2))
            print(f"{taxa:>7.2f} {c or '-':>15} {i or '-':>15}")
        print("\nAlíquota informada à mão = cálculo SIMULADO (o motor avisa). Use para cenário, não para nota.")
        return 0

    resp = calcula(a.url, op)
    motor = itens(resp)
    meu = json.load(open(a.meu, encoding="utf-8")) if a.meu else {}
    tol = Decimal(a.tolerancia)
    ruins = 0
    print(f"{'item':>4} {'estado':<24} {'CBS motor':>10} {'IBS motor':>10}" + (f" {'CBS seu':>9} {'IBS seu':>9}  resultado" if meu else ""))
    for n, m in motor.items():
        linha = f"{n:>4} {m['estado'] or '-':<24} {m['vCBS'] or '-':>10} {m['vIBS'] or '-':>10}"
        if m["erros"]:
            ruins += 1
            linha += "   ERRO NA ENTRADA: " + "; ".join(m["erros"])
        elif meu:
            s = meu.get(n, {})
            dif = [k for k in ("vCBS", "vIBS")
                   if s.get(k) is not None and m[k] is not None and abs(Decimal(str(s[k])) - Decimal(m[k])) > tol]
            falta = s == {}
            linha += f" {s.get('vCBS', '-'):>9} {s.get('vIBS', '-'):>9}  " + (
                "sem valor seu" if falta else ("DIFERENTE em " + ", ".join(dif) if dif else "igual"))
            ruins += 1 if (dif or falta) else 0
        print(linha)
    c, i = total(resp)
    print(f"\nTotal do motor: CBS R$ {c} · IBS R$ {i} (só itens calculados)")
    print("Memória de cálculo e fundamentação legal de cada item: veja 'memoriaCalculo' na resposta completa.")
    if ruins:
        print(f"{ruins} item(ns) pedem atenção: confira cadastro (NCM/NBS, CST, cClassTrib) antes de emitir.")
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main())
