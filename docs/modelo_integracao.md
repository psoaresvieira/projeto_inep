# Modelo de integração analítica — ENEM e Censo Escolar 2024

**Estado:** modelo e testes sintéticos publicados. A integração real é condicionada à auditoria de chaves da Issue #2 e à limpeza da Issue #3.

## Objetivo e limites

Relacionar resultados de participantes do ENEM 2024 **com escola estadual identificada na Paraíba** às características de sua escola no Censo Escolar 2024.

**Unidade da saída:** uma escola do Censo por linha, com indicadores agregados do ENEM quando existirem correspondências válidas.

O questionário socioeconômico em `PARTICIPANTES_2024.csv` **não** faz parte desta integração: não foi identificada chave individual comum com `RESULTADOS_2024.csv`. Não realizar junções por índice ou posição.

## Chaves candidatas

| Fonte | Campo | Unidade | Ano |
|---|---|---|---|
| ENEM 2024 — RESULTADOS | `CO_ESCOLA` | Várias linhas de participantes para uma escola | 2024 |
| Censo Escolar 2024 | `CO_ENTIDADE` | Uma linha por escola | 2024 |

O identificador escolar é mantido como texto, sem conversão numérica. O relacionamento muitos-para-um é auditado antes da agregação. A base integrada final é uma linha por escola do Censo, equivalente a uma junção da tabela escolar à agregação escolar do ENEM.

## Pré-condições bloqueantes

1. Existe relatório de correspondência `reports/filtragem/validacao_chaves_2024.json` com status de chave candidata aprovada.
2. Não há duplicidade de `CO_ENTIDADE` no recorte do Censo.
3. Todos os registros de ambos os recortes possuem ano 2024, UF PB e rede estadual, nos campos previstos.
4. As quantidades de escolas e de linhas pareadas do relatório de auditoria devem corresponder à execução atual.
5. Somente indicadores agregados podem integrar o arquivo por escola.
6. Se qualquer pré-condição falhar, o programa deve interromper o processamento e registrar o erro.

## Indicadores criados

Para cada escola do Censo:
- Presença de participantes do ENEM 2024 identificados na escola;
- Médias por área de prova apenas dos participantes que tenham nota entre 0 e 1000 **e status de presença 1**;
- Notas de redação consideradas com status correspondente a redação válida (`TP_STATUS_REDACAO=1`, sujeito à confirmação oficial no dicionário);
- Médias e respectivos denominadores por escola somente quando houver **pelo menos cinco notas válidas** naquela área;
- Dados descritivos de infraestrutura escolar, professores e matrículas do Censo 2024.

O arquivo integrado detalhado é gravado em `dados_integrados/base_escolar_enem_censo_PB_2024.csv`, excluído do Git. O repositório publica apenas um relatório agregado das coberturas.

## Como reproduzir

```bash
python src/02_filtragem.py
python src/02_validar_chaves.py
python src/03_limpeza.py
python src/04_integracao.py
```

O script de integração lê `dados_limpos/` e verifica as contagens da auditoria. Não aceita a ausência do relatório ou duplicações no Censo.

## Limitações de interpretação

- Alunos que não participaram do ENEM ou cujas informações escolares não aparecem ficam fora da avaliação de notas.
- A infraestrutura escolar é um dado observacional, não evidência de efeito causal sobre o desempenho.
- IDEB 2025 não entra nesta junção de mesmo ano. Deve ser acrescentado como uma **segunda comparação temporal explícita** ou com Censo 2025, sujeito a correspondência de chaves.
- O limiar de cinco notas válidas é um cuidado operacional mínimo e não garante, isoladamente, anonimato ou confiabilidade estatística. Indicadores e grupos pequenos exigem revisão adicional antes de qualquer divulgação.
- O relatório agregado do IDEB 2025 é independente até a integração temporal ser justificada.

## Critérios de conclusão da Issue #4

- [ ] A auditoria real de chaves da Issue #2 foi concluída e revisada.
- [ ] A limpeza real da Issue #3 foi concluída.
- [ ] A base integrada foi gerada sem multiplicação de escolas.
- [ ] Quantidades de escolas pareadas e notas usadas foram auditadas.
- [ ] O relatório agregado foi publicado sem registros individuais.
- [ ] As restrições de inferência e privacidade foram documentadas.
