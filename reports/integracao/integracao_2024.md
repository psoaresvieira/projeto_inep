# Integração ENEM–Censo 2024 por escola — Paraíba

Indicadores agregados; a base escolar detalhada não é publicada no GitHub.

| Métrica | Valor |
|---|---:|
| ano_censo | 2024 |
| ano_enem | 2024 |
| escolas_censo | 482 |
| escolas_enem | 497 |
| escolas_com_correspondencia | 456 |
| escolas_censo_sem_enem | 26 |
| escolas_enem_sem_censo | 41 |
| linhas_enem_no_recorte | 29783 |
| linhas_enem_com_codigo | 29783 |
| linhas_enem_pareadas | 29393 |
| linhas_enem_nao_pareadas_com_codigo | 390 |
| minimo_notas_validas_para_media_escolar | 5 |

## Regras

- Chaves: CO_ESCOLA do ENEM RESULTADOS → CO_ENTIDADE do Censo, ambos 2024.
- A auditoria valida unicidade do Censo, correspondência de códigos e contagens.
- Unidades: escolas (não indivíduos). A base final é uma linha por escola do Censo.
- Médias por escola são omitidas com menos de cinco notas válidas da área.
- Apenas participantes com presença igual a 1 e nota numérica válida entram na média.
- Dados de PARTICIPANTES ENEM não foram relacionados ao RESULTADOS ENEM.

## Atenção

Métricas do ENEM refletem participantes identificados, não todos os alunos da escola.
A correspondência da chave não demonstra representatividade nem causalidade.
