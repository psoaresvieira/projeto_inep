# Perfil dos dados — Paraíba

Relatório agregado, sem linhas individuais e sem junções entre participantes e resultados.
O filtro por escola da rede estadual usa SG_UF_ESC=PB e TP_DEPENDENCIA_ADM_ESC=2.
O filtro de Censo usa SG_UF=PB, TP_DEPENDENCIA=2 e oferta de ensino médio.
As médias do ENEM abrangem apenas participantes com escola identificada e nota válida.
A validade e o significado das variáveis exigem conferência dos dicionários oficiais.

## PARTICIPANTES_ENEM_2024

~~~json
{
  "registros_nacionais": 4332944,
  "local_de_prova_PB": 128546,
  "campos_vazios_entre_local_prova_PB": {},
  "alerta": "Local de prova não equivale à residência ou à escola. Não juntar por ordem com RESULTADOS."
}
~~~

## RESULTADOS_ENEM_2024

~~~json
{
  "registros_nacionais": 4332944,
  "escola_na_PB": 37251,
  "local_de_prova_PB": 128546,
  "escola_estadual_na_PB": 29783,
  "sem_codigo_escola_entre_escolas_PB": 0,
  "codigos_escola_distintos_PB": 696,
  "municipios_escolares_distintos_PB": 223,
  "NU_SEQUENCIAL_nao_numerico": 0,
  "NU_SEQUENCIAL_diferente_da_posicao_linha": 4332944,
  "notas_de_participantes_com_escola_estadual_PB": {
    "NU_NOTA_CN": {
      "validas": 21786,
      "min": 0.0,
      "max": 735.8,
      "media": 456.53
    },
    "NU_NOTA_CH": {
      "validas": 22487,
      "min": 0.0,
      "max": 783.4,
      "media": 467.67
    },
    "NU_NOTA_LC": {
      "validas": 22487,
      "min": 0.0,
      "max": 718.0,
      "media": 489.85
    },
    "NU_NOTA_MT": {
      "validas": 21786,
      "min": 0.0,
      "max": 881.3,
      "media": 476.81
    },
    "NU_NOTA_REDACAO": {
      "validas": 22487,
      "min": 0.0,
      "max": 980.0,
      "media": 571.92
    }
  },
  "alerta": "Notas de participantes cuja escola estadual está identificada na PB; não representam todos os estudantes da rede."
}
~~~

## CENSO_ESCOLAR_2024

~~~json
{
  "registros_nacionais_escolas": 215545,
  "escolas_PB": 5325,
  "escolas_estaduais_PB": 667,
  "escolas_estaduais_ensino_medio_PB": 482,
  "escolas_estaduais_EM_com_codigo": 482,
  "municipios_estaduais_EM": 223,
  "matriculas_ensino_medio_somadas": 116779,
  "codigos_escola_repetidos_no_recorte": 0,
  "chaves_vazias": {},
  "valores_infraestrutura": {
    "IN_INTERNET": {
      "1": 459,
      "0": 23
    },
    "IN_BIBLIOTECA": {
      "1": 358,
      "0": 124
    },
    "IN_SALA_LEITURA": {
      "0": 444,
      "1": 38
    },
    "IN_LABORATORIO_CIENCIAS": {
      "1": 233,
      "0": 249
    },
    "IN_LABORATORIO_INFORMATICA": {
      "1": 284,
      "0": 198
    },
    "IN_QUADRA_ESPORTES": {
      "1": 248,
      "0": 234
    },
    "IN_BANDA_LARGA": {
      "0": 320,
      "1": 139,
      "(vazio)": 23
    }
  },
  "alerta": "Cada linha representa uma escola. Matrículas são quantidades declaradas por escola; confirmar conceitos no dicionário."
}
~~~

## IDEB_2025

~~~json
{
  "planilhas": [
    {
      "aba": "IDEB_Escolas (ENSINO MÉDIO)",
      "total_linhas_incluindo_cabecalhos": 22195,
      "total_colunas": 60,
      "amostra_cabecalhos": [
        [
          {
            "coluna": 3,
            "texto": "Ministério da Educação"
          }
        ],
        [
          {
            "coluna": 3,
            "texto": "Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira"
          }
        ],
        [],
        [
          {
            "coluna": 1,
            "texto": "Ensino Médio Regular"
          }
        ],
        [
          {
            "coluna": 1,
            "texto": "Indicadores educacionais compostos por: Taxa de Aprovação, SAEB e IDEB nos anos de 2017, 2019, 20211"
          }
        ],
        [],
        [
          {
            "coluna": 1,
            "texto": "Sigla da UF"
          },
          {
            "coluna": 2,
            "texto": "Código do Município"
          },
          {
            "coluna": 3,
            "texto": "Nome do Município"
          },
          {
            "coluna": 4,
            "texto": "Código da Escola"
          },
          {
            "coluna": 5,
            "texto": "Nome da Escola"
          },
          {
            "coluna": 6,
            "texto": "Rede"
          },
          {
            "coluna": 7,
            "texto": "Taxa de Aprovação - 2017"
          },
          {
            "coluna": 13,
            "texto": "Taxa de Aprovação - 2019"
          },
          {
            "coluna": 19,
            "texto": "Taxa de Aprovação - 20211"
          },
          {
            "coluna": 25,
            "texto": "Taxa de Aprovação - 2023"
          },
          {
            "coluna": 31,
            "texto": "Taxa de Aprovação - 2025"
          },
          {
            "coluna": 37,
            "texto": "Nota SAEB - 2017"
          },
          {
            "coluna": 40,
            "texto": "Nota SAEB - 2019"
          },
          {
            "coluna": 43,
            "texto": "Nota SAEB - 20211"
          },
          {
            "coluna": 46,
            "texto": "Nota SAEB - 2023"
          },
          {
            "coluna": 49,
            "texto": "Nota SAEB - 2025"
          },
          {
            "coluna": 52,
            "texto": "IDEB\n2017\n(N x P)"
          },
          {
            "coluna": 53,
            "texto": "IDEB\n2019\n(N x P)"
          }
        ],
        [
          {
            "coluna": 37,
            "texto": "Matemática"
          },
          {
            "coluna": 38,
            "texto": "Língua Portuguesa"
          },
          {
            "coluna": 39,
            "texto": "Nota Média Padronizada (N)"
          },
          {
            "coluna": 40,
            "texto": "Matemática"
          },
          {
            "coluna": 41,
            "texto": "Língua Portuguesa"
          },
          {
            "coluna": 42,
            "texto": "Nota Média Padronizada (N)"
          },
          {
            "coluna": 43,
            "texto": "Matemática"
          },
          {
            "coluna": 44,
            "texto": "Língua Portuguesa"
          },
          {
            "coluna": 45,
            "texto": "Nota Média Padronizada (N)"
          },
          {
            "coluna": 46,
            "texto": "Matemática"
          },
          {
            "coluna": 47,
            "texto": "Língua Portuguesa"
          },
          {
            "coluna": 48,
            "texto": "Nota Média Padronizada (N)"
          },
          {
            "coluna": 49,
            "texto": "Matemática"
          },
          {
            "coluna": 50,
            "texto": "Língua Portuguesa"
          },
          {
            "coluna": 51,
            "texto": "Nota Média Padronizada (N)"
          }
        ],
        [
          {
            "coluna": 7,
            "texto": "Total"
          },
          {
            "coluna": 8,
            "texto": "1ª série"
          },
          {
            "coluna": 9,
            "texto": "2ª série"
          },
          {
            "coluna": 10,
            "texto": "3ª série"
          },
          {
            "coluna": 11,
            "texto": "4ª série"
          },
          {
            "coluna": 12,
            "texto": "Indicador de Rendimento (P)"
          },
          {
            "coluna": 13,
            "texto": "Total"
          },
          {
            "coluna": 14,
            "texto": "1ª série"
          },
          {
            "coluna": 15,
            "texto": "2ª série"
          },
          {
            "coluna": 16,
            "texto": "3ª série"
          },
          {
            "coluna": 17,
            "texto": "4ª série"
          },
          {
            "coluna": 18,
            "texto": "Indicador de Rendimento (P)"
          },
          {
            "coluna": 19,
            "texto": "Total"
          },
          {
            "coluna": 20,
            "texto": "1ª série"
          },
          {
            "coluna": 21,
            "texto": "2ª série"
          },
          {
            "coluna": 22,
            "texto": "3ª série"
          },
          {
            "coluna": 23,
            "texto": "4ª série"
          },
          {
            "coluna": 24,
            "texto": "Indicador de Rendimento (P)"
          }
        ],
        [
          {
            "coluna": 1,
            "texto": "SG_UF"
          },
          {
            "coluna": 2,
            "texto": "CO_MUNICIPIO"
          },
          {
            "coluna": 3,
            "texto": "NO_MUNICIPIO"
          },
          {
            "coluna": 4,
            "texto": "ID_ESCOLA"
          },
          {
            "coluna": 5,
            "texto": "NO_ESCOLA"
          },
          {
            "coluna": 6,
            "texto": "REDE"
          },
          {
            "coluna": 7,
            "texto": "VL_APROVACAO_2017_SI_4"
          },
          {
            "coluna": 8,
            "texto": "VL_APROVACAO_2017_1"
          },
          {
            "coluna": 9,
            "texto": "VL_APROVACAO_2017_2"
          },
          {
            "coluna": 10,
            "texto": "VL_APROVACAO_2017_3"
          },
          {
            "coluna": 11,
            "texto": "VL_APROVACAO_2017_4"
          },
          {
            "coluna": 12,
            "texto": "VL_INDICADOR_REND_2017"
          },
          {
            "coluna": 13,
            "texto": "VL_APROVACAO_2019_SI_4"
          },
          {
            "coluna": 14,
            "texto": "VL_APROVACAO_2019_1"
          },
          {
            "coluna": 15,
            "texto": "VL_APROVACAO_2019_2"
          },
          {
            "coluna": 16,
            "texto": "VL_APROVACAO_2019_3"
          },
          {
            "coluna": 17,
            "texto": "VL_APROVACAO_2019_4"
          },
          {
            "coluna": 18,
            "texto": "VL_INDICADOR_REND_2019"
          }
        ],
        [
          {
            "coluna": 1,
            "texto": "RO"
          },
          {
            "coluna": 2,
            "texto": "1100015"
          },
          {
            "coluna": 3,
            "texto": "Alta Floresta D'Oeste"
          },
          {
            "coluna": 4,
            "texto": "11024682"
          },
          {
            "coluna": 5,
            "texto": "EEEFM EURIDICE LOPES PEDROSO"
          },
          {
            "coluna": 6,
            "texto": "Estadual"
          },
          {
            "coluna": 7,
            "texto": "-"
          },
          {
            "coluna": 8,
            "texto": "-"
          },
          {
            "coluna": 9,
            "texto": "-"
          },
          {
            "coluna": 10,
            "texto": "-"
          },
          {
            "coluna": 11,
            "texto": "-"
          },
          {
            "coluna": 12,
            "texto": "-"
          },
          {
            "coluna": 13,
            "texto": "-"
          },
          {
            "coluna": 14,
            "texto": "-"
          },
          {
            "coluna": 15,
            "texto": "-"
          },
          {
            "coluna": 16,
            "texto": "-"
          },
          {
            "coluna": 17,
            "texto": "-"
          },
          {
            "coluna": 18,
            "texto": "-"
          }
        ],
        [
          {
            "coluna": 1,
            "texto": "RO"
          },
          {
            "coluna": 2,
            "texto": "1100015"
          },
          {
            "coluna": 3,
            "texto": "Alta Floresta D'Oeste"
          },
          {
            "coluna": 4,
            "texto": "11024968"
          },
          {
            "coluna": 5,
            "texto": "EEEMTI JUSCELINO KUBITSCHEK DE OLIVEIRA"
          },
          {
            "coluna": 6,
            "texto": "Estadual"
          },
          {
            "coluna": 7,
            "texto": "96.1"
          },
          {
            "coluna": 8,
            "texto": "96.2"
          },
          {
            "coluna": 9,
            "texto": "95.1"
          },
          {
            "coluna": 10,
            "texto": "96.4"
          },
          {
            "coluna": 11,
            "texto": "-"
          },
          {
            "coluna": 12,
            "texto": "0.958966"
          },
          {
            "coluna": 13,
            "texto": "97.7"
          },
          {
            "coluna": 14,
            "texto": "96.2"
          },
          {
            "coluna": 15,
            "texto": "96.3"
          },
          {
            "coluna": 16,
            "texto": "100"
          },
          {
            "coluna": 17,
            "texto": "-"
          },
          {
            "coluna": 18,
            "texto": "0.974683"
          }
        ],
        [
          {
            "coluna": 1,
            "texto": "RO"
          },
          {
            "coluna": 2,
            "texto": "1100015"
          },
          {
            "coluna": 3,
            "texto": "Alta Floresta D'Oeste"
          },
          {
            "coluna": 4,
            "texto": "11025638"
          },
          {
            "coluna": 5,
            "texto": "COLEGIO TIRADENTES DA POLICIA MILITAR - CTPM XI"
          },
          {
            "coluna": 6,
            "texto": "Estadual"
          },
          {
            "coluna": 7,
            "texto": "85.1"
          },
          {
            "coluna": 8,
            "texto": "80.2"
          },
          {
            "coluna": 9,
            "texto": "89"
          },
          {
            "coluna": 10,
            "texto": "87.8"
          },
          {
            "coluna": 11,
            "texto": "-"
          },
          {
            "coluna": 12,
            "texto": "0.85484"
          },
          {
            "coluna": 13,
            "texto": "91.4"
          },
          {
            "coluna": 14,
            "texto": "90.8"
          },
          {
            "coluna": 15,
            "texto": "90.4"
          },
          {
            "coluna": 16,
            "texto": "93.5"
          },
          {
            "coluna": 17,
            "texto": "-"
          },
          {
            "coluna": 18,
            "texto": "0.915462"
          }
        ],
        [
          {
            "coluna": 1,
            "texto": "RO"
          },
          {
            "coluna": 2,
            "texto": "1100023"
          },
          {
            "coluna": 3,
            "texto": "Ariquemes"
          },
          {
            "coluna": 4,
            "texto": "11006773"
          },
          {
            "coluna": 5,
            "texto": "EEEFM CORA CORALINA"
          },
          {
            "coluna": 6,
            "texto": "Estadual"
          },
          {
            "coluna": 7,
            "texto": "-"
          },
          {
            "coluna": 8,
            "texto": "-"
          },
          {
            "coluna": 9,
            "texto": "-"
          },
          {
            "coluna": 10,
            "texto": "-"
          },
          {
            "coluna": 11,
            "texto": "-"
          },
          {
            "coluna": 12,
            "texto": "-"
          },
          {
            "coluna": 13,
            "texto": "68"
          },
          {
            "coluna": 14,
            "texto": "33.8"
          },
          {
            "coluna": 15,
            "texto": "70.9"
          },
          {
            "coluna": 16,
            "texto": "78.8"
          },
          {
            "coluna": 17,
            "texto": "-"
          },
          {
            "coluna": 18,
            "texto": "0.532099"
          }
        ],
        [
          {
            "coluna": 1,
            "texto": "RO"
          },
          {
            "coluna": 2,
            "texto": "1100023"
          },
          {
            "coluna": 3,
            "texto": "Ariquemes"
          },
          {
            "coluna": 4,
            "texto": "11006889"
          },
          {
            "coluna": 5,
            "texto": "EEEFM ANISIO TEIXEIRA"
          },
          {
            "coluna": 6,
            "texto": "Estadual"
          },
          {
            "coluna": 7,
            "texto": "70.2"
          },
          {
            "coluna": 8,
            "texto": "62.8"
          },
          {
            "coluna": 9,
            "texto": "68.8"
          },
          {
            "coluna": 10,
            "texto": "86.3"
          },
          {
            "coluna": 11,
            "texto": "-"
          },
          {
            "coluna": 12,
            "texto": "0.713505"
          },
          {
            "coluna": 13,
            "texto": "70.3"
          },
          {
            "coluna": 14,
            "texto": "58.5"
          },
          {
            "coluna": 15,
            "texto": "70.5"
          },
          {
            "coluna": 16,
            "texto": "91.2"
          },
          {
            "coluna": 17,
            "texto": "-"
          },
          {
            "coluna": 18,
            "texto": "0.710171"
          }
        ]
      ]
    }
  ],
  "alerta": "Contagem inclui títulos, cabeçalhos e notas. Ainda não é contagem validada de escolas da PB."
}
~~~

## Restrição de integração do ENEM 2024

PARTICIPANTES_2024 usa NU_INSCRICAO; RESULTADOS_2024 usa NU_SEQUENCIAL.
Não existe chave comum validada; não juntar por índice ou posição das linhas.

## Próximos passos

- Conferir códigos e definições dos dicionários oficiais.
- Testar correspondência de CO_ESCOLA com CO_ENTIDADE somente após validar formato e completude.
- Identificar os cabeçalhos e colunas relevantes da planilha IDEB 2025.
- Adicionar os dados ENEM e Censo de 2025 quando disponíveis.
