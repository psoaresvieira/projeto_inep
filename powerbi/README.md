# Base de dados do Power BI — Projeto INEP / Paraíba

**Entrega atual:** tabelas CSV agregadas, produzidas a partir dos relatórios já validados para o recorte estadual da Paraíba. **Não existe um arquivo .pbix pronto**: estes arquivos servem para começar sua construção.

## Arquivos gerados

Execute `python src/07_exportar_powerbi.py` na raiz do repositório. Os arquivos são gravados em `powerbi/dados/` com **UTF-8, separador ponto e vírgula (;) e decimal vírgula**, apropriados à configuração regional brasileira.

| Arquivo | Unidade de análise | Ano | Finalidade |
|---|---|---|---|
| `dim_municipio.csv` | Município, chave IBGE | — | Filtro e relacionamento por município |
| `fato_censo_municipio_2024.csv` | Município | 2024 | Escolas e matrículas da rede estadual com ensino médio |
| `fato_infra_municipio_2024.csv` | Município **e tipo de recurso** | 2024 | Escolas com/sem infraestrutura, incluindo dados ausentes |
| `fato_ideb_municipio_2025.csv` | Município | 2025 | Quantidades de escolas e médias escolares simples quando publicáveis |
| `fato_enem_areas_2024.csv` | Área do conhecimento | 2024 | Médias de notas válidas no recorte de escola estadual identificada |
| `fato_cobertura_escolar_2024.csv` | Estado da Paraíba | 2024 | Correspondência escolar entre ENEM e Censo |
| `manifesto.json` | Metadados | — | Origem, limites e contagens das tabelas |

**Atenção:** não há microdados individuais, CPF, nome de aluno ou código de participante nos CSVs. O código IBGE de município é a chave `codigo_municipio`, que deve ser importada como **Texto**.

## Importar no Power BI Desktop

1. Abra o Power BI Desktop e selecione **Obter dados > Texto/CSV**, apontando para os seis arquivos CSV em `powerbi/dados/`.
2. Confira o **delimitador ponto e vírgula** e a codificação **UTF-8**.
3. Em **Transformar dados**, defina `codigo_municipio` como **Texto**, `ano` e contagens como **Número inteiro**, e as médias como **Número decimal** usando a localidade **Português (Brasil)** quando necessário.
4. Carregue os dados e abra **Exibição de modelo**.
5. Crie relacionamentos **1 para muitos (1:N)** de `dim_municipio[codigo_municipio]` para o mesmo campo das tabelas de Censo, infraestrutura e IDEB, todos com filtro em **direção única** a partir da dimensão. Não crie junções físicas diretas entre as tabelas de fatos de 2024 e 2025.
6. As tabelas de ENEM por área e cobertura estadual ficam **desconectadas da dimensão Município**, pois esses arquivos NÃO contêm dados desagregados por município.

## Medidas iniciais em DAX

As medidas abaixo podem ser criadas em **Modelagem > Nova medida**. O Power BI poderá usar separador `;` entre argumentos de funções, dependendo da configuração regional.

```dax
Escolas estaduais (2024) =
SUM(fato_censo_municipio_2024[escolas_ensino_medio])

Matrículas declaradas (2024) =
SUM(fato_censo_municipio_2024[matriculas_declaradas])

Escolas com internet (%) =
CALCULATE(
    DIVIDE(
        SUM(fato_infra_municipio_2024[escolas_sim]),
        SUM(fato_infra_municipio_2024[total_escolas])
    ),
    fato_infra_municipio_2024[codigo_recurso] = "IN_INTERNET"
)

IDEB médio simples de escolas (município selecionado) =
IF(
    HASONEVALUE(dim_municipio[codigo_municipio]),
    SELECTEDVALUE(fato_ideb_municipio_2025[media_simples_escolas]),
    BLANK()
)

Cobertura de registros ENEM pareados (%) =
DIVIDE(
    SUM(fato_cobertura_escolar_2024[registros_enem_pareados]),
    SUM(fato_cobertura_escolar_2024[registros_enem_com_codigo_escola])
)
```

Formate medidas de proporção como **Percentual**. Não use `AVERAGE` sobre médias municipais de IDEB ou médias por área do ENEM como se isso criasse o indicador oficial da rede.

## Organização inicial das cinco páginas

1. **Visão Executiva:** cartões com escolas, matrículas, municípios e cobertura da integração escolar; indicadores com ano visível.
2. **Desempenho e Aprendizagem:** visual do ENEM 2024 por área, quantidade de notas válidas e IDEB 2025 disponível por município, com avisos de amostra e período.
3. **Infraestrutura:** barras por recurso e classificação sim/não/sem informação; comparação municipal.
4. **Desigualdades Territoriais:** tabela por município, mapa com código IBGE devidamente configurado e recortes de infraestrutura/IDEB apresentados separadamente.
5. **Prioridades e Recomendações:** quadro descritivo de necessidades e possíveis intervenções; **sem ranking arbitrário**.

As páginas 2 e 5 serão ampliadas quando as taxas de aprovação/abandono, o SAEB ou mais edições estiverem adequadamente validadas.

## Limitações que devem acompanhar os dashboards

- **Censo 2024 vs. IDEB 2025:** anos e universos diferentes; apresentar cada indicador com seu período, sem afirmar que um explica o outro.
- **IDEB 2025:** `media_simples_escolas` é uma média simples dos IDEBs escolares do município, e **não** o IDEB oficial agregado da rede estadual ou do município.
- **Supressão:** médias/medianas de municípios com menos de três notas IDEB válidas permanecem **vazias**; não preencher nem calcular substitutas.
- **ENEM 2024:** não representa todos os alunos estaduais; o arquivo exportado não possui município e não deve receber filtro municipal.
- **Infraestrutura:** cada município tem sete registros (um por recurso). Para percentuais gerais de um recurso, some `escolas_sim` e `total_escolas` após filtrar o recurso; não some percentuais municipais nem trate todos os recursos como uma única variável.
- **Mapa:** o código IBGE é usado para identificar municípios, mas é preciso testar o reconhecimento geográfico ou vincular uma tabela de geometrias antes de publicar o mapa.

## Fontes e rastreabilidade

- ENEM 2024: https://download.inep.gov.br/microdados/microdados_enem_2024.zip
- Censo Escolar 2024: https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2024.zip
- IDEB 2025: https://download.inep.gov.br/ideb/resultados/divulgacao_ensino_medio_escolas_2025.zip
- Relatório territorial: [reports/municipios/resumo_municipios.md](../reports/municipios/resumo_municipios.md)
- Perfil ENEM/Censo: [reports/inspecao/perfil_paraiba.md](../reports/inspecao/perfil_paraiba.md)
- Auditoria da integração escolar: [reports/filtragem/validacao_chaves_2024.md](../reports/filtragem/validacao_chaves_2024.md)

**Escopo:** preparar bases importáveis e confiáveis, sem alterar os relatórios originais ou afirmar que o Power BI já foi implementado.
