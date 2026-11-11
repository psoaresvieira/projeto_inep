#!/usr/bin/env python3
"""Verifica correspondência entre escolas ENEM e Censo 2024, sem unir registros.

Requer dados_filtrados/* gerados por src/02_filtragem.py.
O arquivo de resultados ENEM pode ter múltiplos participantes por escola.
O Censo deve ter no máximo uma linha para cada CO_ENTIDADE/ano.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

PASTA = Path("dados_filtrados")
OUT = Path("reports/filtragem")
ENEM = PASTA / "enem_escola_estadual_PB_2024.csv"
CENSO = PASTA / "censo_escolas_estaduais_EM_PB_2024.csv"


def ler_coluna(path, coluna):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        if coluna not in (reader.fieldnames or []):
            raise ValueError(f"{path}: campo ausente: {coluna}")
        for row in reader:
            yield str(row.get(coluna) or "").strip()


def analisar():
    censo = Counter(ler_coluna(CENSO, "CO_ENTIDADE"))
    enem = Counter(ler_coluna(ENEM, "CO_ESCOLA"))
    censo.pop("", None)
    enem_vazios = enem.pop("", 0)
    censo_dupls = {codigo: n for codigo, n in censo.items() if n != 1}
    escolas_censo = set(censo)
    escolas_enem = set(enem)
    intersecao = escolas_enem & escolas_censo
    sem_par = escolas_enem - escolas_censo
    contagem_enem = sum(enem.values())
    linhas_matched = sum(enem[cod] for cod in intersecao)
    return {
        "escolas_distintas_censo": len(escolas_censo),
        "escolas_distintas_enem_resultados": len(escolas_enem),
        "escolas_em_ambas_as_bases": len(intersecao),
        "escolas_enem_sem_par_no_censo": len(sem_par),
        "escolas_censo_sem_participantes_identificados_enem": len(escolas_censo - escolas_enem),
        "linhas_participantes_enem_com_codigo": contagem_enem,
        "linhas_participantes_enem_sem_codigo": enem_vazios,
        "linhas_enem_com_correspondencia_escolar": linhas_matched,
        "linhas_enem_sem_correspondencia_escolar": contagem_enem - linhas_matched,
        "taxa_match_participantes_pct": round(100 * linhas_matched / contagem_enem, 2) if contagem_enem else None,
        "codigos_censo_duplicados": len(censo_dupls),
        "validade_juncao": "CANDIDATA_APROVADA_PARA_ANÁLISE_POR_ESCOLA" if not censo_dupls else "BLOQUEADA_DUPLICIDADE_CENSO",
        "alerta": "Esta é apenas a auditoria de cardinalidade e cobertura da chave CO_ESCOLA→CO_ENTIDADE, não uma junção de notas e questionário socioeconômico.",
    }


def main():
    result = analisar()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "validacao_chaves_2024.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    linhas = [
        "# Validação de chaves ENEM–Censo 2024 — Paraíba", "",
        "Recorte: resultados do ENEM com escola estadual identificada na PB e escolas estaduais de ensino médio no Censo Escolar 2024.",
        "Nenhuma junção por posição ou entre tabelas de participantes e resultados foi executada.", "",
        "| Métrica | Valor |", "|---|---:|",
    ]
    for key, value in result.items():
        if key in ("alerta", "validade_juncao"): continue
        linhas.append(f"| {key} | {value} |")
    linhas += ["", "**Status de cardinalidade:** " + result["validade_juncao"], "",
               result["alerta"], "",
               "**Limitações:** mesmo com chaves compatíveis, o recorte ENEM representa apenas participantes identificados,",
               "e o relacionamento com Censo 2024 não mede causalidade de características escolares sobre notas.",
               "Confirme os códigos e as definições nos dicionários antes de efetuar um \`merge\` definitivo.", ""]
    (OUT / "validacao_chaves_2024.md").write_text("\n".join(linhas), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
