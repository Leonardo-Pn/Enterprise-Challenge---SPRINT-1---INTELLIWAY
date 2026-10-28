# Riscos e governança — versão inicial

| Risco | Impacto | Mitigação inicial | Evidência/ação pendente |
|---|---|---|---|
| Dados pessoais nos textos (LGPD) | Exposição de PII | Minimização, mascaramento antes de persistir texto, TLS, acesso por perfil e retenção limitada | Definir controlador/operador, finalidade, base legal e processo de direitos com orientação institucional/jurídica |
| Licença incompatível | Violação de termos | Inventário em `data/LICENSES.md`; bloquear incorporação sem revisão | Confirmar licença dos datasets e do gerador antes de usar |
| Uso indevido do detector | Atacantes refinam bypass | API key, rate limit, monitoramento, motivos públicos resumidos | Implementar rate limiting e gestão de segredos em deployment |
| Falso negativo | Injeção chega ao agente | Testes adversariais, métricas por origem, privilégio mínimo e confirmação humana | Executar benchmark e registrar resultados reais |
| Falso positivo | Conteúdo legítimo retido | Hard negatives e decisão REVIEW | Medir FPR em teste congelado |
| Dados sintéticos enviesados | Generalização ruim | Revisão humana, deduplicação, split por template | Registrar `generator`, `reviewed_by` e `template_id` |
| Prompt injection no portal/avaliador | Exposição ou decisão manipulada | Tratar texto como dado, escapar HTML, avaliador sem ferramentas nem acesso privilegiado | Implementar isolamento no portal |
| Retenção excessiva | Maior exposição | Não persistir conteúdo bruto por padrão; hash e metadados mínimos | Aprovar tabela de retenção antes de produção |
| Indisponibilidade | Consumidor sem decisão | Falha segura: reter para revisão, nunca presumir ALLOW | Testes de timeout e indisponibilidade |

## Política provisória de retenção
- Texto bruto: não persistir por padrão; se necessário para revisão, armazenar com acesso restrito e prazo aprovado.
- Metadados e hash: prazo a definir com PO e responsável por privacidade.
- Imagens/PDF: descartar após OCR, salvo autorização explícita e prazo definido.
- Logs de segurança: acesso restrito, sem segredos ou conteúdo integral desnecessário.

Os prazos do README são propostas de planejamento, não parecer jurídico nem política aprovada. A LGPD exige avaliação contextual; a equipe deve validar base legal, finalidade, necessidade, transparência, segurança e direitos dos titulares antes de uso real.

## Métricas e registro de versão
Acompanhar precision, recall, F1, ROC-AUC/PR-AUC, FPR em hard negatives, proporção REVIEW, recall por origem/tipo de ataque, latência p50/p95, memória e concordância com revisão humana. Toda métrica deve apontar para versão do modelo, hash do dataset, split e configuração. Não publicar valores fictícios como resultados.
