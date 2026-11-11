# Projeto INEP — Diagnóstico da Educação Pública da Paraíba

Projeto acadêmico de Análise de Dados, voltado à qualidade do ensino médio público da Paraíba. O objetivo é produzir indicadores, análises exploratórias e propostas baseadas em evidências para apresentação simulada ao Governo Estadual.

## Metodologia

Framework **D.E.I.L.A.S.**: Definir objetivos, Escolher métricas, Identificar fontes, Limpar dados, Analisar e Sugerir decisões.

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
- IDEB 2025: **478 escolas estaduais** identificadas na planilha de ensino médio. A extração correta da nota de 2025 ainda está em validação.

Relatórios: [Resultados preliminares](docs/resultados_preliminares.md), [Censo PB 2024](reports/inspecao/censo_pb_2024.md) e [Perfil ENEM e Censo](reports/inspecao/perfil_paraiba.md).

Código e documentação de filtragem: [script](src/02_filtragem.py) e [critérios](docs/estrategia_filtragem.md). Os testes sintéticos dos filtros passaram no GitHub Actions.

**Estado atual:** Issue #1 com contagens nacionais e estaduais processadas; a validação de dicionários e relacionamentos ainda está aberta. Issue #2 com script e testes preparados, mas filtragem real ainda não concluída.

**Segurança:** os arquivos brutos, recortes individuais e resultados intermediários estão excluídos do versionamento. Não foram executadas junções por posição dos registros ENEM.
