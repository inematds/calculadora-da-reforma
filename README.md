# Calculadora aberta: confira se o seu sistema calcula a CBS e o IBS certo

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![Calculadora aberta](guia/assets/banner.jpg)](https://inematds.github.io/calculadora-da-reforma/guia/)

## O que é

Este kit explica e põe para funcionar os três programas que a Receita Federal abriu no GitHub em novembro de 2026: a calculadora da CBS, do IBS e do Imposto Seletivo (empresas do regime regular), a calculadora do Simples Nacional e o gerador do PDF da nota de serviço (DANFSe). Ele serve para empresas, contadores, desenvolvedores e curiosos. O kit traz o **teste do motor oficial**: a mesma operação calculada no seu sistema e no programa da Receita, lado a lado, com a diferença apontada. Você pede à sua IA que leia o kit e mostre o resultado. Quem prefere fazer à mão precisa de um computador com Java 25. **Não é produto da Receita**: é um kit do INEMA feito sobre o código aberto dela.

## 📖 Guia de uso

Guia completo (o que é, para quem, novidades de novembro, como começar): **https://inematds.github.io/calculadora-da-reforma/guia/**

<!-- VIDEO: entra o explicavideo do projeto quando publicado -->

## Peça para a sua IA

Abra o Claude Code ou o Codex numa pasta do seu computador e cole:

```text
Leia o kit "calculadora-da-reforma" em https://github.com/inematds/calculadora-da-reforma (o README explica tudo, inclusive a instalação técnica).
Depois, neste computador:
1. Confira se o código da Receita Federal é o original (script conferir-origem) e me diga o resultado.
2. Veja se tenho o que precisa (Java 25; Go só para o PDF da nota). Se faltar, me explique o que falta e espere o meu sim antes de baixar qualquer coisa.
3. Suba a calculadora e rode o exemplo oficial. Me mostre em português simples o imposto de cada item e o motivo.
4. Me diga como eu faria o mesmo teste com as vendas da minha empresa.
Não mude nada no meu sistema nem nos meus arquivos. Mostre o plano e espere eu dizer sim.
```

## O que tem aqui

| Arquivo | Para quê |
|---|---|
| [kit/PARA-QUEM.md](kit/PARA-QUEM.md) | Os 3 programas explicados, e o que ganha a pessoa, a empresa, o desenvolvedor e o contador |
| [kit/NOVIDADES.md](kit/NOVIDADES.md) | O que mudou em novembro de 2026 (alíquota de 11,3% indicada pelo TCU, versões novas, notas técnicas), com fonte |
| [kit/MEDICOES.md](kit/MEDICOES.md) | O que rodamos de verdade: números, tempos, versões e as armadilhas |
| `kit/scripts/conferir-origem.sh` | Confere se o código no GitHub é o da Portaria (commit das versões iniciais) |
| `kit/scripts/subir-calculadoras.sh` | Baixa, compila e sobe os 3 programas só no seu computador |
| `kit/scripts/teste_do_motor.py` | O teste do motor oficial: seu sistema × motor da Receita, e cenários de alíquota |
| `kit/exemplos/` | Operação oficial, cenário com CBS de 11,3%, operação do Simples, valores de um "sistema" com erro, NFS-e fictícia e o PDF gerado |

> **Atenção.** O código da Receita não tem efeito de lei nem suporte ao público (Portaria Cotec nº 342/2026, art. 6º). A responsabilidade pelo imposto continua de quem emite a nota. A licença MIT deixa usar o código, mas não o nome nem os símbolos da Receita para sugerir que um produto é oficial. Este kit não é oficial.

---

## Instalação técnica

### Pré-requisitos

- `git`, `curl`, Python 3 (só biblioteca padrão).
- **Java 25 ou mais novo** para as duas calculadoras (JDK 8, 17 ou 21 não servem). Sem instalar no sistema: baixe o JDK 25 da [Adoptium](https://adoptium.net), descompacte e use `JAVA_HOME=/caminho/jdk-25`.
- **Go 1.22+** só para o gerador de DANFSe (opcional).
- Internet na primeira vez (o Maven Wrapper baixa as dependências). Depois roda sem internet (perfil `offline`).
- Testado em Linux arm64 (23/11/2026). Os repositórios oficiais também trazem comandos para Windows.

### Passo a passo

```bash
git clone https://github.com/inematds/calculadora-da-reforma && cd calculadora-da-reforma

# 1. Conferir a origem (compara as tags iniciais com os commits da Portaria)
bash kit/scripts/conferir-origem.sh

# 2. Baixar, compilar e subir os 3 programas em ./motores (só em 127.0.0.1)
JAVA_HOME=/caminho/jdk-25 bash kit/scripts/subir-calculadoras.sh
#    portas padrão 8080 (regular), 8082 (Simples), 8090 (DANFSe); para trocar:
#    PORTA_REGULAR=18080 PORTA_SIMPLES=18082 PORTA_DANFSE=18090 bash kit/scripts/subir-calculadoras.sh

# 3. Calcular o exemplo oficial (arroz, cerveja com IS, escola, item com erro)
python3 kit/scripts/teste_do_motor.py kit/exemplos/operacao-oficial.json

# 4. Teste do motor oficial: comparar com o que o SEU sistema calculou
python3 kit/scripts/teste_do_motor.py kit/exemplos/operacao-oficial.json --meu kit/exemplos/meu-sistema-exemplo.json

python3 kit/scripts/teste_do_motor.py kit/exemplos/minhas-vendas.csv --data 2027-03-10   # sua planilha (Excel → CSV, separador ;)

# 5. Cenários de alíquota da CBS (8,8% do exemplo oficial × 11,3% do TCU)
python3 kit/scripts/teste_do_motor.py kit/exemplos/operacao-oficial.json --cbs 8.8 11.3

# 6. Simples Nacional
curl -s -X POST http://127.0.0.1:8082/api/calculadora/observabilidade/simples-nacional \
  -H 'Content-Type: application/json' -d @kit/exemplos/operacao-simples.json

# 7. PDF da NFS-e (DANFSe) a partir do XML
curl -s -X POST "http://127.0.0.1:8090/api/danfse" -H 'Content-Type: application/xml' \
  --data-binary @kit/exemplos/nfse-exemplo.xml -o danfse.pdf

# Desligar
kill $(cat motores/logs/*.pid)
```

Para usar com as suas operações: monte o JSON no formato de `kit/exemplos/operacao-oficial.json` (o Swagger em `http://127.0.0.1:8080/api/swagger-ui.html` mostra todos os campos) e o `meu.json` com o `vCBS`/`vIBS` que o seu sistema calculou para cada número de item. O `teste_do_motor.py` sai com código 1 se algum item diferir mais que `--tolerancia` (padrão R$ 0,01) ou vier com erro de entrada, então serve para teste automático (CI).

### Armadilhas que achamos (e que o script já contorna)

1. O passo do banco falha com `SQLITE_CANTOPEN` se a pasta `calculadora/db` não existir: o README oficial não diz para criá-la.
2. O Simples Nacional não tem a pasta `flyway/` (issue #5 aberta): usa o mesmo banco do regime regular.
3. A resposta com observabilidade é HTTP 200 mesmo com item errado: leia o `estadoItem` de cada item.
4. Em 2027, `aliquotasNominais` é obrigatório e o resultado sai como `CALCULO_SIMULADO` até as alíquotas oficiais estarem cadastradas.
5. No Simples, sem `pIBSSN`/`pCBSSN` o item volta com VSN-004/VSN-006: a alíquota efetiva vem do PGDAS-D.
6. O SHA-512 dos zips da Portaria não bate com o zip gerado pelo GitHub; confira pelo commit.

Detalhes e números: [kit/MEDICOES.md](kit/MEDICOES.md).

## O processo, do início ao fim

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Conferir que o código é o publicado na Portaria | `bash kit/scripts/conferir-origem.sh` | ⚙️ script |
| 2 | Baixar, compilar e subir os 3 motores | `bash kit/scripts/subir-calculadoras.sh` | ⚙️ script |
| 3 | Calcular o exemplo oficial e ler a memória de cálculo | `python3 kit/scripts/teste_do_motor.py kit/exemplos/operacao-oficial.json` | ⚙️ script |
| 4 | Montar as operações mais comuns da empresa e o que o seu sistema calculou | `kit/exemplos/*.json` como modelo | 🧠 você (ou a IA, com o seu sim) |
| 5 | Teste do motor oficial | `teste_do_motor.py OPERACAO.json --meu MEU.json` | ⚙️ script |
| 6 | Cenários de alíquota até o Senado fixar a CBS | `teste_do_motor.py OPERACAO.json --cbs 8.8 11.3` | ⚙️ script |
| 7 | Levar diferenças ao fornecedor/contador; repetir a cada versão nova da Receita | `git -C motores/<repo> pull` + passos 2–5 | 🧠 você |

## Fontes

- [Portaria Cotec nº 342/2026 (DOU de 13/11/2026)](https://www.in.gov.br/web/dou/-/portaria-cotec-n-342-de-12-de-novembro-de-2026-744398356)
- [Receita Federal: anúncio da publicação no GitHub](https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2026/novembro/receita-federal-publica-primeiro-codigo-fonte-aberto-no-github-e-amplia-transparencia-da-reforma-tributaria)
- Repositórios: [regime regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular) · [Simples Nacional](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional) · [gerador de DANFSe](https://github.com/ReceitaFederal/calculadora-rtc-gerador-danfse)
- Novidades de novembro com fontes: [kit/NOVIDADES.md](kit/NOVIDADES.md)

## Licença

Kit (textos, scripts, exemplos): MIT. O código da Receita Federal segue a licença MIT dos repositórios dela e não está copiado aqui (o script baixa direto da fonte).

---

Grátis no [inema.club](https://inema.club), direto na internet.
