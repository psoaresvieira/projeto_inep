# Critérios de validação e integração — Projeto ENEM Paraíba

**Status:** critérios metodológicos propostos antes do tratamento; serão revisados após a leitura integral dos microdados.  
**Objetivo:** estudar a qualidade do ensino médio público da Paraíba sem confundir população, unidade de observação ou ano de referência.

## Bases e granularidade

| Base | Unidade prevista | Variáveis observadas no inventário | Recorte preliminar |
|---|---|---|---|
| ENEM 2024 — PARTICIPANTES | inscrição/participante | `NU_INSCRICAO`, `SG_UF_PROVA`, `Q001`, `Q002`, `Q007` | `SG_UF_PROVA=PB` apenas para análise de **local de prova**, não de escola |
| ENEM 2024 — RESULTADOS | linha de resultado | `NU_SEQUENCIAL`, `CO_ESCOLA`, `SG_UF_ESC`, `TP_DEPENDENCIA_ADM_ESC`, notas | `SG_UF_ESC=PB` e `TP_DEPENDENCIA_ADM_ESC=2` para participantes com escola estadual identificada |
| Censo Escolar 2024 | escola | `CO_ENTIDADE`, `SG_UF`, `TP_DEPENDENCIA`, `IN_MED`, `QT_MAT_MED` | `SG_UF=PB`, `TP_DEPENDENCIA=2`, com oferta de ensino médio |
| IDEB 2025 — escolas | escola/período, conforme planilha | planilha com títulos e cabeçalhos múltiplos; códigos ainda não validados | identificar UF, escola e ano após leitura dos cabeçalhos |

Esses recortes **não** representam todos os estudantes da Paraíba. Os dados ENEM são voluntários e os campos escolares possuem cobertura limitada.

## Regra crítica: participantes versus resultados

**Não executar um vínculo individual entre `PARTICIPANTES_2024.csv` e `RESULTADOS_2024.csv` pela posição das linhas.**

As colunas inspecionadas evidenciam chaves diferentes: `NU_INSCRICAO` e `NU_SEQUENCIAL`. Não existe chave comum individual demonstrada. O dicionário do INEP deve prevalecer sobre hipóteses de relacionamento por posição; não imputar renda, sexo ou perfil socioeconômico aos registros de notas sem uma chave autorizada e validada.

Análises de desempenho e análises do questionário podem ser feitas **separadamente**.

## Relacionamentos candidatos (sujeitos a validação)

1. ENEM resultados 2024 `CO_ESCOLA` → Censo 2024 `CO_ENTIDADE`. Verificar tipo e preenchimento, escola única por ano e quais registros ENEM ficam sem par.
2. Censo 2025 → IDEB 2025 por escola/rede/município, **depois da coleta do Censo 2025 e confirmação dos códigos e níveis da planilha**.
3. Comparações ENEM 2024 ↔ ENEM 2025 com harmonização de esquemas, análise entre **grupos e anos**, sem tentar vincular os mesmos indivíduos.
4. Nunca integrar apenas pelo nome da escola, município da prova, nomes de pessoas ou correspondência posicional.

## Testes de qualidade requeridos

- Quantidade exata de registros por fonte e edição.
- Integridade do ZIP e identificação dos arquivos de dados e dicionários.
- Percentual de códigos de escola não preenchidos por recorte.
- Duplicidade de `CO_ENTIDADE` dentro de uma mesma edição do Censo, quando cada linha representar uma escola.
- Cardinalidade do relacionamento (evitar junções muitos-para-muitos).
- Contagens antes/depois do `merge`; quantificação de registros sem correspondência.
- Campos de notas: valores ausentes e situações de presença, sem conversão automática de nulo para zero.
- Conferência dos códigos de dependência administrativa, ano, município, infraestrutura e oferta de ensino no dicionário.

## Indicadores possíveis, condicionados aos testes

- Número de escolas estaduais com oferta de ensino médio.
- Distribuição geográfica e matrículas declaradas dessas escolas.
- Infraestrutura escolar: internet, biblioteca, laboratório e quadra, conforme a codificação oficial.
- Resultados ENEM por área, **somente para participantes com escola estadual da PB identificada e nota válida**.
- Indicadores IDEB no nível escolar ou agregado, preservando as regras oficiais de divulgação.

## Cuidados para apresentação ao governador

- Não afirmar representatividade da rede estadual com base apenas nos participantes do ENEM.
- Não transformar diferenças descritivas em conclusões causais.
- Preferir recomendações de diagnóstico/avaliação e propostas sujeitas a viabilidade, evidência e recursos.
- Se houver poucos participantes por grupo/escola, evitar publicar grupos muito pequenos.
- Identificar a origem de cada indicador no dashboard.

## Fontes oficiais

- [Microdados ENEM — INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)
- [Microdados Censo Escolar — INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar)
- [IDEB — INEP](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb)

**As contagens reais, a cobertura dos códigos e os relacionamentos permanecem pendentes até o relatório de perfil da Paraíba ser produzido e validado.**
