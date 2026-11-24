# Medições (rodado de verdade em 23/11/2026)

Máquina: Linux arm64, JDK Temurin 25.0.5.1 em pasta local (sem instalar no sistema), Go 1.26.3.
Versões testadas: regime regular `f1eebd7` (1.7.2), Simples Nacional `a926d5a` (1.0.2), DANFSe `8d79e6b` (1.0.0).

## Autenticidade (Portaria Cotec nº 342/2026)

| Repositório | Tag inicial | Commit na Portaria | Tag no GitHub | Resultado |
|---|---|---|---|---|
| regime regular | 1.6.1 | `150cccbe414d…` | `150cccbe414d…` | igual |
| Simples Nacional | 0.0.6 | `c5b0f01c8351…` | `c5b0f01c8351…` | igual |
| DANFSe | 1.0.0 | `8d79e6b2f7fa…` | `8d79e6b2f7fa…` | igual |

O SHA-512 dos zips da Portaria **não** bate com o zip que o GitHub gera em `archive/refs/tags/<tag>.zip` (o GitHub monta o zip na hora, e o zip da Portaria foi feito pela Receita). Confira pelo commit: `kit/scripts/conferir-origem.sh`.

## Regime regular (CBS, IBS, Imposto Seletivo)

- Banco + compilação: 28 s. Subida do servidor: 6,2 s. Cálculo do exemplo oficial: 0,33 s (a 2ª chamada, 0,02 s).
- Exemplo oficial (`exemplos/operacao-oficial.json`, data 10/03/2027, Porto Alegre/RS, CBS 8,8%, IBS 0,05% + 0,05%):

| Item | O quê | Estado | Base | CBS | IBS |
|---|---|---|---|---|---|
| 1 | arroz da cesta básica (redução de 100%) | CALCULO_SIMULADO | 100,00 | 0,00 | 0,00 |
| 2 | cerveja com Imposto Seletivo (IS R$ 15,00) | CALCULO_SIMULADO | 165,00 | 14,52 | 0,16 |
| 3 | serviço de educação (redução de 60%) | CALCULO_SIMULADO | 1.200,00 | 42,24 | 0,48 |
| 4 | carne com classificação errada de propósito | INCONSISTENCIA_ENTRADA (REG-011, "NCM não vinculada") | – | – | – |
| | **Total** | | 1.465,00 | **56,76** | 0,64 |

Bate com o total publicado no `docs/exemplos.md` do repositório oficial.

- A mesma operação com CBS de **11,3%** (recomendação do TCU, ainda não aprovada): total de CBS **R$ 72,88** (item 2: 18,64; item 3: 54,24).
- No endpoint sem observabilidade (`/regime-geral`), a operação inteira volta com HTTP 422 por causa do item 4.
- Memória de cálculo do item 3, como sai do motor: "Operação de consumo com enquadramento legal em Art. 129, tributada conforme Alíquota reduzida em 60%. A base de cálculo utilizada é de R$ 1.200,00, com alíquota de 8,80%, sendo que esse regime define uma redução de 60,00% na alíquota."

## Nota de supermercado real em janeiro de 2027 (rodado em 24/11/2026, regime regular 1.7.2)

NFC-e real de 06/11/2026, supermercado de Canela/RS, 121 linhas, R$ 1.512,15 (dados pessoais e da loja fora). Transcrita em `exemplos/supermercado-janeiro-itens.py` (a soma confere com o total da nota). Entrada e resposta: `exemplos/operacao-supermercado-janeiro-cbs-8-8.json`, `...-11-3.json`, `resposta-supermercado-janeiro-*.json`. Data do fato gerador 15/01/2027, município 4304408, IBS 0,05% + 0,05%.

A nota não traz NCM: o INEMA escolheu o código de cada produto e conferiu o enquadramento no texto do anexo na própria base do programa. Supõe loja no regime regular e usa o valor de cada linha como base.

| Grupo | Produtos | Base | CBS 8,8% | CBS 11,3% |
|---|---|---|---|---|
| Anexo I, alíquota zero (Art. 125) | frango, leite UHT, café, açúcar, sal, farinha de trigo, sagu | 396,04 | 0,00 | 0,00 |
| Anexo VII, redução de 60% (Art. 135) | bebida láctea, iogurte, óleo de soja, amido de milho | 173,74 | 6,13 | 7,87 |
| Alíquota cheia | leite condensado, creme de leite, gelatina, conservas, molhos etc. | 942,37 | 83,01 | 106,43 |
| **Total** | 121 itens, todos `CALCULO_SIMULADO` | **1.512,15** | **89,14** | **114,30** |

IBS R$ 0,70 nas duas. Destaques: 81 leites condensados (404,19) → CBS 35,57 / 45,67; 81 cremes de leite (201,69) → 17,75 / 22,79; 19 óleos de soja (132,81) → 4,67 com 8,8% (seriam 11,69 sem a redução).

Armadilhas achadas: NCM 0207.14.00 não existe mais (REG-002), o certo é 0207.14.11 (peito) e 0207.14.12 (coxa e sobrecoxa); milho/ervilha em conserva e batata palha NÃO entram no item 16 do Anexo VII (só hortícola cozida sem sal nem outro ingrediente); pão de alho (1905.90.90) e gelatina (2106.90.90) aparecem ligados ao Anexo I, mas só para pão francês e fórmula infantil.

## Simples Nacional

- Compilação: 5 s (reaproveitando o banco do regime regular). Cálculo: 0,27 s.
- `exemplos/operacao-simples.json`: venda de R$ 1.000,00 de mercadoria (atividade 01, anexo I), alíquotas efetivas de exemplo IBS 1,25% e CBS 2,75% → IBS **R$ 12,50**, CBS **R$ 27,50**, total **R$ 40,00**, com memória de cálculo.
- Sem `pIBSSN`/`pCBSSN` o item volta com VSN-004 e VSN-006 ("alíquota ausente"): no Simples a alíquota efetiva vem do PGDAS-D, a calculadora não descobre sozinha.

## Gerador de DANFSe

- `go build` + `go test ./...`: 11 pacotes com teste, todos ok.
- XML fictício (`exemplos/nfse-exemplo.xml`) → PDF de 1 página, 79 KB, em **0,18 s**, com QR Code e a marca "NFS-e SEM VALIDADE JURÍDICA" (ambiente de homologação). Sem canhoto: `?canhoto=false`.

## Repercussão (GitHub, 23/11/2026)

| Repositório | Estrelas | Forks | Issues abertas |
|---|---|---|---|
| regime regular | 1.022 | 262 | 16 |
| Simples Nacional | 741 | 195 | 6 |
| gerador de DANFSe | 599 | 179 | 13 |
| **Total** | **2.362** | **636** | **35** |

## Planilha (CSV) no teste do motor

`kit/exemplos/minhas-vendas.csv` (arroz, mensalidade escolar com o valor errado de um sistema, carne com código errado) → arroz "igual", escola "DIFERENTE em vCBS, vIBS" (motor R$ 42,24 × sistema R$ 105,60), carne barrada com REG-011. Rodado em 23/11/2026.

## Armadilhas achadas (e o que o kit faz)

1. O README do regime regular não manda criar `calculadora/db`; sem a pasta, o `flyway:migrate` falha com `SQLITE_CANTOPEN`. O `subir-calculadoras.sh` cria.
2. O Simples não tem a pasta `flyway/` (issue #5 aberta): o banco é o mesmo do regime regular. O script copia.
3. Os dois motores Java pedem **Java 25**; JDK 8, 17 ou 21 não serve.
4. Porta 8080 ocupada é comum: use `PORTA_REGULAR`, `PORTA_SIMPLES` e `PORTA_DANFSE`.
5. A resposta da observabilidade é HTTP 200 mesmo com item errado: leia o `estadoItem` de cada item (o `teste_do_motor.py` faz isso).
6. Em 2027, a alíquota tem que ser informada e o resultado sai como `CALCULO_SIMULADO` até as alíquotas oficiais estarem cadastradas.
