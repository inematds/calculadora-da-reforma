# FALHAS

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-11-24 | Pages: todos os deploys desde 9268136 falharam (upload-pages-artifact@v3 sem artefato); o "200" de 23/11 era a página velha | upload-pages-artifact@v4 (push por SSH) + 1 workflow_dispatch; conferir o conteúdo no ar, não só o 200 | infra |
| 2026-11-23 | subir-calculadoras.sh: `( cd && setsid java & )` mandava o bloco todo ao fundo, segurava a saída do terminal e gravava o PID errado | `cd || exit 1;` antes do `setsid … &` | prompt |
