# Censo Escolar 2024 — recorte da Paraíba

Contagens do CSV oficial extraído em streaming, sem publicar microdados individuais.

| Indicador | Quantidade |
|---|---:|
| registros_nacionais_escolas | 215545 |
| escolas_PB | 5325 |
| escolas_estaduais_PB | 667 |
| escolas_estaduais_ensino_medio_PB | 482 |
| escolas_estaduais_EM_com_codigo | 482 |
| municipios_estaduais_EM | 223 |
| matriculas_ensino_medio_somadas | 116779 |
| codigos_escola_repetidos_no_recorte | 0 |

Checksum MD5 do CSV validado contra arquivo interno do pacote.

## Infraestrutura no recorte

As frequências incluem categorias vazias. As interpretações dependem do dicionário oficial.

- **IN_INTERNET**: 1: 459, 0: 23
- **IN_BIBLIOTECA**: 1: 358, 0: 124
- **IN_SALA_LEITURA**: 0: 444, 1: 38
- **IN_LABORATORIO_CIENCIAS**: 1: 233, 0: 249
- **IN_LABORATORIO_INFORMATICA**: 1: 284, 0: 198
- **IN_QUADRA_ESPORTES**: 1: 248, 0: 234
- **IN_BANDA_LARGA**: 0: 320, 1: 139, (vazio): 23

**Cautela:** os indicadores de infraestrutura são descritivos, e matrículas são contagens por escola.

Fonte: [Censo Escolar — INEP](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar)
