# Projeto INEP — Diagnóstico da Educação Pública da Paraíba

Projeto acadêmico de Análise de Dados, voltado à qualidade do ensino médio público da Paraíba. O objetivo é produzir indicadores, análises exploratórias e propostas baseadas em evidências para apresentação simulada ao Governo Estadual.

## Metodologia

Framework **D.E.I.L.A.S.**: Definir objetivos, Escolher métricas, Identificar fontes, Limpar dados, Analisar e Sugerir decisões.

A [documentação metodológica D.E.I.L.A.S.](docs/metodologia_DEILAS.md) registra objetivos, métricas, fontes, métodos, resultados verificados e propostas preliminares.

O desenvolvimento está dividido em seis [Issues](../../issues):
1. Inspeção e catalogação dos datasets;
2. Filtragem da Paraíba e seleção de variáveis;
3. Limpeza e padronização;
4. Integração dos datasets;
5. Análise exploratória;
6. Documentação e recomendações.

## Bases de dados

- ENEM 2024 e 2025;
- Censo Escolar 2024 e 2025;
- IDEB 2025;
- Indicadores de rendimento escolar e SAEB (complementares, conforme viabilidade).

A procedência, o status de recebimento e as lacunas são apresentados em [docs/inventario_datasets.md](docs/inventario_datasets.md).

## Como iniciar a inspeção

É necessário **Python 3.10+**. Clone o projeto, crie uma pasta `dados_brutos/` e coloque nela os arquivos ZIP baixados do INEP. A pasta é ignorada pelo Git.

```bash
python -m pip install -r requirements.txt
python src/01_inspecao.py --pasta dados_brutos
```

Serão gerados `reports/inspecao/inventario.md` e `reports/inspecao/inventario.json`. Este comando inspeciona arquivos e cabeçalhos; para contar registros, execute `python src/01_perfil_paraiba.py`, que gera o perfil agregado do ENEM e Censo. Para gerar recortes locais da Paraíba, utilize `python src/02_filtragem.py`.

Antes de interpretar os resultados é indispensável verificar os dicionários oficiais, especialmente UF, dependência administrativa, unidades de observação, situação de presença no ENEM e granularidade de escola/município.

## Boas práticas

- Preservar os arquivos brutos originais sem modificá-los;
- Não publicar microdados ou arquivos grandes no GitHub;
- Documentar cada filtro, ausência, junção e sua justificativa;
- Não equiparar notas do ENEM à qualidade de toda a rede pública nem inferir causalidade sem evidência.

## Primeiras evidências verificadas (2024)

- Censo Escolar: **5.325 escolas da PB**, das quais **482 estaduais com oferta de ensino médio** e **116.779 matrículas** declaradas nesse recorte.
- ENEM: **29.783 registros de participantes com escola estadual identificada na PB**; o total de participantes que fizeram a prova no estado (**128.546**) pertence a outro critério.
- IDEB 2025: **478 escolas estaduais** identificadas, das quais **458 possuem nota válida** na coluna `VL_OBSERVADO_2025`; média simples por escola com nota **4,267** (não é o IDEB oficial da rede).

Relatórios: [Resultados preliminares](docs/resultados_preliminares.md), [Censo PB 2024](reports/inspecao/censo_pb_2024.md) e [Perfil ENEM e Censo](reports/inspecao/perfil_paraiba.md).

Código e documentação de filtragem: [script](src/02_filtragem.py) e [critérios](docs/estrategia_filtragem.md). Os testes sintéticos dos filtros passaram no GitHub Actions. O fluxo de filtragem completa de 2024 está registrado na [Issue #2](../../issues/2); só serão publicados relatórios agregados.

**Estado atual:** o [pipeline oficial PB 2024](.github/workflows/pipeline-pb-2024.yml) foi executado com sucesso, incluindo filtragem, auditoria de chaves, limpeza conservadora e integração escolar. Das 482 escolas do Censo, 456 possuem correspondência com o ENEM e 29.393 registros do ENEM foram pareados (98,69% dos registros selecionados). Ver [relatório de filtragem](reports/filtragem/resumo_2024.md), [auditoria das chaves](reports/filtragem/validacao_chaves_2024.md), [qualidade](reports/qualidade/qualidade_2024.md) e [integração](reports/integracao/integracao_2024.md).

A [análise exploratória preliminar](reports/analise_exploratoria/analise_preliminar.md) já gera [gráficos](reports/figuras/) e pode ser reproduzida pelo [notebook acadêmico](notebooks/05_analise_exploratoria.ipynb). Não inclui microdados individuais versionados.

O [painel executivo HTML](dashboard/index.html) foi gerado e testado a partir de indicadores agregados. Para visualizar a interface, baixe o projeto e abra `dashboard/index.html` no navegador, conforme [instruções](docs/painel_executivo.md). Ainda não foi publicado como site.

**Bases de 2025:** confirmadas nas [páginas oficiais do INEP](docs/fontes_2025.md), com [fluxo de inspeção estrutural](.github/workflows/inspecao-2025.yml) iniciado. Os esquemas e campos de 2025 não devem ser presumidos iguais aos de 2024. As seis Issues permanecem abertas enquanto houver validações, análises e entregáveis finais pendentes.

**Segurança:** os arquivos brutos, recortes individuais e resultados intermediários estão excluídos do versionamento. Não foram executadas junções por posição dos registros ENEM.
