#!/usr/bin/env bash
# Baixa, compila e sobe no seu computador os 3 motores abertos da Receita Federal.
# Uso: bash kit/scripts/subir-calculadoras.sh [pasta-de-trabalho]   (padrão: ./motores)
# Requisitos: git, curl, Java 25+ (JAVA_HOME ou java no PATH) e Go 1.22+ (só para o DANFSe).
# Portas (só no seu computador, 127.0.0.1): regime regular 8080, Simples 8082, DANFSe 8090.
# Variáveis para trocar portas: PORTA_REGULAR, PORTA_SIMPLES, PORTA_DANFSE.
set -euo pipefail

W="${1:-$PWD/motores}"
PR="${PORTA_REGULAR:-8080}"; PS="${PORTA_SIMPLES:-8082}"; PD="${PORTA_DANFSE:-8090}"
mkdir -p "$W/logs"; cd "$W"

JAVA="${JAVA_HOME:+$JAVA_HOME/bin/}java"
v=$("$JAVA" -version 2>&1 | head -1 | sed -E 's/.*version "([0-9]+).*/\1/')
if [ "${v:-0}" -lt 25 ] 2>/dev/null; then
  echo "Precisa de Java 25 ou mais novo (achei: ${v:-nenhum})."
  echo "Sem instalar no sistema: baixe o JDK 25 da Adoptium (adoptium.net), descompacte e rode"
  echo "  JAVA_HOME=/caminho/jdk-25 bash $0 $W"
  exit 2
fi
export JAVA_HOME="${JAVA_HOME:-$(dirname "$(dirname "$(readlink -f "$(command -v java)")")")}"

for r in calculadora-rtc-regime-regular calculadora-rtc-simples-nacional calculadora-rtc-gerador-danfse; do
  [ -d "$r/.git" ] || git clone -q https://github.com/ReceitaFederal/$r.git
  git -C "$r" pull -q --ff-only || true
  echo "$r em $(git -C "$r" describe --tags --always)"
done

# 1) Banco do regime regular (armadilha: a pasta calculadora/db precisa existir antes)
cd calculadora-rtc-regime-regular
mkdir -p calculadora/db
[ -s calculadora/db/calculadora-pro.db ] || ./mvnw -q flyway:migrate -Dflyway.configFiles=./flyway/flyway-pro.conf --batch-mode --errors
[ -s target/api-regime-geral.jar ] || ./mvnw -q clean package -DskipTests --batch-mode
cd ..

# 2) Simples Nacional (armadilha: não tem pasta flyway; usa o MESMO banco do regime regular)
cd calculadora-rtc-simples-nacional
mkdir -p calculadora/db
cp -n ../calculadora-rtc-regime-regular/calculadora/db/calculadora-pro.db calculadora/db/ 2>/dev/null || true
[ -s target/api-simples-nacional.jar ] || ./mvnw -q clean package -DskipTests --batch-mode
cd ..

# 3) Gerador de DANFSe (Go)
if command -v go >/dev/null; then
  (cd calculadora-rtc-gerador-danfse && go build -o ../danfse ./cmd/danfse)
else
  echo "Go não encontrado: o gerador de DANFSe fica de fora (o resto funciona)."
fi

# Sobe tudo só no seu computador (desligado do terminal: setsid + stdin fechado)
sobe() { # pasta log comando...
  local d="$1" n="$2"; shift 2
  ( cd "$W/$d" || exit 1; setsid nohup "$@" > "$W/logs/$n.log" 2>&1 < /dev/null & echo $! > "$W/logs/$n.pid" )
}
sobe calculadora-rtc-regime-regular regular "$JAVA" -Xmx1g -Dserver.address=127.0.0.1 -Dserver.port=$PR \
  -Dspring.profiles.active=offline -jar target/api-regime-geral.jar
sobe calculadora-rtc-simples-nacional simples "$JAVA" -Xmx1g -Dserver.address=127.0.0.1 -Dserver.port=$PS \
  -Dmanagement.server.port=$((PS+1021)) -Dspring.profiles.active=offline -jar target/api-simples-nacional.jar
[ -x danfse ] && sobe calculadora-rtc-gerador-danfse danfse env SERVER_PORT=$PD ../danfse

espera() { for _ in $(seq 1 90); do curl -s -o /dev/null "$1" && return 0; sleep 1; done; return 1; }
espera "http://127.0.0.1:$PR/api/swagger-ui.html" && echo "Regime regular no ar:  http://127.0.0.1:$PR/api/swagger-ui.html"
espera "http://127.0.0.1:$PS/api/swagger-ui.html" && echo "Simples Nacional no ar: http://127.0.0.1:$PS/api/swagger-ui.html"
[ -x danfse ] && espera "http://127.0.0.1:$PD/api/swagger-ui/index.html" && echo "DANFSe no ar:           http://127.0.0.1:$PD/api/swagger-ui/index.html"
echo "Para desligar: kill \$(cat $W/logs/*.pid)"
