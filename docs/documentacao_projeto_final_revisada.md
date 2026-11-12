# Projeto INEP
## Diagnóstico da Qualidade do Ensino Médio Público da Paraíba
### Documentação acadêmica, técnica e funcional — Versão revisada

**Disciplina:** Análise de Dados  
**Público-alvo:** Governo do Estado da Paraíba  
**Equipe:** Pedro Alexandre; Pedro Henrique Faustino; Maria Vitória Espínola Carneiro  
**Data de atualização:** 12 de novembro de 2026  
**Status:** preparação, auditoria e análise exploratória de 2024 executadas; estrutura de cinco dashboards Power BI definida, com implementação do arquivo PBIX ainda pendente; processamento completo de 2025 e relatório conclusivo também pendentes.

> **Síntese executiva.** O projeto integra, de maneira auditável e metodologicamente cautelosa, indicadores oficiais de aprendizagem, infraestrutura e oferta do ensino médio público da Paraíba. Sua finalidade é identificar diferenças entre escolas e municípios e oferecer evidências para a avaliação de políticas educacionais — sem confundir associação com causalidade ou resultados amostrais com toda a rede estadual.

---

# 1. Introdução, contexto e objetivos

## 1.1. Objetivo geral

Desenvolver um processo reproduzível de inspeção, limpeza, integração e análise exploratória de bases educacionais públicas, acompanhado de **um relatório Power BI com cinco páginas analíticas integradas**, para diagnosticar aspectos da qualidade do ensino médio público da Paraíba e subsidiar propostas de melhoria da aprendizagem na gestão estadual.

## 1.2. Contexto e justificativa

O Governo do Estado precisa interpretar dados de desempenho, fluxo escolar, infraestrutura e condições de oferta de ensino de maneira articulada. A disponibilização de microdados e indicadores pelo INEP torna possível transformar informações dispersas em diagnósticos compreensíveis, com recortes territoriais que apoiem decisões de acompanhamento pedagógico e alocação de recursos.

Não se pressupõe que correlações representem relações de causa e efeito. O valor do projeto está na **identificação de necessidades e hipóteses verificáveis**, na documentação das fontes e na transparência dos critérios de análise.

## 1.3. Pergunta central

**Quais necessidades de aprendizagem e desigualdades educacionais podem ser identificadas no ensino médio público da Paraíba, e que intervenções governamentais merecem avaliação à luz das evidências disponíveis?**

## 1.4. Objetivos específicos

1. Catalogar, inspecionar e documentar os microdados e indicadores educacionais oficiais aplicáveis à Paraíba.
2. Construir recortes reprodutíveis, com identificação explícita do ano, da rede de ensino e da unidade de análise.
3. Validar a integridade, o tratamento de ausências e a correspondência das chaves escolares.
4. Descrever aprendizagem, rendimento, oferta, matrículas e infraestrutura conforme a disponibilidade e a qualidade das fontes.
5. Examinar diferenças municipais e evolução temporal quando as definições forem comparáveis.
6. Projetar cinco páginas interativas no Power BI e apresentar achados com ressalvas metodológicas.
7. Sugerir hipóteses de intervenção e medidas de acompanhamento, sem antecipar conclusões causais.

## 1.5. Escopo e público-alvo

O foco principal é o **ensino médio da rede estadual da Paraíba**. Outras redes públicas podem ser apresentadas como contexto comparativo somente quando a base oferecer variável de dependência administrativa e a comparação for apropriada.

O público-alvo é a gestão estadual; o painel deve privilegiar indicadores relevantes para tomada de decisão, e não apenas visualizações descritivas.

# 2. Metodologia — D.E.I.L.A.S.

| Etapa | Aplicação ao projeto | Evidência ou entrega prevista |
|---|---|---|
| **D — Definir objetivos** | Delimitar a qualidade do ensino público, a questão de pesquisa e o recorte da rede estadual. | Problema, objetivos, público e perguntas norteadoras. |
| **E — Escolher métricas** | Selecionar medidas de aprendizagem, rendimento, participação, infraestrutura e desigualdade territorial. | Dicionário de indicadores e denominadores. |
| **I — Identificar fontes** | Catalogar microdados, dicionários oficiais, anos, cobertura, granularidade e chaves. | Inventários e documentação de origem dos datasets. |
| **L — Limpar os dados** | Corrigir tipos, conservar ausências, padronizar categorias, verificar faixas e auditar duplicidades. | Scripts, testes e relatórios de qualidade. |
| **A — Analisar os dados** | Explorar distribuições, diferenças entre grupos e localidades e comparações válidas por ano. | Notebooks, gráficos e dashboards. |
| **S — Sugerir soluções** | Traduzir achados em ações a avaliar, com critérios claros e medidas de acompanhamento. | Relatório executivo e hipóteses de políticas públicas. |

A implementação ocorre iterativamente: novas fontes ou problemas de qualidade podem exigir retorno às etapas de identificação, limpeza e definição das métricas.

# 3. Tecnologias e arquitetura da solução

## 3.1. Tecnologias utilizadas e propostas

| Tecnologia | Papel no projeto | Situação |
|---|---|---|
| **Python e bibliotecas de dados** | Inspeção, transformação, indicadores, testes e geração de bases analíticas. | Scripts e fluxos de 2024 executados. |
| **Jupyter Notebook / Google Colab** | Exploração e reprodutibilidade acadêmica. | Notebook exploratório inicial disponível. |
| **Power BI Desktop** | Relatório definitivo com cinco páginas, segmentadores e medidas. | **Proposto; arquivo PBIX ainda não implementado.** |
| **Git e GitHub** | Versionamento, Issues, execução automatizada e publicação de documentação. | Utilizados no desenvolvimento. |

## 3.2. Fluxo de dados proposto

**INEP (fontes brutas)** → **Python (inspeção, filtragem, limpeza, validações)** → **tabelas analíticas com granularidade definida** → **Power BI (modelo semântico, medidas DAX, cinco páginas)** → **relatório executivo**.

Os ZIPs nacionais e recortes com informações individuais não devem ser publicados no repositório público. O GitHub armazena códigos, documentação, testes, indicadores agregados e versões que não exponham dados pessoais.

## 3.3. Modelo conceitual para o Power BI

A arquitetura proposta utiliza dimensões de **Ano**, **Município**, **Escola** e **Rede de ensino**, sempre que houver identificadores compatíveis. As tabelas de fatos não serão misturadas sem considerar sua granularidade:

- **Fato Censo / Escolas:** uma observação por escola e edição do Censo, contendo recursos e características da oferta.
- **Fato Matrículas / Rendimento:** quantidades ou taxas na unidade oficial correspondente (escola, rede, município e ano), conforme a fonte.
- **Fato ENEM:** resultados por prova e participante identificável apenas nos limites dos microdados públicos; para relacionamento com escolas, priorizar indicadores previamente agregados por escola e ano.
- **Fato IDEB:** indicador divulgado na unidade e edição oficiais, com valores ausentes distintos de zero.

Os relacionamentos devem ser testados quanto à unicidade das dimensões, cardinalidade, direção de filtros e risco de contagens duplicadas. Dimensões compartilhadas não autorizam somar indevidamente populações ou tratar indicadores de anos diferentes como equivalentes.

# 4. Fontes de dados e sua disponibilidade

| ID | Base | Conteúdo relevante | Ano(s) | Situação no projeto |
|---|---|---|---|---|
| F01 | **ENEM** | Notas, presença, escola quando informada e questionário, em arquivos específicos. | 2024 e 2025 | 2024 processado; estrutura 2025 inspecionada, mas resultados ainda não tratados. |
| F02 | **Censo Escolar** | Unidades escolares, rede, localização, matrículas e recursos escolares. | 2024 e 2025 | 2024 processado; 2025 requer adaptação à estrutura de múltiplas tabelas. |
| F03 | **IDEB — ensino médio** | Indicadores por escola e outros níveis oficiais de divulgação. | 2025 | Planilha escolar inspecionada e recortada para a Paraíba. |
| F04 | **Taxas de rendimento** | Aprovação, reprovação e abandono. | 2024/2025 | **Prevista; indicadores ainda não incorporados à base analítica.** |
| F05 | **SAEB** | Dados complementares sobre aprendizagem e contexto. | 2023, conforme escopo | **Complementar; ainda não integrado.** |

## 4.1. Links oficiais das bases efetivamente utilizadas

As bases são disponibilizadas pelo **Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (INEP)**. Os links abaixo permitem localizar a documentação e baixar os pacotes nacionais originais; os filtros para a Paraíba são realizados posteriormente em Python.

| Base e edição | Página oficial para consulta e dicionário | Arquivo utilizado no processamento |
|---|---|---|
| **ENEM 2024** | [Microdados ENEM — INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem) | [Baixar microdados ENEM 2024 (.zip)](https://download.inep.gov.br/microdados/microdados_enem_2024.zip) |
| **Censo Escolar 2024** | [Microdados Censo Escolar — INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar) | [Baixar microdados Censo Escolar 2024 (.zip)](https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2024.zip) |
| **IDEB 2025 — ensino médio, escolas** | [Resultados IDEB — INEP](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados) | [Baixar planilha escolar IDEB 2025 (.zip)](https://download.inep.gov.br/ideb/resultados/divulgacao_ensino_medio_escolas_2025.zip) |

Os três pacotes acima são os que fundamentam as contagens e as análises preliminares de 2024/2025 apresentadas neste documento. O tratamento dos registros e a rastreabilidade das fontes estão descritos no [repositório do projeto](https://github.com/psoaresvieira/projeto_inep).

## 4.2. Fontes disponíveis ou previstas para ampliação da análise

| Base e edição | Fonte oficial | Situação |
|---|---|---|
| **ENEM 2025** | [Página oficial](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem) · [Baixar microdados 2025 (.zip)](https://download.inep.gov.br/microdados/microdados_enem_2025.zip) | Pacote inspecionado; os resultados ainda requerem leitura compatível e validação. |
| **Censo Escolar 2025** | [Página oficial](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar) · [Baixar microdados 2025 (.zip)](https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2025_.zip) | Estrutura inspecionada; integração e análise ainda pendentes. |
| **Taxas de rendimento 2024/2025** | [Taxas de Rendimento Escolar — INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/taxas-de-rendimento-escolar) | Fonte identificada; taxas de aprovação, reprovação e abandono ainda não incorporadas ao projeto. |
| **SAEB 2023** | [Microdados SAEB — INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/saeb) | Fonte complementar ainda não integrada. |

**Importante:** um link disponível não significa que a base foi processada. Somente os dados efetivamente conferidos podem fundamentar gráficos, indicadores e conclusões. A documentação oficial de cada edição deve ser consultada para os critérios de recorte, variáveis e limitações.

A disponibilidade de um pacote não significa que seus registros já tenham sido analisados. Os dados de 2025 precisam passar por inspeção detalhada, adaptação e validação antes de qualquer comparação temporal.

# 5. Indicadores e métricas

## 5.1. Aprendizagem e participação — ENEM

| Indicador | Definição / regra de cálculo | Fonte |
|---|---|---|
| Nota média por área | Média das notas **válidas** em Linguagens, Humanas, Natureza, Matemática e Redação; informar quantidade de notas válidas (N). | ENEM |
| Mediana e dispersão | Mediana, quartis, distribuição e desvio-padrão das notas no recorte selecionado. | ENEM |
| Participação observada | Registros com presença válida, sempre com denominador explícito. | ENEM |
| Diferenças entre grupos | Comparações por variáveis disponíveis e compatíveis, sem vinculações individuais não demonstradas. | ENEM |
| Cobertura escolar | Percentual de registros de resultados com identificação escolar compatível com Censo no mesmo ano. | ENEM + Censo |

**Restrição identificada:** no ENEM 2024, os arquivos PARTICIPANTES e RESULTADOS não possuem uma chave individual comum validada no projeto. **Não realizar junção por posição, índice ou ordem das linhas** para atribuir renda, sexo ou respostas do questionário às notas.

## 5.2. Qualidade e contexto da rede pública

| Indicador | Definição / regra | Fonte |
|---|---|---|
| IDEB do ensino médio | Utilizar o **valor oficial divulgado** para escola, município ou rede, quando disponível. | IDEB |
| Média simples escolar de IDEB | Média não ponderada das escolas com nota válida, identificada como estatística descritiva; **não equivale ao IDEB oficial da rede**. | IDEB |
| Aprovação / reprovação / abandono | Taxas oficiais por ano e recorte, sem inferir valores a partir de contagens incompletas. | Rendimento (pendente) |
| Matrículas | Total de matrículas do ensino médio com recorte claro de rede, município e ano. | Censo |
| Infraestrutura | Percentual de escolas com recurso declarado; registrar **sim, não e não informado** separadamente. | Censo |
| Condições docentes | Indicadores adequados de formação e disponibilidade de professores quando a fonte permitir. | Censo (a desenvolver) |
| Desigualdade territorial | Distribuição dos indicadores por município e diferenças observadas, com análise de cobertura e denominadores. | Dados integrados |
| Qualidade e cobertura dos dados | Percentual de campos ausentes, escolas pareadas, notas disponíveis e indicadores suprimidos. | Pipeline |

As métricas finais e suas fórmulas, especialmente rendimento e formação docente, devem ser validadas nos dicionários oficiais antes da implementação em DAX.

# 6. Limpeza, integração e validação

## 6.1. Procedimentos de limpeza

1. Selecionar registros da Paraíba e, quando aplicável, da rede estadual, registrando filtros explícitos.
2. Manter arquivos brutos originais e scripts reproduzíveis.
3. Corrigir tipos, padronizar categorias e validar anos, códigos escolares e intervalos permitidos.
4. Preservar **ausência de informação** como diferente de **valor zero**.
5. Auditar valores inválidos, categorias não informadas, presença nas provas e duplicidade de escolas.
6. Comparar contagens antes e depois dos tratamentos e documentar exceções.

## 6.2. Integração escolar já validada para 2024

Foi implementado e executado um relacionamento candidato entre **CO_ESCOLA**, no arquivo de resultados do ENEM 2024, e **CO_ENTIDADE**, no Censo Escolar 2024, após filtros para a rede estadual e auditoria de cobertura.

- **497 escolas** distintas no recorte de resultados do ENEM 2024.
- **482 escolas** estaduais com ensino médio no recorte do Censo 2024.
- **456 escolas** presentes nas duas bases.
- **29.393 de 29.783** registros do ENEM com escola estadual identificada na Paraíba encontraram correspondência escolar no Censo (**98,69%**).
- **Nenhum código escolar duplicado** no recorte do Censo.

A base integrada de 2024 foi produzida com uma linha por escola do Censo, após agregação de indicadores do ENEM por escola. Trata-se de integração **escolar**, não da ligação de questionários socioeconômicos a notas individuais.

## 6.3. Integrações e comparações ainda previstas

As edições ENEM 2024 e 2025 poderão ser empilhadas **somente após harmonização de esquemas e definições**, para comparações entre edições, sem tentar identificar o mesmo participante entre anos.

O Censo Escolar 2025 exigirá adaptação à sua estrutura própria. IDEB, rendimento e SAEB deverão ser relacionados exclusivamente por chaves, períodos e níveis de agregação compatíveis. A comparação de Censo 2024 com IDEB 2025 deve ser explicitamente longitudinal, não um cruzamento de informações do mesmo período.

## 6.4. Critérios de qualidade obrigatórios

- Documentar origem, versão e dicionário das bases.
- Verificar chaves e cardinalidade antes de cada junção.
- Publicar notas e taxas com denominador e regras de exclusão.
- Evitar divulgar grupos pequenos quando houver risco de interpretação indevida ou reidentificação.
- Informar fonte, período e unidade de análise de cada visual.
- Não atribuir causalidade a associações descritivas.

# 7. Estrutura funcional do relatório Power BI — Cinco dashboards

**Solução proposta:** um único arquivo **.pbix** com cinco páginas interligadas, menu lateral, identidade visual consistente, filtros pertinentes e opção de detalhamento. **O relatório definitivo em Power BI ainda não foi produzido.**

## 7.1. Dashboard 1 — Visão Executiva

**Pergunta:** Como está a situação geral do ensino médio estadual da Paraíba?

**Componentes planejados:** cartões de escolas, matrículas e municípios; valor oficial e evolução do IDEB quando disponível; aprendizagem, aprovação e abandono após coleta das fontes; indicadores de infraestrutura e resumo de diferenças territoriais. Cada cartão deve indicar ano e população.

**Finalidade:** permitir que o governador identifique rapidamente questões que merecem aprofundamento nas outras páginas.

## 7.2. Dashboard 2 — Desempenho e Aprendizagem

**Pergunta:** Onde os indicadores de aprendizagem mostram maiores dificuldades?

**Componentes planejados:** distribuição das notas ENEM por área, mediana e quartis, quantidade de notas válidas, IDEB escolar ou oficialmente agregado, SAEB quando incorporado, comparação por município e evolução temporal somente quando válida.

**Cuidados:** não extrapolar o ENEM para toda a rede; não comparar notas de provas como se tivessem escalas idênticas; não usar questionário socioeconômico sem chave individual validada.

## 7.3. Dashboard 3 — Infraestrutura e Condições de Ensino

**Pergunta:** Quais recursos estão disponíveis nas escolas estaduais e onde aparecem as maiores necessidades?

**Componentes planejados:** internet, banda larga, biblioteca, laboratório de ciências, laboratório de informática, quadra, infraestrutura de água e, se viável, indicadores docentes. Filtros por município e rede conforme a fonte.

**Finalidade:** comparar recursos declarados, identificar lacunas e apoiar diagnóstico de necessidades de investimento; a presença do recurso não demonstra sua qualidade ou efeito sobre notas.

## 7.4. Dashboard 4 — Desigualdades Territoriais

**Pergunta:** Como a oferta, a infraestrutura e os resultados se distribuem entre os municípios?

**Componentes planejados:** mapa com códigos IBGE e limites geográficos corretos; tabela pesquisável; comparações de infraestrutura, matrículas e resultados divulgados; detalhamento por município; visualização de dados ausentes.

**Situação atual:** indicadores municipais agregados de Censo 2024 e IDEB 2025 já foram calculados e validados, apresentados separadamente por ano. O mapa geográfico e a página correspondente no Power BI ainda serão implementados.

## 7.5. Dashboard 5 — Prioridades e Recomendações Governamentais

**Pergunta:** Quais necessidades e propostas de intervenção merecem avaliação primeiro?

**Componentes planejados:** matriz de problemas e hipóteses de ação, indicadores territoriais, população potencialmente beneficiada, confiança/cobertura dos dados, possibilidade de acompanhamento e critérios transparentes de priorização.

**Cuidados:** a pontuação ou o ranking de municípios **não será produzido automaticamente** a partir de pesos arbitrários. Critérios, limites e eventual ponderação deverão ser fundamentados e revisados pelo grupo, considerando evidências, contexto e viabilidade.

## 7.6. Experiência de navegação e design

A proposta visual utiliza azul-marinho, verde-petróleo e fundos claros; cards de KPI com unidades e anos visíveis; gráficos legíveis; tabelas acessíveis; menu de navegação das cinco páginas; segmentadores sincronizados quando apropriado.

A implementação em Power BI poderá usar indicadores DAX, filtros, drillthrough e tooltips. A escolha final de elementos dependerá de consistência dos dados, clareza para gestores e desempenho do relatório.

# 8. Regras de negócio do dashboard

| Código | Regra |
|---|---|
| **RN01 — Recorte territorial** | Paraíba como recorte principal; municípios mediante identificadores válidos. |
| **RN02 — Rede de ensino** | Priorizar rede estadual e distinguir outras redes quando a fonte permitir. |
| **RN03 — Filtros** | Filtros de ano, município, rede e área do conhecimento somente onde forem semanticamente aplicáveis. |
| **RN04 — Integridade** | Não transformar ausentes em zero; informar presença, exclusões e denominadores. |
| **RN05 — Série temporal** | Distinguir anos e avisar quando definições ou populações não forem comparáveis. |
| **RN06 — Fonte e atualização** | Cada indicador deve informar fonte, ano, unidade de medida e data da última carga. |
| **RN07 — Privacidade** | Não divulgar identificação individual; aplicar supressão e revisão quando necessário. |
| **RN08 — Recomendações** | Tratar propostas como hipóteses, com justificativa, público beneficiado e critério de avaliação. |
| **RN09 — Exportação** | Permitir exportar visões agregadas e resumos quando o recurso e as permissões forem adequados. |
| **RN10 — Organização visual** | O relatório Power BI deverá conter cinco páginas temáticas, sem redundância excessiva. |
| **RN11 — Navegação** | Disponibilizar navegação entre páginas e contexto dos filtros utilizados. |
| **RN12 — Granularidade** | Não somar linhas de participantes, escolas ou matrículas como se representassem a mesma unidade. |
| **RN13 — Priorização transparente** | Documentar critérios e eventuais ponderações; não criar rankings sem validação. |
| **RN14 — Acessibilidade** | Priorizar contraste, rótulos legíveis, navegação compreensível e texto alternativo quando possível. |
| **RN15 — Governança** | Separar indicadores concluídos, preliminares e planejados; permitir rastrear dados e transformações. |

# 9. Análise exploratória — Resultados preliminares verificados

Os valores abaixo correspondem aos recortes efetivamente processados até esta revisão. São **estatísticas descritivas**, não estimativas causais nem evidências de representatividade integral da rede quando derivadas do ENEM.

## 9.1. Oferta do ensino médio estadual — Censo Escolar 2024

| Indicador | Resultado |
|---|---:|
| Escolas estaduais com ensino médio na Paraíba | **482** |
| Municípios atendidos | **223** |
| Matrículas de ensino médio declaradas | **116.779** |
| Escolas com internet declarada | **459** |
| Escolas com biblioteca declarada | **358** |
| Escolas com laboratório de informática declarado | **284** |
| Escolas com laboratório de ciências declarado | **233** |
| Escolas com quadra de esportes declarada | **248** |
| Escolas com banda larga declarada | **139** |

A diferença entre presença de internet e de banda larga justifica uma investigação de conectividade; não demonstra, por si só, deficiência de qualidade ou impacto pedagógico.

## 9.2. ENEM 2024 — Participantes com escola estadual da PB identificada

**29.783 registros** atendem ao recorte escolar estadual. As médias abaixo utilizam apenas notas válidas, com denominadores específicos:

| Área | Notas válidas | Média descritiva |
|---|---:|---:|
| Ciências da Natureza | 21.786 | 456,53 |
| Ciências Humanas | 22.487 | 467,67 |
| Linguagens | 22.487 | 489,85 |
| Matemática | 21.786 | 476,81 |
| Redação | 22.487 | 571,92 |

O número de participantes com **local de prova** na Paraíba é um recorte distinto. Não se deve confundir local de prova, escola e residência, ou concluir que as médias acima representam todos os estudantes estaduais.

## 9.3. IDEB 2025 — Planilha de escolas estaduais

| Indicador | Resultado |
|---|---:|
| Escolas estaduais da PB presentes na planilha | **478** |
| Escolas com IDEB 2025 numérico válido | **458** |
| Escolas sem nota numérica válida | **20** |
| Média aritmética simples das 458 escolas com nota | **4,267** |
| Mediana entre escolas com nota | **4,3** |

A média aritmética simples **não é** o IDEB oficial agregado da rede estadual.

## 9.4. Análise territorial e preparação do Power BI

Foram calculados indicadores agregados por município, incluindo escolas, matrículas e infraestrutura do Censo Escolar 2024 e resultados do IDEB 2025, apresentados separadamente por ano. Também foram elaborados gráficos, um notebook de análise exploratória, relatórios de qualidade e uma auditoria da integração escolar.

Esses resultados constituem **insumos validados para a construção do relatório Power BI com cinco páginas**. A modelagem semântica, as medidas DAX e o arquivo **.pbix** final permanecem como entregas de desenvolvimento.

# 10. Propostas de decisão e critérios de priorização

As ações abaixo representam **hipóteses para investigação**. Nenhuma deve ser tratada como necessária antes de verificar dados, contexto local, capacidade administrativa, recursos disponíveis e alternativas de política pública.

| Hipótese de achado | Possível resposta de gestão | Indicador de acompanhamento |
|---|---|---|
| Dificuldades de aprendizagem em Matemática | Avaliação diagnóstica e reforço focalizado. | Resultados posteriores em avaliações comparáveis. |
| Disparidades territoriais persistentes | Apoio pedagógico territorialmente orientado. | Evolução de indicadores comparáveis por município/rede. |
| Abandono ou reprovação elevados | Busca ativa, apoio à permanência e acompanhamento da trajetória escolar. | Taxas oficiais de rendimento no período seguinte. |
| Recursos pedagógicos ausentes | Diagnóstico de infraestrutura, manutenção e investimento planejado. | Cobertura, uso e funcionamento dos recursos. |
| Conectividade declarada insuficiente | Avaliar qualidade do acesso e necessidades de contratação/equipamentos. | Disponibilidade e qualidade efetiva de conexão. |

## 10.1. Como propor prioridades sem inventar rankings

A página de Prioridades Governamentais pode organizar os municípios ou escolas a partir dos seguintes critérios **a validar**: aprendizagem e fluxo escolar, desigualdade territorial, condições de oferta, número potencial de estudantes afetados, qualidade dos dados, viabilidade de intervenção e possibilidade de monitoramento.

A eventual combinação em uma pontuação deverá documentar critérios, normalização, pesos, limitações e análise de sensibilidade, além de ser revisada com a equipe. **Até isso acontecer, o dashboard deve mostrar diagnósticos e necessidades observadas, não uma classificação definitiva de municípios.**

# 11. Entregáveis e andamento do projeto

| Entregável | Situação em 12/11/2026 |
|---|---|
| Datasets brutos preservados e documentados, com volume compatível com a disciplina | **2024: realizado.** 2025: inspeção estrutural realizada, processamento pendente. |
| Scripts e testes de filtragem, limpeza e integração | **Realizados e executados para ENEM/Censo 2024.** |
| Auditoria de chaves e relatórios de qualidade | **Publicados para 2024.** |
| Notebooks e relatório exploratório | **Versões preliminares disponíveis.** |
| Relatório Power BI com cinco páginas | **Planejado; ainda não construído.** |
| Inclusão de rendimento, SAEB e indicadores docentes | **Planejada ou complementar, conforme viabilidade.** |
| Comparações validadas entre 2024 e 2025 | **Pendentes.** |
| Relatório executivo final com recomendações avaliáveis | **Pendente de análises complementares.** |

## 11.1. Próximas atividades prioritárias

1. Resolver a leitura do arquivo de resultados ENEM 2025 e validar suas variáveis.
2. Adaptar os scripts ao formato do Censo Escolar 2025 e produzir indicadores comparáveis.
3. Obter taxas oficiais de aprovação, reprovação e abandono, confirmando seus níveis de divulgação.
4. Construir tabelas analíticas para o Power BI com chaves e granularidade auditadas.
5. Implementar as cinco páginas no Power BI, com navegação e visual coerentes.
6. Aprofundar a análise estatística, apresentar limitações e revisar hipóteses de intervenção.
7. Finalizar relatório acadêmico, apresentação ao governador e estratégia de disponibilização.

# 12. Limitações, transparência e disponibilização

- **Representatividade:** o ENEM não cobre necessariamente todos os estudantes da rede estadual.
- **Comparabilidade:** fontes e anos distintos exigem análise de equivalência antes de inferir evolução.
- **Identificação:** participantes e resultados do ENEM 2024 não foram associados individualmente por ausência de chave comum validada.
- **IDEB:** uma média simples de notas escolares não substitui indicador oficial agregado.
- **Causalidade:** a observação de diferentes resultados e recursos escolares não demonstra efeitos de políticas.
- **Privacidade:** microdados pessoais e agrupamentos pequenos exigem proteção e avaliação antes de divulgação.
- **Entregas:** análises, indicadores e documentação estão disponíveis; o arquivo final do Power BI ainda precisa ser desenvolvido e revisado.

**Publicação do Power BI:** não há, nesta revisão, arquivo PBIX finalizado nem relatório publicado no Power BI Service. A disponibilização será definida após a conclusão das cinco páginas e a validação dos indicadores.

**Repositório do projeto:** https://github.com/psoaresvieira/projeto_inep

---

## Referências e rastreabilidade

- [INEP — Microdados do ENEM (2024 e 2025)](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)
- [INEP — Microdados do Censo Escolar (2024 e 2025)](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar)
- [INEP — Resultados oficiais IDEB 2025](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb/resultados)
- [INEP — Taxas de Rendimento Escolar](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/taxas-de-rendimento-escolar)
- [INEP — Microdados do SAEB](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/saeb)
- Relatórios técnicos do projeto: https://github.com/psoaresvieira/projeto_inep/tree/main/reports
- Código e testes: https://github.com/psoaresvieira/projeto_inep/tree/main/src
- Documentação metodológica: https://github.com/psoaresvieira/projeto_inep/tree/main/docs

**Nota editorial:** esta versão foi atualizada a partir do documento original de seis páginas, preservando seus objetivos, fontes, metodologia, regras de negócio, indicadores, estratégia de integração e propostas de decisão; os acréscimos explicitam a estrutura de cinco dashboards, o Power BI e o progresso real reportado do projeto.
