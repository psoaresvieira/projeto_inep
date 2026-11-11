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

Serão gerados `reports/inspecao/inventario.md` e `reports/inspecao/inventario.json`. O programa lê membros e cabeçalhos por amostragem, sem extrair todos os arquivos. **Não conta ainda os registros completos nem executa a integração.**

Antes de interpretar os resultados é indispensável verificar os dicionários oficiais, especialmente UF, dependência administrativa, unidades de observação, situação de presença no ENEM e granularidade de escola/município.

## Boas práticas

- Preservar os arquivos brutos originais sem modificá-los;
- Não publicar microdados ou arquivos grandes no GitHub;
- Documentar cada filtro, ausência, junção e sua justificativa;
- Não equiparar notas do ENEM à qualidade de toda a rede pública nem inferir causalidade sem evidência.

**Estado atual:** Issue #1 em andamento; inspeção interna dos três ZIPs recebidos ainda pendente.
