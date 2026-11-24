# O que tem de mais recente (conferido em 23/11/2026)

Datas e números com a fonte. Antes de usar em parecer ou decisão, abra a fonte oficial: as regras mudam durante a transição (2026–2033).

| Data | O quê | Fonte |
|---|---|---|
| 12–13/11/2026 | Portaria Cotec nº 342 autoriza abrir os 3 repositórios, registra os hashes das versões iniciais, diz que o código é MIT e que **não** implica suporte, manutenção nem efeito normativo (art. 6º). | [DOU](https://www.in.gov.br/web/dou/-/portaria-cotec-n-342-de-12-de-novembro-de-2026-744398356) |
| 16/11/2026 | Receita anuncia a publicação no GitHub (organização `ReceitaFederal`). O código já podia ser baixado pela Plataforma CBS desde 2025; agora tem histórico, versões e issues públicas. | [Receita Federal](https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2026/novembro/receita-federal-publica-primeiro-codigo-fonte-aberto-no-github-e-amplia-transparencia-da-reforma-tributaria) |
| 18–19/11/2026 | **Regime regular 1.7.2**: corrige o arredondamento. Antes, um total podia diferir da soma dos itens (rejeição 1091, "Total de CBS difere da soma dos itens"); agora cada número é arredondado uma vez. Quem integra vê diferença de centavos em relação à 1.7.0. | [CHANGELOG](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/main/CHANGELOG.md) |
| 20/11/2026 | **Simples Nacional 1.0.2** publicado. Em 23/11 os três repositórios somavam 35 issues abertas da comunidade (16 no regime regular, 6 no Simples, 13 no DANFSe) e mais de 600 forks. No Simples, por exemplo: README com porta e nome de JAR trocados, pasta `flyway` que não existe, totais que podem divergir da soma. | [Issues](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional/issues) |
| 10/11/2026 | TCU entrega ao Senado estudo que recomenda **11,3%** como alíquota de referência da CBS para 2027 (cálculo detalhado 11,3468%). O Senado fixa por resolução até 15/12. **Ainda não é a alíquota definitiva.** | [Senado](https://www12.senado.leg.br/noticias/materias/2026/11/10/senado-recebe-acordao-do-tcu-que-propoe-aliquota-de-11-3-para-a-cbs) |
| 17/11/2026 | Ministro da Fazenda defende o início da CBS em janeiro e estima alíquota efetiva média de 8,5%. Esse número é diferente da alíquota de referência e não vale como reajuste uniforme de preço. | [Senado](https://www12.senado.leg.br/noticias/materias/2026/11/17/no-senado-ministro-da-fazenda-defende-novo-tributo-sobre-o-consumo) |
| 09/11/2026 | Receita libera APIs de apuração da CBS (débitos e créditos). | [Receita Federal](https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2026/novembro/receita-federal-libera-acesso-as-novas-apis-de-apuracao-da-cbs) |
| 13/11/2026 | PGDAS-D: em nov. e dez./2026, informar a folha dos últimos 12 meses (FS12) para todas as atividades; a partir de 2027 a apuração do Simples é por competência. Os dados alimentam a alíquota efetiva de IBS/CBS das notas. | [Radar da Reforma, resumo com fontes oficiais](https://radardareformatributaria.com/radar-reforma-tributaria-o-que-mudou-novembro-2026/) |
| nov./2026 | Cinco notas técnicas de NF-e/NFC-e (IBS, CBS, IS): valor total passa a incluir os tributos "por fora", novos campos de valor líquido (NT 2026.008) e DANFE (NT 2026.010). | [Contábeis](https://www.contabeis.com.br/noticias/79836/nf-e-e-nfc-e-cinco-notas-tecnicas-atualizam-regras-do-ibs-e-da-cbs/) |

## O que isso significa na prática

1. **2027 começa daqui a 5 semanas** e a CBS substitui PIS/Cofins. Quem tem sistema próprio precisa testar agora.
2. **A alíquota ainda não está fechada.** Por isso a calculadora de 2027 pede a alíquota e marca o resultado como simulado. Faça cenários (8,8% do exemplo oficial, 11,3% do TCU) e refaça quando o Senado publicar.
3. **O motor já mudou duas vezes em novembro.** Fixe a versão que usa e anote a data.
