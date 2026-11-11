# Documentação D.E.I.L.A.S. — Ensino Médio Público da Paraíba

**Projeto:** Diagnóstico da Qualidade do Ensino Médio Público na Paraíba  
**Público-alvo:** Governo do Estado da Paraíba, com foco em decisões para a rede estadual  
**Atualização:** 11/11/2026  
**Situação:** D/E/I estabelecidos; L/A em desenvolvimento; S com possibilidades de ação ainda não avaliadas.

## D — Definir objetivos

**Problema:** compreender quais necessidades educacionais da rede estadual da Paraíba podem ser identificadas pela integração de bases oficiais e como organizar evidências que apoiem políticas de melhoria.

**Questão norteadora:** Como a análise exploratória e a integração de dados do ENEM e de indicadores educacionais podem contribuir para identificar necessidades de aprendizagem no ensino médio público da Paraíba e fundamentar propostas de melhoria da qualidade do ensino?

**Objetivo geral:** analisar indicadores de desempenho, oferta e infraestrutura escolar, preservando as limitações de representação e de comparabilidade entre bases, para subsidiar recomendações ao governo estadual.

**Recorte:** escolas estaduais com ensino médio, participantes do ENEM com escola estadual da PB identificada e indicadores IDEB disponíveis.

## E — Escolher métricas

| Dimensão | Indicadores | Cuidados |
|---|---|---|
| Oferta educacional | Quantidade de escolas, municípios atendidos e matrículas de ensino médio | Unidade: escola ou matrículas agregadas, não participantes ENEM |
| Infraestrutura | Presença de internet, banda larga, biblioteca, laboratórios e quadra | Ausência e valores não informados são categorias diferentes |
| Participação no ENEM | Registros com escola estadual identificada; notas válidas por área | ENEM voluntário: não representa toda a rede |
| Desempenho ENEM | Média, mediana, quantis, dispersão e distribuição por área | Diferenciar presença, nota zero e nota ausente |
| IDEB | IDEB observado por escola, valores não divulgados, mediana e distribuição | Média simples das escolas não substitui o IDEB oficial da rede |
| Cobertura de dados | Correspondência de chaves entre ENEM e Censo | Não extrapolar de escolas/participantes pareados a toda a população |

## I — Identificar fontes

1. **ENEM 2024:** arquivos RESULTADOS e PARTICIPANTES, analisados separadamente quando não houver chave individual comum verificável.
2. **Censo Escolar 2024:** escolas, modalidade de oferta, infraestrutura e matrículas.
3. **IDEB 2025 por escola:** indicadores de rendimento, SAEB e nota observada, conforme a planilha oficial.
4. **ENEM 2025 e Censo Escolar 2025:** inclusão planejada, condicionada à coleta e à compatibilidade de esquemas.
5. **Taxas de rendimento e SAEB:** possíveis bases complementares, após confirmação da granularidade necessária.

Fontes: [INEP — ENEM](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem), [INEP — Censo Escolar](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar) e [INEP — IDEB](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb).

## L — Limpar dados

**Situação:** regras implementadas e testadas com dados sintéticos; processamento real em andamento.

1. Inspecionar estrutura de ZIP e dicionários.
2. Aplicar filtros reprodutíveis da Paraíba por ano, rede e oferta educacional.
3. Registrar contagens antes e depois dos filtros.
4. Preservar os arquivos brutos.
5. Padronizar tipos e códigos, investigar duplicidades, ausências e valores inválidos.
6. Diferenciar explicitamente nota zero, nota ausente e ausência nas provas.
7. Auditar chaves de escolas antes de integrar.

Documentos técnicos: [filtragem](estrategia_filtragem.md), [qualidade](relatorio_qualidade.md) e [integração](modelo_integracao.md).

## A — Analisar dados

**Achados descritivos já verificados:**

| Fonte | Achado |
|---|---|
| Censo 2024 | 482 escolas estaduais com oferta de ensino médio, distribuídas por 223 municípios |
| Censo 2024 | 116.779 matrículas declaradas no recorte |
| Censo 2024 | 459 escolas declararam internet; 139 banda larga; 233 laboratório de ciências |
| ENEM 2024 | 29.783 registros com escola estadual da PB; **21.786** notas válidas em Matemática e Ciências da Natureza |
| ENEM–Censo 2024 | 456 escolas com correspondência de código; 29.393 registros de ENEM encontraram escola no Censo |
| IDEB 2025 | 478 escolas estaduais na planilha, 458 com nota válida; média simples não ponderada 4,267 e mediana 4,3 |

Referências internas: [relatório consolidado](resultados_preliminares.md), [auditoria das chaves](../reports/filtragem/validacao_chaves_2024.md), [perfil ENEM/Censo](../reports/inspecao/perfil_paraiba.md) e [IDEB](../reports/inspecao/ideb_pb_2025.md).

**Ainda falta:** análise de distribuições e diferenças por localidade, investigação cuidadosa de covariáveis, integração escolar verificada após limpeza, avaliação de limitações amostrais e comparação temporal com dados de 2025.

## S — Sugerir soluções (hipóteses de políticas, não recomendações definitivas)

As possibilidades abaixo derivam de necessidades potenciais observáveis e **precisam de validação de campo, orçamento e avaliação de impacto**:

1. **Diagnóstico de conectividade:** auditar disponibilidade e qualidade de banda larga nas escolas que não registraram acesso ou têm informação ausente; priorizar intervenções somente após confirmar necessidades.
2. **Infraestrutura pedagógica:** avaliar laboratórios de ciências e informática nas escolas sem recursos declarados, considerando matrícula, situação do prédio e desigualdades territoriais.
3. **Apoio à aprendizagem:** examinar os resultados escolares do IDEB/SAEB, reprovação e indicadores de fluxo para direcionar ações de reforço e formação docente; não usar só notas do ENEM como critério.
4. **Monitoramento de políticas:** definir metas, indicadores de acesso e aprendizagem, cronograma e mecanismos de acompanhamento para estimar se as intervenções produziram melhorias.

## Produto final planejado

Dashboard executivo com:
- Visão do alcance da rede e distribuição de escolas;
- Indicadores comparativos de infraestrutura, com tratamento de ausentes;
- Desempenho ENEM e IDEB apresentados em visões separadas e claramente rotuladas;
- Recortes geográficos e evolução temporal quando as bases forem compatíveis;
- Lista de oportunidades para investigação e decisões públicas, com ressalvas metodológicas.

## Reprodutibilidade e integridade

- Os arquivos nacionais brutos não são versionados.
- Os scripts de preparação estão em `src/` e os testes em `tests/`.
- Relatórios agregados e auditáveis são armazenados em `reports/`.
- O pipeline de 2024 só publica resultados de integração quando a auditoria de chaves e os testes de qualidade não identificarem bloqueios.
- Não será feito relacionamento entre `PARTICIPANTES_2024` e `RESULTADOS_2024` por posição ou índice.

**Status final deste documento:** documentação metodológica em evolução, não relatório acadêmico finalizado.
