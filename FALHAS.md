# FALHAS

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-11-23 | subir-calculadoras.sh: `( cd && setsid java & )` mandava o bloco todo ao fundo, segurava a saída do terminal e gravava o PID errado | `cd || exit 1;` antes do `setsid … &` | prompt |
