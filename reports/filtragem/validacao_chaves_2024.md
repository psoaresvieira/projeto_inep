# Validação de chaves ENEM–Censo 2024 — Paraíba

Recorte: resultados do ENEM com escola estadual identificada na PB e escolas estaduais de ensino médio no Censo Escolar 2024.
Nenhuma junção por posição ou entre tabelas de participantes e resultados foi executada.

| Métrica | Valor |
|---|---:|
| escolas_distintas_censo | 482 |
| escolas_distintas_enem_resultados | 497 |
| escolas_em_ambas_as_bases | 456 |
| escolas_enem_sem_par_no_censo | 41 |
| escolas_censo_sem_participantes_identificados_enem | 26 |
| linhas_participantes_enem_com_codigo | 29783 |
| linhas_participantes_enem_sem_codigo | 0 |
| linhas_enem_com_correspondencia_escolar | 29393 |
| linhas_enem_sem_correspondencia_escolar | 390 |
| taxa_match_participantes_pct | 98.69 |
| codigos_censo_duplicados | 0 |

**Status de cardinalidade:** CANDIDATA_APROVADA_PARA_ANÁLISE_POR_ESCOLA

Esta é apenas a auditoria de cardinalidade e cobertura da chave CO_ESCOLA→CO_ENTIDADE, não uma junção de notas e questionário socioeconômico.

**Limitações:** mesmo com chaves compatíveis, o recorte ENEM representa apenas participantes identificados,
e o relacionamento com Censo 2024 não mede causalidade de características escolares sobre notas.
Confirme os códigos e as definições nos dicionários antes de efetuar um \`merge\` definitivo.
