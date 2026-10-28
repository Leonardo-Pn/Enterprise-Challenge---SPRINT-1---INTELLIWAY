# Wireframes de baixa fidelidade

Os wireframes de texto estão no README principal, Seção 7. Navegação proposta: Login → Painel ⇄ Histórico → Detalhe da decisão → Revisão humana. Menu lateral: Painel, Histórico, Fila de revisão, Modelos e Configurações.

## Telas e campos
- **Login:** e-mail, senha, recuperar acesso.
- **Painel (PO):** filtro de versão/período; precision, recall, F1, AUC e % REVIEW; volume diário por decisão; métricas por `source_type`; comparação de versões.
- **Histórico:** filtros por data, decisão, origem e texto/ID; tabela com timestamp, origem, decisão, score, versão e estado da revisão.
- **Detalhe/revisão:** conteúdo com PII mascarada, trecho suspeito, motivos, metadados OCR quando houver; rótulo ataque/falso positivo/incerto, tipo de ataque e comentário.
- **Modelos:** versão, hash do dataset, configuração, métricas e model card.

Os números exibidos nos esboços do README são fictícios e não podem ser apresentados como métricas reais. Portal ainda não implementado neste scaffold.
