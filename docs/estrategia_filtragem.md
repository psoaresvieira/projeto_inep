# Estratégia de filtragem — dados do INEP na Paraíba (2024)

## Objetivo
Criar subconjuntos analíticos reprodutíveis para o ensino médio estadual da Paraíba, preservando os ZIPs originais e evitando junções sem chave válida.

## Bases, população e filtros

| Arquivo original | Saída local (não versionada) | Critério |
|---|---|---|
| `RESULTADOS_2024.csv` (ENEM) | `dados_filtrados/enem_escola_estadual_PB_2024.csv` | `SG_UF_ESC = 'PB'` e `TP_DEPENDENCIA_ADM_ESC = '2'` |
| `microdados_ed_basica_2024.csv` (Censo) | `dados_filtrados/censo_escolas_estaduais_EM_PB_2024.csv` | `SG_UF = 'PB'`, `TP_DEPENDENCIA = '2'` e `IN_MED = '1'` ou `QT_MAT_MED > 0` |
| `PARTICIPANTES_2024.csv` (ENEM) | `dados_filtrados/enem_local_prova_PB_2024.csv` | `SG_UF_PROVA = 'PB'` |

**Atenção:** a terceira base seleciona apenas pessoas que fizeram a prova na PB, independentemente de sua escola ou residência. Ela NÃO deve ser usada como população de estudantes estaduais nem vinculada individualmente às notas de `RESULTADOS_2024` por posição.

O código de dependência `2` e o campo `IN_MED` devem ser conferidos no dicionário oficial da edição.

## Script e execução

Com Python 3.10+, na raiz do repositório, coloque os ZIPs oficiais na pasta `dados_brutos/`. Depois:

```bash
python src/02_filtragem.py
```

Para calcular apenas contagens sem produzir arquivos individuais:

```bash
python src/02_filtragem.py --somente-resumo
```

O programa faz leitura em streaming diretamente dos ZIPs, sem extração completa. Ao executar com o primeiro comando, gera arquivos CSV menores na pasta local `dados_filtrados/`, ignorada pelo Git. Em ambos os modos, cria `reports/filtragem/resumo_2024.md` com contagem nacional, quantidade selecionada, municípios e escolas distintos.

## Critérios de validação antes de encerrar a Issue #2

- [ ] Conferir o significado de todos os códigos usados nos dicionários oficiais.
- [ ] Executar o script nos três ZIPs e registrar as contagens.
- [ ] Garantir que somente o grupo pertinente foi exportado (amostras de checagem).
- [ ] Verificar existência de códigos de escola ausentes, duplicados ou não identificáveis.
- [ ] Checar a diversidade de municípios; diferenciar município de prova e escola.
- [ ] Registrar versão do script, fonte do ZIP e data de obtenção.
- [ ] Confirmar que nenhuma linha individual será versionada no repositório público.

## Observações metodológicas

Não utilizar o ENEM como indicador direto de toda a rede. O estudo deve tratar ENEM e IDEB/Censo em unidades apropriadas. O IDEB 2025 só poderá ser integrado ao Censo 2025 por chaves e ano compatíveis após confirmação dos códigos na planilha. A integração de Censo 2024 com IDEB 2025, quando utilizada, precisará ser explicitamente longitudinal e justificada.

## Referências oficiais
- [Microdados ENEM](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)
- [Microdados Censo Escolar](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar)
