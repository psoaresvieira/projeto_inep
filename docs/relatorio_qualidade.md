# Protocolo de limpeza e controle de qualidade — Recortes PB 2024

**Estado:** regras implementadas e em testes; resultados de limpeza dos arquivos oficiais ainda pendentes.

## Escopo
Aplicável aos recortes produzidos por [src/02_filtragem.py](../src/02_filtragem.py):
- Resultados ENEM 2024 com escola estadual identificada na Paraíba;
- Escolas estaduais com oferta de ensino médio no Censo Escolar 2024;
- Participantes ENEM 2024 com **local de prova** na Paraíba, em arquivo separado.

## Regras efetivamente implementadas

1. Preservar os ZIPs e CSVs filtrados originais. Os arquivos tratados serão escritos em `dados_limpos/` (fora do Git).
2. Remover espaços periféricos dos valores, sem alterar a quantidade ou a ordem dos registros.
3. Manter códigos escolares como **texto** e nunca como números, evitando perda de zeros à esquerda.
4. Substituir códigos de escola não numéricos por campo vazio e registrar a ocorrência; o valor original permanece na base filtrada.
5. Tratar notas do ENEM:
   - Campo vazio permanece vazio (**não significa nota zero**).
   - Nota numérica entre 0 e 1000 é mantida (inclusive valor 0).
   - Texto não numérico ou nota fora de 0 a 1000 passa a vazio na base tratada e a ocorrência é registrada.
   - Conflitos entre `TP_PRESENCA_CN/CH/LC/MT` e nota são contabilizados, sem correção automática de presença.
   - O status de redação precisa ser interpretado com base no dicionário antes de análise de desempenho.
6. No Censo, contagens de matrículas, docentes e turmas devem ser inteiros não negativos. Campos inválidos ficam vazios, com registro das ocorrências.
7. Valores das variáveis de infraestrutura são mantidos como declarados. Categorias fora de `0` e `1` são sinalizadas, não recodificadas sem dicionário.
8. Duplicidade de código de escola no recorte do Censo não pode ser apagada silenciosamente. A execução deve indicar duplicidade e **bloquear a integração**, até sua investigação.

## Executar

```bash
python src/03_limpeza.py
python -m unittest discover -s tests -v
```

O script lê os três CSVs locais em `dados_filtrados/`, produz os mesmos recortes tratados na pasta privada `dados_limpos/` e um relatório agregado em `reports/qualidade/qualidade_2024.md`.

## Critérios para concluir a etapa

- [ ] Os recortes reais da Issue #2 foram gerados e validados.
- [ ] O script rodou em todos os recortes disponíveis e os arquivos permanecem fora do Git.
- [ ] Contagens antes e depois demonstram que nenhuma linha foi excluída.
- [ ] Os campos vazios, notas inválidas, inconsistências de presença e duplicidades foram contabilizados.
- [ ] Os tratamentos que dependem de códigos específicos foram confrontados com os dicionários oficiais.
- [ ] Qualquer falha relevante foi documentada, sem substituição especulativa de valores.

**Importante:** documentação de regras não equivale à validação dos dados reais. A Issue #3 deve ficar aberta até a execução e a auditoria.
