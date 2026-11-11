# Resultados preliminares — Diagnóstico do Ensino Médio Público da Paraíba

**Atualização:** 11/11/2026. **Status:** análise descritiva inicial; sujeita a verificação dos dicionários e do escopo amostral.

## 1. Fontes e recortes

Este relatório reúne os resultados de processamento dos arquivos oficiais publicados no projeto, utilizando **ENEM 2024** e **Censo Escolar 2024**.

- [Perfil agregado do ENEM e do Censo](../reports/inspecao/perfil_paraiba.md).
- [Recorte específico do Censo Escolar PB](../reports/inspecao/censo_pb_2024.md).
- [Inventário da estrutura dos pacotes](../reports/inspecao/inventario.md).

A leitura do IDEB 2025 foi validada; a correspondência entre identificadores escolares nas diferentes bases permanece em avaliação.

## 2. Censo Escolar 2024

| Indicador | Valor |
|---|---:|
| Registros de escolas no Brasil | 215.545 |
| Escolas com registro na Paraíba | 5.325 |
| Escolas estaduais da Paraíba | 667 |
| Escolas estaduais com oferta de ensino médio | 482 |
| Municípios com escolas estaduais de ensino médio | 223 |
| Matrículas de ensino médio declaradas nas escolas selecionadas | 116.779 |
| Códigos repetidos de escola no recorte selecionado | 0 |

### Recursos de infraestrutura (482 escolas do recorte)

| Variável | Presença (1) | Ausência (0) | Campo vazio |
|---|---:|---:|---:|
| Internet (`IN_INTERNET`) | 459 | 23 | 0 |
| Banda larga (`IN_BANDA_LARGA`) | 139 | 320 | 23 |
| Biblioteca (`IN_BIBLIOTECA`) | 358 | 124 | 0 |
| Sala de leitura (`IN_SALA_LEITURA`) | 38 | 444 | 0 |
| Laboratório de ciências (`IN_LABORATORIO_CIENCIAS`) | 233 | 249 | 0 |
| Laboratório de informática (`IN_LABORATORIO_INFORMATICA`) | 284 | 198 | 0 |
| Quadra de esportes (`IN_QUADRA_ESPORTES`) | 248 | 234 | 0 |

**Interpretação cautelosa:** há diferenças relevantes de infraestrutura declarada entre as escolas selecionadas, que podem orientar um diagnóstico de necessidades. Isso não demonstra, por si só, impacto causal sobre o desempenho dos estudantes.

## 3. ENEM 2024

| Indicador | Valor |
|---|---:|
| Registros nacionais de participantes/resultados | 4.332.944 |
| Registros com local de prova na Paraíba | 128.546 |
| Registros com escola na Paraíba (resultados) | 37.251 |
| Registros com escola estadual na Paraíba (resultados) | 29.783 |
| Códigos de escola distintos na Paraíba (resultados) | 696 |

**Não confundir as populações:** local da prova na Paraíba, escola identificada na Paraíba e escola estadual na Paraíba são critérios distintos.

### Médias entre registros com escola estadual identificada na PB e nota válida

| Área | Notas válidas | Média |
|---|---:|---:|
| Ciências da Natureza | 21.786 | 456,53 |
| Ciências Humanas | 22.487 | 467,67 |
| Linguagens | 22.487 | 489,85 |
| Matemática | 21.786 | 476,81 |
| Redação | 22.487 | 571,92 |

Esses resultados são descrições dos participantes analisáveis, **não do conjunto integral de estudantes da rede estadual**. A presença na prova e a composição dos participantes afetam diretamente os denominadores. As médias de diferentes provas não devem ser comparadas como se medissem competências em escala idêntica.

## 4. IDEB 2025 — Escolas da Paraíba

A planilha oficial de resultados por escola apresenta **529 escolas da PB** (todas as redes) e **478 escolas estaduais** (todas com código distinto). Dessas escolas estaduais, **458 possuem IDEB 2025 com valor numérico válido** na coluna técnica `VL_OBSERVADO_2025`, e **20 não possuem nota válida**.

Estatísticas **somente das 458 escolas com nota**:

| Métrica | Valor |
|---|---:|
| Média simples não ponderada | 4,267 |
| Mediana | 4,3 |
| Mínimo | 2,7 |
| Máximo | 5,8 |

A média simples calculada por escola não representa o IDEB oficial agregado da rede. Também não se deve presumir correspondência 1:1 entre a população do IDEB 2025 e a do Censo 2024.

Fonte e método: [Perfil IDEB 2025 — escolas PB](../reports/inspecao/ideb_pb_2025.md).

## 5. Limitação importante da integração

No inventário, o arquivo de participantes do ENEM possui `NU_INSCRICAO`, enquanto o arquivo de resultados utiliza `NU_SEQUENCIAL`. Não foi demonstrada chave individual comum, e `NU_SEQUENCIAL` também não corresponde à posição do registro no arquivo (4.332.944 divergências na verificação).

**Não unir essas tabelas por ordem ou índice.** O questionário socioeconômico poderá ser analisado separadamente até que uma chave oficial válida seja identificada.

A junção de `CO_ESCOLA` (ENEM resultados) com `CO_ENTIDADE` (Censo) é apenas candidata, dependendo de correspondência e de cardinalidade; ainda não foi executada.

## 6. Hipóteses a investigar, não conclusões

1. Distribuição territorial e níveis de acesso a recursos de infraestrutura escolar.
2. Relação descritiva entre infraestrutura e resultados educacionais, **apenas após integração validada por escola e período**.
3. Presença e ausência no ENEM por grupo de participantes, sem extrapolar para a rede completa.
4. Diferenças entre escolas ou grupos em indicadores de aprendizagem/fluxo com IDEB e SAEB.

## 7. Próximas verificações

- [ ] Conferir as definições e códigos das variáveis nos dicionários de 2024.
- [x] Completar o recorte agregado do IDEB 2025, preservando os registros sem nota válida.
- [ ] Medir a correspondência `CO_ESCOLA` ↔ `CO_ENTIDADE` e perdas na junção, respeitando unidade e ano.
- [ ] Coletar e harmonizar dados de 2025 quando disponíveis para as séries comparativas.
- [ ] Verificar quais métricas são adequadas para recomendações de políticas públicas.

## Fontes

- [Microdados ENEM — INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem).
- [Microdados Censo Escolar — INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar).
- [Resultados do IDEB — INEP](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb).
