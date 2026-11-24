#!/usr/bin/env python3
"""Reaplica nas páginas guia/en e guia/es o que o traduz-pagina-codex.py refaz do zero:
pedido do <pre> traduzido, banners por idioma, link do README por idioma e marca de página só em PT."""
import re
from pathlib import Path

G = Path(__file__).resolve().parents[2] / "guia"
P = {'en': '''Read the "calculadora-da-reforma" kit at https://github.com/inematds/calculadora-da-reforma (the README explains everything, including the technical setup).
Then, on this computer:
1. Check that the Receita Federal code is the original (conferir-origem script) and tell me the result.
2. See if I have what is needed (Java 25; Go only for the service invoice PDF). If something is missing, explain what and wait for my yes before downloading anything.
3. Start the calculator and run the official example. Show me in plain English the tax on each item and why.
4. Explain how to fill in the template spreadsheet kit/exemplos/minhas-vendas.csv with my company's sales, and run the test with it.
Do not change anything in my system or my files. Show me the plan and wait for me to say yes.''',
     'es': '''Lee el kit "calculadora-da-reforma" en https://github.com/inematds/calculadora-da-reforma (el README lo explica todo, incluida la instalación técnica).
Después, en este computador:
1. Verifica que el código de la Receita Federal sea el original (script conferir-origem) y dime el resultado.
2. Mira si tengo lo necesario (Java 25; Go solo para el PDF de la factura de servicios). Si falta algo, explícame qué y espera mi sí antes de descargar nada.
3. Levanta la calculadora y ejecuta el ejemplo oficial. Muéstrame en español sencillo el impuesto de cada ítem y el motivo.
4. Explícame cómo llenar la planilla modelo kit/exemplos/minhas-vendas.csv con las ventas de mi empresa y ejecuta la prueba con ella.
No cambies nada en mi sistema ni en mis archivos. Muéstrame el plan y espera a que diga sí.'''}
MARCA = {'en': ' (in Portuguese)', 'es': ' (en portugués)'}
for l, txt in P.items():
    p = G / l / "index.html"
    s = p.read_text()
    s = re.sub(r'(<pre id="pedidoTxt"[^>]*>).*?(</pre>)', lambda m: m.group(1) + txt + m.group(2), s, flags=re.S)
    s = s.replace('../assets/banner.jpg', f'../assets/banner-{l}.jpg').replace('../assets/banner-grade.jpg', f'../assets/banner-grade-{l}.jpg')
    s = s.replace('guia/assets/banner.jpg"', f'guia/assets/banner-{l}.jpg"')
    s = s.replace('calculadora-da-reforma#instalação-técnica', f'calculadora-da-reforma/blob/main/README.{l}.md')
    if 'MEDICOES.md</a>' + MARCA[l] not in s:
        s = s.replace('MEDICOES.md</a>', 'MEDICOES.md</a>' + MARCA[l])
    p.write_text(s)
    print(l, 'ok', s.count(f'banner-{l}.jpg'))
