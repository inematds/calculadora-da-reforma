#!/usr/bin/env bash
# Confere se as versões iniciais nos repositórios da Receita Federal são as mesmas
# registradas na Portaria Cotec nº 342/2026 (DOU de 13/11/2026, Seção 1 Extra B, p. 10).
# Uso: bash kit/scripts/conferir-origem.sh            (consulta o GitHub com git, sem login)
#      bash kit/scripts/conferir-origem.sh <pasta>    (confere clones locais já baixados em <pasta>)
set -u

# repo | tag inicial | SHA-1 do commit publicado na Portaria
LISTA="calculadora-rtc-regime-regular 1.6.1 150cccbe414d4a5edea703e4f7a424af5aa222c7
calculadora-rtc-simples-nacional 0.0.6 c5b0f01c8351c3f0d0795cc617b29d233e9f98df
calculadora-rtc-gerador-danfse 1.0.0 8d79e6b2f7fad6375340afcb51c85ed370c64a14"

PASTA="${1:-}"
falhas=0
while read -r repo tag esperado; do
  if [ -n "$PASTA" ] && [ -d "$PASTA/$repo/.git" ]; then
    git -C "$PASTA/$repo" fetch -q --tags origin 2>/dev/null
    achado=$(git -C "$PASTA/$repo" rev-parse "refs/tags/$tag^{commit}" 2>/dev/null)
  else
    achado=$(git ls-remote "https://github.com/ReceitaFederal/$repo.git" "refs/tags/$tag" "refs/tags/$tag^{}" 2>/dev/null | tail -1 | cut -f1)
  fi
  if [ "$achado" = "$esperado" ]; then
    echo "OK     $repo  tag $tag = commit ${esperado:0:12} (igual à Portaria)"
  else
    echo "FALHOU $repo  tag $tag: esperado ${esperado:0:12}, achado '${achado:0:12}'"
    falhas=$((falhas+1))
  fi
done <<< "$LISTA"

echo
echo "Endereço oficial: https://github.com/ReceitaFederal (cópia de outro lugar = não use)."
echo "Obs.: o zip que o GitHub gera na hora NÃO tem o mesmo SHA-512 da Portaria; confira pelo commit."
exit $falhas
