# Para quem serve, e o que cada um ganha

A Receita Federal abriu (licença MIT, Portaria Cotec nº 342/2026) três programas que já usa na Reforma Tributária do Consumo. Eles não são um site para consultar. São **motores**: programas que você baixa, roda no seu computador ou servidor e consulta por endereço HTTP (API REST).

| Motor | O que faz | Língua |
|---|---|---|
| `calculadora-rtc-regime-regular` | Calcula CBS, IBS (estadual e municipal) e Imposto Seletivo por item, com **memória de cálculo em português** e o artigo da lei aplicado. Também gera e valida o XML do grupo de tributação da nota. | Java 25 |
| `calculadora-rtc-simples-nacional` | Calcula CBS e IBS das operações de quem é do Simples Nacional, a partir da alíquota efetiva. | Java 25 |
| `calculadora-rtc-gerador-danfse` | Transforma o XML da NFS-e no PDF (DANFSe), com QR Code e canhoto. | Go |

O que muda é que agora o cálculo deixa de ser uma caixa-preta: qualquer um pode rodar o mesmo motor que a Receita usa e comparar com o próprio sistema. O kit chama isso de **teste do motor oficial**.

---

## Pessoa física, estudante, curioso

- **Ganha:** ver com os próprios olhos como um imposto sobre consumo é montado, item por item. A resposta diz, em português, "base R$ 1.200,00, alíquota 8,80%, redução de 60%, Art. 129".
- **Faz:** roda o exemplo do kit e muda uma alíquota para ver o efeito (`--cbs 8.8 11.3`).
- **Não faz:** não é calculadora de preço de supermercado nem de imposto de renda.

## Empresa (dono, financeiro, compras)

- **Ganha:** um jeito de **conferir o seu sistema** antes de 2027, quando a CBS passa a ser cobrada. Se o ERP calcular diferente do motor oficial, você descobre agora, não na autuação.
- **Ganha também:** simular cenários de preço com a alíquota que o Senado ainda vai fixar (o TCU indicou 11,3% para a CBS; o Senado decide até 15/12/2026).
- **Faz:** pede ao fornecedor do sistema (ou ao seu TI) para rodar o teste do motor nas suas notas mais comuns.
- **Cuidado:** o código **não tem efeito de lei** e **não vem com suporte** (Portaria, art. 6º). A responsabilidade pelo imposto continua sua.

## Desenvolvedor, software house, ERP, emissor de nota

- **Ganha:** o motor de referência para testes automáticos. Mesmo pedido, seu código × motor oficial, diferença acusada em centavos.
- **Ganha também:** geração e validação do XML do grupo IBS/CBS contra o XSD (`/xml/generate`, `/xml/validate`), base de cálculo unificada da NF-e/NFC-e e da NFS-e, e o gerador de DANFSe pronto.
- **Pode:** embutir o motor no seu produto (MIT), desde que **não use o nome nem os símbolos da Receita** para sugerir que o produto é oficial.
- **Precisa:** acompanhar as versões (já são 1.7.2 e 1.0.2 em 20/11/2026) e registrar qual versão estava em uso em cada período.

## Contador e escritório contábil

- **Ganha:** uma segunda opinião independente do ERP do cliente. Rodou a nota no motor e deu diferente? O motor mostra o porquê: classificação (`cClassTrib`), redução, NCM/NBS que não casa.
- **Ganha também:** a **memória de cálculo com a fundamentação legal**, pronta para anexar ao parecer ou explicar ao cliente.
- **Faz:** pega as 10 operações mais comuns de cada cliente, roda no motor e guarda o resultado com a data e a versão do motor. Isso vira prova de diligência.
- **Cuidado:** em 2027 a calculadora exige que você informe a alíquota (`aliquotasNominais`) e marca o resultado como `CALCULO_SIMULADO` até as alíquotas oficiais estarem cadastradas.

---

## O que NÃO é

- Não é lei nem tem efeito normativo.
- Não tem suporte da Receita para o público externo.
- Não atualiza sozinho o sistema da empresa: alguém precisa baixar cada versão nova e testar.
- Não emite nota fiscal. Calcula, gera e valida o XML do grupo de tributação, e gera o PDF da NFS-e.
