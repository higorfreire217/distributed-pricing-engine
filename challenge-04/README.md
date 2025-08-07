# Desafio 4: Cenário de Crise Real

## Situação

Segunda-feira, 8h30:
- Bloomberg API fora do ar desde 6h (40% dos preços dependem dela)
- Investidor institucional ligou exigindo NAV atualizado até 10h
- CVM marcou call às 14h para discutir "inconsistências" nos relatórios
- Sistema de backup também está com problemas

---

## Plano de Contingência Técnico

### 1. Priorização de Ações

1. **Identificar ativos impactados**: Listar quais preços dependem da Bloomberg.
2. **Acionar fontes alternativas**: Buscar dados em outras APIs e provedores.
3. **Atualizar NAV com dados alternativos**: Gerar cálculo provisório.
4. **Comunicar stakeholders**: Informar status e plano de ação.
5. **Restaurar sistema de backup**: Tentar reestabelecer redundância.
6. **Preparar documentação para CVM**: Detalhar inconsistências e medidas tomadas.

---

### 2. Fontes Alternativas de Dados

- **Reuters Eikon**
- **Yahoo Finance API**
- **Morningstar Direct**
- **B3 (Bolsa Brasileira)**
- **Web scraping de sites confiáveis**
- **Contatos diretos com brokers**

---

### 3. Comunicação

- **Investidor Institucional**: Informar que o NAV será atualizado com dados alternativos, garantir transparência e estimar prazo.
- **CVM**: Explicar a falha técnica, detalhar fontes alternativas utilizadas e enviar documentação do processo.
- **Equipe Interna**: Atualizar status em tempo real, delegar tarefas e registrar decisões.
- **Gestores/Clientes**: Comunicar sobre a contingência, reforçar compromisso com precisão e compliance.

---

### 4. Prevenção

- **Redundância de provedores de dados**
- **Monitoramento proativo de APIs**
- **Testes regulares de backup e recuperação**
- **Procedimentos claros de contingência**
- **Automatização de alertas e failover**
- **Documentação e treinamento contínuo da equipe**

---

Este plano visa garantir a continuidade operacional, transparência e conformidade regulatória diante de falhas críticas de infraestrutura.
