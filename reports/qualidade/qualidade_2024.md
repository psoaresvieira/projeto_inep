# Qualidade dos recortes INEP 2024 — Paraíba

Limpeza conservadora, rastreável, sem imputação de valores e sem exclusão de linhas.
Somente informações agregadas são divulgadas neste documento.

## enem

- Registros preservados: 29783
- Colunas: 19
- Códigos escolares duplicados no Censo: None

### Qualidade por tipo de ocorrência

~~~json
{
  "NU_NOTA_CN:valida": 21786,
  "TP_PRESENCA_CN:1": 21786,
  "NU_NOTA_CH:valida": 22487,
  "TP_PRESENCA_CH:1": 22487,
  "NU_NOTA_LC:valida": 22487,
  "TP_PRESENCA_LC:1": 22487,
  "NU_NOTA_MT:valida": 21786,
  "TP_PRESENCA_MT:1": 21786,
  "NU_NOTA_REDACAO:valida": 22487,
  "NU_NOTA_CN:ausente": 7997,
  "TP_PRESENCA_CN:0": 7984,
  "NU_NOTA_CH:ausente": 7296,
  "TP_PRESENCA_CH:0": 7255,
  "NU_NOTA_LC:ausente": 7296,
  "TP_PRESENCA_LC:0": 7255,
  "NU_NOTA_MT:ausente": 7997,
  "TP_PRESENCA_MT:0": 7984,
  "NU_NOTA_REDACAO:ausente": 7296,
  "TP_PRESENCA_CH:2": 41,
  "TP_PRESENCA_LC:2": 41,
  "TP_PRESENCA_CN:2": 13,
  "TP_PRESENCA_MT:2": 13
}
~~~

### Campos vazios após limpeza

~~~json
{
  "NU_NOTA_CN": 7997,
  "NU_NOTA_CH": 7296,
  "NU_NOTA_LC": 7296,
  "NU_NOTA_MT": 7997,
  "TP_STATUS_REDACAO": 7296,
  "NU_NOTA_REDACAO": 7296
}
~~~

## censo

- Registros preservados: 482
- Colunas: 22
- Códigos escolares duplicados no Censo: 0

### Qualidade por tipo de ocorrência

~~~json
{
  "IN_INTERNET:1": 459,
  "IN_INTERNET_APRENDIZAGEM:1": 219,
  "IN_BANDA_LARGA:0": 320,
  "IN_BIBLIOTECA:1": 358,
  "IN_SALA_LEITURA:0": 444,
  "IN_LABORATORIO_CIENCIAS:1": 233,
  "IN_LABORATORIO_INFORMATICA:1": 284,
  "IN_QUADRA_ESPORTES:1": 248,
  "IN_AGUA_POTAVEL:1": 469,
  "QT_MAT_MED:valida": 482,
  "QT_DOC_MED:valida": 482,
  "QT_TUR_MED:valida": 482,
  "IN_INTERNET_APRENDIZAGEM:0": 263,
  "IN_BIBLIOTECA:0": 124,
  "IN_LABORATORIO_CIENCIAS:0": 249,
  "IN_BANDA_LARGA:1": 139,
  "IN_LABORATORIO_INFORMATICA:0": 198,
  "IN_QUADRA_ESPORTES:0": 234,
  "IN_SALA_LEITURA:1": 38,
  "IN_AGUA_POTAVEL:0": 13,
  "IN_INTERNET:0": 23,
  "IN_BANDA_LARGA:(vazio)": 23
}
~~~

### Campos vazios após limpeza

~~~json
{
  "IN_BANDA_LARGA": 23
}
~~~

## participantes

- Registros preservados: 128546
- Colunas: 14
- Códigos escolares duplicados no Censo: None

### Qualidade por tipo de ocorrência

~~~json
{}
~~~

### Campos vazios após limpeza

~~~json
{
  "TP_ENSINO": 93481
}
~~~

## Limitações

- Os valores brutos foram preservados nos ZIPs originais e nos arquivos filtrados.
- O tratamento de valores especiais segue uma abordagem conservadora e requer o dicionário oficial.
- Não houve vinculação individual de PARTICIPANTES_2024 com RESULTADOS_2024.
- A integração escolar depende da auditoria de correspondência e unicidade das chaves.
