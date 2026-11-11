#!/usr/bin/env python3
"""Perfil do IDEB 2025 por escola estadual da Paraíba (dados agregados).

Usa a linha de nomes técnicos da planilha, detectada dinamicamente.
Não substitui "-" por 0 nem presume que todas as escolas têm nota divulgada.
"""
from __future__ import annotations

import io
import json
import statistics
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import load_workbook

BASE = Path("dados_brutos")
OUT = Path("reports/inspecao")
ARQUIVO = "divulgacao_ensino_medio_escolas_2025.zip"
SUFIXO = "divulgacao_ensino_medio_escolas_2025.xlsx"


def texto(v):
    return "" if v is None else str(v).strip()


def nota(v):
    s = texto(v).replace(",", ".")
    try:
        n = float(s)
    except ValueError:
        return None
    if not (0 <= n <= 10):
        return None
    return n


def analisar():
    zip_path = BASE / ARQUIVO
    with zipfile.ZipFile(zip_path) as z:
        membros = [m for m in z.namelist() if m.endswith(SUFIXO)]
        if len(membros) != 1:
            raise ValueError("IDEB 2025: planilha .xlsx não encontrada de forma única.")
        with z.open(membros[0]) as f:
            dados = f.read()
    wb = load_workbook(io.BytesIO(dados), read_only=True, data_only=True)
    try:
        ws = wb.worksheets[0]
        linhas = ws.iter_rows(values_only=True)
        header = None
        num_header = None
        for i, row in enumerate(linhas, 1):
            campos = [texto(v) for v in row]
            if len(campos) >= 6 and campos[0] == "SG_UF" and campos[3] == "ID_ESCOLA":
                header = campos
                num_header = i
                break
        if header is None:
            raise ValueError("Cabeçalho técnico da planilha IDEB não localizado.")
        indices = {v: i for i, v in enumerate(header) if v}
        for obrigatoria in ("SG_UF", "CO_MUNICIPIO", "ID_ESCOLA", "REDE"):
            if obrigatoria not in indices:
                raise ValueError(f"Coluna obrigatória ausente: {obrigatoria}")

        candidatos = [s for s in indices if "IDEB" in s.upper() and "2025" in s]
        preferidos = [s for s in candidatos if s.upper() == "VL_IDEB_2025"]
        nome_ideb = (preferidos or candidatos or [None])[0]
        conta_pb = conta_estadual = 0
        codigos = set()
        cidades = set()
        sem_codigo = 0
        duplicados = 0
        valores = []
        invalidos = Counter()
        redes_pb = Counter()
        for row in linhas:
            if texto(row[indices["SG_UF"]]) != "PB":
                continue
            cod = texto(row[indices["ID_ESCOLA"]])
            if not cod:
                continue
            conta_pb += 1
            rede = texto(row[indices["REDE"]])
            redes_pb[rede or "(vazio)"] += 1
            if rede.casefold() != "estadual":
                continue
            conta_estadual += 1
            if cod in codigos:
                duplicados += 1
            else:
                codigos.add(cod)
            mun = texto(row[indices["CO_MUNICIPIO"]])
            if mun:
                cidades.add(mun)
            if not cod: sem_codigo += 1
            if nome_ideb:
                v = row[indices[nome_ideb]]
                valor = nota(v)
                if valor is None:
                    invalidos[texto(v) or "(vazio)"] += 1
                else:
                    valores.append(valor)

        stats = {"quantidade_com_IDEB_2025_valido": len(valores),
                 "quantidade_sem_IDEB_2025_valido": conta_estadual - len(valores),
                 "media_simples_escolas_com_nota": round(statistics.mean(valores), 3) if valores else None,
                 "mediana_escolas_com_nota": round(statistics.median(valores), 3) if valores else None,
                 "minimo": min(valores) if valores else None,
                 "maximo": max(valores) if valores else None}
        return {
            "arquivo": ARQUIVO, "aba": ws.title, "linha_cabecalho": num_header,
            "total_linhas_planilha_incluindo_cabecalhos": ws.max_row,
            "quantidade_escolas_PB_todas_redes": conta_pb,
            "quantidade_escolas_estaduais_PB_na_planilha": conta_estadual,
            "escolas_estaduais_distintas_PB": len(codigos),
            "municipios_com_escolas_estaduais_PB_na_planilha": len(cidades),
            "duplicidade_codigo_escola_estadual": duplicados,
            "redes_no_recorte_PB": dict(redes_pb),
            "colunas_IDEB_2025_candidatas": candidatos,
            "coluna_nota_usada": nome_ideb, "resumo_ideb_2025": stats,
            "motivos_nota_invalida": dict(invalidos),
            "aviso": "A média é não ponderada e inclui apenas escolas com IDEB válido; não representa IDEB oficial da rede estadual. Valores '-' e vazios não são nota zero.",
        }
    finally:
        wb.close()


def main():
    result = analisar()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ideb_pb_2025.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    linhas = [
        "# IDEB 2025 — Escolas estaduais da Paraíba", "",
        "Recorte da planilha oficial de ensino médio por escola. Valores ausentes não foram imputados.", "",
        "| Indicador | Valor |", "|---|---:|",
    ]
    for k in ("quantidade_escolas_PB_todas_redes",
              "quantidade_escolas_estaduais_PB_na_planilha",
              "escolas_estaduais_distintas_PB",
              "municipios_com_escolas_estaduais_PB_na_planilha",
              "duplicidade_codigo_escola_estadual"):
        linhas.append(f"| {k} | {result[k]} |")
    linhas.extend(["", "## IDEB 2025", "",
                   f"Coluna selecionada: \`{result['coluna_nota_usada']}\`.",
                   "Campos candidatos: " + ", ".join(result["colunas_IDEB_2025_candidatas"]),
                   "", "| Métrica | Valor |", "|---|---:|"])
    for k, v in result["resumo_ideb_2025"].items():
        linhas.append(f"| {k} | {v} |")
    linhas += ["", "## Valores ausentes ou não numéricos", "", "~~~json",
               json.dumps(result["motivos_nota_invalida"], indent=2, ensure_ascii=False),
               "~~~", "", "**Limitações:** a média simples não substitui o IDEB oficial da rede. "
               "A planilha de 2025 e o Censo 2024 referem-se a anos distintos e não devem ser tratados como mesmo período.",
               "", "[Fonte INEP — IDEB](https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/ideb)", ""]
    (OUT / "ideb_pb_2025.md").write_text("\n".join(linhas), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
