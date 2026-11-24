# Estado da sessão — calculadora-da-reforma (23/11/2026 ~22:40)

Pedido do Nei (23/11): repo + projeto explicando os 3 repos da Receita (RTC regime regular, Simples, DANFSe) para pessoas/empresas/devs/contadores; pesquisar o que há de mais recente; explicavideo no lives4 + INEMA.VIBE (Telegram) e outro no lives8.

## Feito
- Repo público inematds/calculadora-da-reforma (9268136), Pages via Actions: https://inematds.github.io/calculadora-da-reforma/guia/ (+ en/, es/).
- Kit: PARA-QUEM, NOVIDADES, MEDICOES, scripts conferir-origem / subir-calculadoras / teste_do_motor.py, exemplos. Tudo rodado de verdade (JDK 25 em ~/.local/jdk25, Go 1.26).
- Banners 6 (Codex). Prints de vídeo guia/assets/video-{teste,cenarios,danfse}.png.
- Cadeias de vídeo: units ev-calculadora-reforma-lives4 e -lives8; pastas explicavideos/textos/calculadora-da-reforma{,-lives4,-lives8}; FATOS.md lá.

## Falta
1. Revisor independente do guia (runbook revisor-independente.md) + nota com revisor-nota.py.
2. Portal (skill atualiza-portal) + Telegram INEMA.VIBE (skill postar-telegram).
3. CONTINUAR.md nas 2 pastas de vídeo + continua --add (fase 2: Metricool lives4→inema.tds IG+TikTok, lives8→VIBE TikTok; embed no #video do guia PT/EN/ES + README; portal de vídeo; resposta no tópico INEMA.VIBE).
4. Memória project_calculadora_da_reforma.md + PRODUCOES-VIDEO.md.

## Atualização 23:05
- Revisor R1 (persona Márcia, contadora 46, não programa; MESMA lista fixa) reprovou nota 6; corrigido em 8cf0075 (passo 1 explica Claude Code/Codex, cards TI/fornecedor e Windows, teste com planilha CSV testado, +2.300 estrelas em MEDICOES, termos explicados). Registrado no revisor-nota.
- PRÓXIMO 1: revisor R2 NOVO, mesma persona e lista (pedido igual ao R1; ver runbook). Captura 390 px com ~/.cache/ms-playwright/chromium-1254/chrome-linux-arm64/chrome.
- PRÓXIMO 2: portal JÁ EDITADO e NÃO publicado: courses.ts (projectUpdatesData), Portal.tsx (communityProjects), translated-courses.ts (id 10260 en/es), gen:data feito; enrichment.json do inemapro-mono com projeto:calculadora-da-reforma-guia (inserido no início, formato de 1 linha). Falta: bash ~/.claude/skills/atualiza-portal/scripts/publica.sh "calculadora-da-reforma" (+ testes do portal p/ translated).
- PRÓXIMO 3: Telegram INEMA.VIBE (skill postar-telegram), tópico do kit; depois link dos vídeos.
- PRÓXIMO 4: CONTINUAR.md nas pastas explicavideos/textos/calculadora-da-reforma-lives4 e -lives8 (modelo: textos/sem-cara-de-ia-lives8/CONTINUAR.md; Metricool lives4→inema.tds IG+TikTok, lives8→VIBE só TikTok inema.prompts; embed #video no guia PT/EN/ES + README; portal de vídeo; resposta no tópico INEMA.VIBE) + `python3 ~/projetos/wifi/continua/continua.py --add ...` para cada.
- PRÓXIMO 5: memória project_calculadora_da_reforma.md + linha no MEMORY.md + PRODUCOES-VIDEO.md.
- Cadeias de vídeo rodando: systemctl --user status ev-calculadora-reforma-lives4 / -lives8; cadeia.log nas pastas.

## Atualização 23:12 — fase 1 FECHADA
- Revisor: R2 reprovou 7 (custo da assinatura, dados pela IA, vídeo vazio) → d33db7c; R3 (mesma persona/lista) aprovou 8 → 8f0adbd (CST). Notas no revisor-nota.
- Portal publicado: portal 6b6cc1c, inemabuscas d472cc6, inemapro 9e7ee03 (título do quadro encurtado para 90).
- Telegram INEMA.VIBE: tópico 4345 https://t.me/c/3650752323/4345, MENU msg 4363.
- CONTINUAR.md nas pastas -lives4 (guia+portal+Metricool inema.tds IG/TikTok) e -lives8 (só README+Metricool VIBE TikTok); continua msg 681 e 682.
- Memória wifi project_calculadora_da_reforma.md + MEMORY.md + 2 linhas no PRODUCOES-VIDEO.md.
- Resta só a fase 2 dos vídeos, pelo vigia.
