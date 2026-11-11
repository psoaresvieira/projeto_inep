# Incorporacao das bases INEP 2025 — Plano de validacao

**Data:** 11/11/2026  
**Status:** download e inventário estrutural dos ZIPs concluídos no GitHub Actions; filtros, contagens da PB e integração de 2025 ainda pendentes.

## Arquivos oficiais selecionados

| Base | URL oficial | Observacao |
|---|---|---|
| ENEM 2025 | https://download.inep.gov.br/microdados/microdados_enem_2025.zip | Pagina do INEP informa atualizacao em 01/09/2026 (arquivo Leia-me) |
| Censo Escolar da Educacao Basica 2025 | https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2025_.zip | Pagina do INEP informa atualizacao da documentacao em julho/2026 |

Os links foram obtidos das paginas oficiais [ENEM — microdados](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem) e [Censo Escolar — microdados](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar).

## Inspecao reproduzivel no GitHub Actions

O workflow [inspecao-2025.yml](../.github/workflows/inspecao-2025.yml) baixa os arquivos em `dados_brutos/` (ignorada pelo Git), verifica se sao pacotes ZIP, identifica arquivos internos e le amostras dos cabecalhos tabulares com `src/01_inspecao.py`.

Apos execucao bem-sucedida, o resultado esperado e:
- `reports/inspecao_2025/inventario.md` (texto publicado);
- `reports/inspecao_2025/inventario.json` (artefato temporario);
- `reports/inspecao_2025/downloads.json` (artefato temporario).

**A inspeção estrutural foi concluída** com sucesso em [GitHub Actions #43067294218](https://github.com/psoaresvieira/projeto_inep/actions/runs/43067294218). O [inventário de 2025](../reports/inspecao_2025/inventario.md) foi publicado. A leitura dos cabeçalhos não constitui a análise completa.

## Resultados efetivamente observados na inspeção de 2025

| Item | Resultado |
|---|---|
| ENEM 2025 | ZIP válido, com 21 arquivos internos, incluindo PARTICIPANTES_2025.csv e RESULTADOS_2025.csv |
| ENEM 2025 — participantes | CSV com 38 colunas amostradas; contém NU_INSCRICAO e SG_UF_PROVA |
| ENEM 2025 — resultados | CSV identificado, **leitura bloqueada: método de compactação não suportado** pela biblioteca Python utilizada |
| Censo Escolar 2025 | ZIP válido, com 19 arquivos internos |
| Censo 2025 — escolas | Tabela_Escola_2025_V2.csv, 290 colunas amostradas, incluindo CO_ENTIDADE, CO_MUNICIPIO, SG_UF e TP_DEPENDENCIA |
| Censo 2025 — arquivos | Separação em tabelas Escola, Matrícula, Docente, Turma, Gestor e Curso Técnico |

**Não foi verificada a contagem de estudantes ou escolas da PB nas edições 2025.**
A tabela escolar de 2025 foi reorganizada e não pode ser tratada como cópia idêntica do CSV único de 2024. O campo de notas do ENEM 2025 ainda exige suporte à compactação utilizada no pacote e verificação do dicionário.

**Próximas medidas técnicas:** identificar o método numérico de compressão do membro RESULTADOS_2025.csv e instalar um descompactador compatível (sem usar fallback que altere os bytes); validar o arquivo extraído e seu dicionário; adaptar os filtros do Censo à estrutura de múltiplas tabelas; calcular contagens reais e conferir chaves antes de qualquer comparação 2024–2025.

## Revisoes obrigatorias antes de filtrar e integrar

- [ ] Confirmar CSVs principais e dicionarios de 2025 e comparar nomes com 2024.
- [ ] Confirmar disponibilidade e semantica de `SG_UF_ESC`, `TP_DEPENDENCIA_ADM_ESC`, `CO_ESCOLA` no ENEM 2025; nao presumir esquema identico.
- [ ] Confirmar `SG_UF`, `TP_DEPENDENCIA`, `IN_MED`, `QT_MAT_MED` e `CO_ENTIDADE` no Censo 2025.
- [ ] Separar unidades analiticas: participantes com local de prova na PB, estudantes com escola estadual identificada, escolas do Censo e escolas do IDEB.
- [ ] Verificar integridade e eventual assinatura/checksum oficial antes de utilizar os dados; descompactacao ZIP e tamanho nao comprovam autenticidade.
- [ ] Validar cobertura das escolas, cardinalidade e valores faltantes por ano.
- [ ] So apos a verificacao das colunas, criar scripts de filtragem e integracao especificos de 2025.

## Estrategia de analise longitudinal

1. Produzir indicadores **independentes por ano** usando denominadores comparaveis.
2. Comparar ENEM 2024 e 2025 **entre grupos**; sem ligacao individual entre os participantes.
3. Comparar Censo 2024 e 2025 por codigo de escola, avaliando escolas que entram/saem da base e mudancas de oferta.
4. Vincular IDEB 2025 a Censo 2025 somente com codigos e periodo correspondentes; avaliar escolas sem divulgacao de nota.
5. Evitar inferir efeito causal de infraestrutura sobre notas e evitar atribuir notas a estudantes sem chave individual oficial.

**Privacidade:** os arquivos nacionais e os recortes com linhas individuais nao devem ser publicados no repositorio.
