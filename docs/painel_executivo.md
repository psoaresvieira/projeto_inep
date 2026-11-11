# Painel executivo — educação estadual da Paraíba

**Status:** versão preliminar reproduzível, com painel geral e visão municipal validados em 11/11/2026.  
**Formato:** HTML/CSS/JavaScript estático, sem conexão externa, construído somente com indicadores agregados validados.

## Como acessar

Painel geral: [dashboard/index.html](../dashboard/index.html).  
**Painel por município:** [dashboard/municipios.html](../dashboard/municipios.html).

Para **visualizar como página**, clone ou baixe o repositório e abra o arquivo `dashboard/index.html` no navegador. O GitHub normalmente mostra o conteúdo ou o arquivo, mas esta versão não foi publicada em um endereço GitHub Pages.

Para **regerar o painel geral** a partir dos relatórios agregados oficiais:

```bash
python src/06_dashboard_agregado.py
python -m unittest discover -s tests -v
```

A geração de gráficos SVG e relatório técnico da EDA:

```bash
python src/05_exploracao_preliminar.py
```

## Estrutura do painel

| Aba | Conteúdo | Ano |
|---|---|---|
| Panorama | Escolas estaduais, matrículas, municípios e cobertura do relacionamento escolar | 2024 |
| Infraestrutura | Presença/ausência/não informado para recursos físicos e digitais, com filtro interativo | 2024 |
| Aprendizagem | Médias ENEM e quantidades válidas por área; estatísticas descritivas do IDEB | ENEM 2024, IDEB 2025 |
| Metodologia | Fontes, recortes, restrições de interpretação e links de auditoria | 2024–2025 |

O painel é **interativo apenas na navegação entre abas e no filtro de indicadores de infraestrutura**. Não possui filtros por município ou escola nesta primeira versão, porque o arquivo público é baseado somente em estatísticas agregadas. Isso impede apresentar análises escolares fictícias ou vazar microdados.

## Proteção de dados e validade

- Não exibe linhas individuais do ENEM, registros de questionários ou combinações que permitam inferir identidades.
- A média do IDEB 2025 é a **média simples das escolas com nota numérica válida**, não o IDEB oficial agregado da rede estadual.
- O ENEM inclui somente o grupo com escola estadual identificada; não representa toda a matrícula estadual.
- O dashboard **não cruza** os questionários individuais do ENEM com as notas, porque não foi identificada chave comum autorizada.
- O relacionamento entre ENEM resultados e Censo usa códigos escolares auditados referentes a 2024.
- O Censo 2024 e o IDEB 2025 referem-se a períodos distintos.
- Estatísticas descritivas não permitem afirmar causalidade.

## Fontes técnicas

- [Perfil agregado ENEM e Censo 2024](../reports/inspecao/perfil_paraiba.md)
- [Perfil IDEB 2025](../reports/inspecao/ideb_pb_2025.md)
- [Auditoria ENEM–Censo](../reports/filtragem/validacao_chaves_2024.md)
- [Análise exploratória preliminar](../reports/analise_exploratoria/analise_preliminar.md)
- [Código gerador](../src/06_dashboard_agregado.py)
- [Testes automáticos](../tests/test_dashboard_agregado.py)

## Próximas melhorias

1. Atualizar as fontes e as visualizações após inspeção de ENEM 2025 e Censo Escolar 2025.
2. Criar análises por município a partir da base escolar limpa, com denominadores válidos.
3. Revisar supressão de grupos muito pequenos e riscos de reidentificação antes da divulgação de indicadores no nível da escola.
4. Discutir com o grupo quais decisões do Governo do Estado o painel deve apoiar antes de considerar o dashboard finalizado.


## Visão territorial (entrega adicional)

A [página municipal](../dashboard/municipios.html) foi gerada a partir dos dados oficiais, após validar os totais estaduais e os códigos de município. Ela inclui busca por nome/código IBGE, ordenação e seleção de municípios, indicadores de infraestrutura (Censo 2024) e média simples de IDEB por escola (2025) somente quando houver pelo menos três notas válidas.

- [Indicadores municipais agregados](../reports/municipios/municipios_agregados.json)
- [Metodologia e totais](../reports/municipios/resumo_municipios.md)
- [Código de produção dos agregados](../src/05_indicadores_municipais.py)
- [Gerador da página](../src/06_dashboard_municipios.py)

O agrupamento é por código do município, sem unir escolas de 2024 às de 2025. A média simples do IDEB não representa a nota oficial agregada da rede.

Para reproduzir a página a partir do arquivo JSON publicado:

```bash
python src/06_dashboard_municipios.py
```
