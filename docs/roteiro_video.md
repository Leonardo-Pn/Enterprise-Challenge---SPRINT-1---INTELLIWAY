# Roteiro sugerido — vídeo de apresentação (até 5 minutos)

> Substituir os trechos entre colchetes e gravar narração humana. O link final deve ser publicado como não listado e inserido no README.

1. **0:00–0:30 — Apresentação**: nome do projeto, equipe, turma e decisão sobre participação no prêmio.
2. **0:30–1:10 — Problema**: diferenciar prompt injection direta e indireta; citar riscos para prompts, dados internos e ferramentas.
3. **1:10–1:50 — Proposta**: mostrar o fluxo consumidor → ingestão/OCR → API → motor sem LLM → decisão → registro/portal.
4. **1:50–2:35 — Dados**: explicar exemplos próprios, datasets públicos somente após checagem de licença, sintéticos revisados e hard negatives; explicar split por template.
5. **2:35–3:20 — Motor**: apresentar baseline por regras, TF-IDF + classificador e plano DeBERTa/LoRA; deixar claro o que está implementado hoje.
6. **3:20–4:05 — API e operação**: demonstrar `/healthz` e `/v1/analyze` localmente, mostrando um exemplo benigno e um suspeito.
7. **4:05–4:40 — Governança e evolução**: LGPD, retenção, falha segura, plano das Sprints 2–4.
8. **4:40–5:00 — Fechamento**: principais entregas da Sprint 1 e próximos passos.

Não apresentar metas como resultados medidos. Mostrar apenas demonstrações executadas e artefatos existentes.
