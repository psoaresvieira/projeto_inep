#!/usr/bin/env python3
"""Issue #1: contagens e qualidade agregadas da Paraíba nos pacotes INEP.

Execução: python src/01_perfil_paraiba.py
Arquivos ZIP originais devem existir em dados_brutos/.
Não exporta linhas individuais. Não relaciona PARTICIPANTES a RESULTADOS por ordem.
"""
from __future__ import annotations

import csv
import io
import json
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("dados_brutos")
OUT = Path("reports/inspecao")
csv.field_size_limit(20_000_000)
ZIP_ENEM = "microdados_enem_2024.zip"
ZIP_CENSO = "microdados_censo_escolar_2024.zip"
ZIP_IDEB = "divulgacao_ensino_medio_escolas_2025.zip"
NOTAS = ("NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO")
INFRA = ("IN_INTERNET", "IN_BIBLIOTECA", "IN_SALA_LEITURA", "IN_LABORATORIO_CIENCIAS",
         "IN_LABORATORIO_INFORMATICA", "IN_QUADRA_ESPORTES", "IN_BANDA_LARGA")


def v(row, key):
    value = row.get(key)
    return "" if value is None else str(value).strip()


def nfloat(text):
    try:
        return float(text.replace(",", "."))
    except (ValueError, TypeError):
        return None


def csv_zip(zip_name, suffix):
    zf = zipfile.ZipFile(BASE / zip_name)
    found = [x for x in zf.infolist() if x.filename.lower().endswith(suffix.lower())]
    if len(found) != 1:
        zf.close()
        raise ValueError(f"{zip_name}: encontrado(s) {len(found)} arquivo(s) com final {suffix}")
    f = io.TextIOWrapper(zf.open(found[0]), encoding="utf-8-sig", errors="replace", newline="")
    reader = csv.DictReader(f, delimiter=";")
    return zf, f, reader


def verificar(reader, needed):
    missing = sorted(set(needed).difference(reader.fieldnames or []))
    if missing:
        raise ValueError("Colunas esperadas não encontradas: " + ", ".join(missing))


def participantes():
    zf, f, rows = csv_zip(ZIP_ENEM, "DADOS/PARTICIPANTES_2024.csv")
    campos = ["SG_UF_PROVA", "NU_INSCRICAO", "Q001", "Q002", "Q007"]
    verificar(rows, campos)
    total = pb = 0
    faltas = Counter()
    try:
        for r in rows:
            total += 1
            if v(r, "SG_UF_PROVA") != "PB":
                continue
            pb += 1
            for c in campos:
                if not v(r, c):
                    faltas[c] += 1
    finally:
        f.close()
        zf.close()
    return {"registros_nacionais": total, "local_de_prova_PB": pb,
            "campos_vazios_entre_local_prova_PB": dict(faltas),
            "alerta": "Local de prova não equivale à residência ou à escola. Não juntar por ordem com RESULTADOS."}


def resultados():
    zf, f, rows = csv_zip(ZIP_ENEM, "DADOS/RESULTADOS_2024.csv")
    needed = ["SG_UF_ESC", "CO_ESCOLA", "CO_MUNICIPIO_ESC", "TP_DEPENDENCIA_ADM_ESC",
              "SG_UF_PROVA", "NU_SEQUENCIAL", *NOTAS]
    verificar(rows, needed)
    total = pb_esc = pb_prova = estadual = sem_codigo_pb = 0
    escolas, municipios = set(), set()
    seq_diferente_linha = 0
    seq_nao_numerico = 0
    notas = {k: {"validas": 0, "soma": 0, "min": None, "max": None} for k in NOTAS}
    try:
        for idx, r in enumerate(rows, 1):
            total += 1
            escola_pb = v(r, "SG_UF_ESC") == "PB"
            if v(r, "SG_UF_PROVA") == "PB":
                pb_prova += 1
            if escola_pb:
                pb_esc += 1
                cod = v(r, "CO_ESCOLA")
                if cod: escolas.add(cod)
                else: sem_codigo_pb += 1
                mun = v(r, "CO_MUNICIPIO_ESC")
                if mun: municipios.add(mun)
                if v(r, "TP_DEPENDENCIA_ADM_ESC") == "2":
                    estadual += 1
                    for key in NOTAS:
                        val = nfloat(v(r, key))
                        if val is None or not (0 <= val <= 1000):
                            continue
                        info = notas[key]
                        info["validas"] += 1
                        info["soma"] += val
                        info["min"] = val if info["min"] is None else min(val, info["min"])
                        info["max"] = val if info["max"] is None else max(val, info["max"])
            seq = v(r, "NU_SEQUENCIAL")
            if not seq.isdigit(): seq_nao_numerico += 1
            elif int(seq) != idx: seq_diferente_linha += 1
    finally:
        f.close()
        zf.close()
    for info in notas.values():
        soma = info.pop("soma")
        info["media"] = round(soma / info["validas"], 2) if info["validas"] else None
    return {"registros_nacionais": total, "escola_na_PB": pb_esc,
            "local_de_prova_PB": pb_prova, "escola_estadual_na_PB": estadual,
            "sem_codigo_escola_entre_escolas_PB": sem_codigo_pb,
            "codigos_escola_distintos_PB": len(escolas),
            "municipios_escolares_distintos_PB": len(municipios),
            "NU_SEQUENCIAL_nao_numerico": seq_nao_numerico,
            "NU_SEQUENCIAL_diferente_da_posicao_linha": seq_diferente_linha,
            "notas_de_participantes_com_escola_estadual_PB": notas,
            "alerta": "Notas de participantes cuja escola estadual está identificada na PB; não representam todos os estudantes da rede."}


def censo():
    zf, f, rows = csv_zip(ZIP_CENSO, "dados/microdados_ed_basica_2024.csv")
    needed = ["SG_UF", "TP_DEPENDENCIA", "CO_ENTIDADE", "CO_MUNICIPIO", "IN_MED", "QT_MAT_MED", *INFRA]
    verificar(rows, needed)
    total = pb = pb_estadual = estadual_em = 0
    escolas, municipios = set(), set()
    repeticoes = 0
    matriculas = 0
    infra = {key: Counter() for key in INFRA}
    faltas = Counter()
    try:
        for r in rows:
            total += 1
            if v(r, "SG_UF") != "PB": continue
            pb += 1
            if v(r, "TP_DEPENDENCIA") != "2": continue
            pb_estadual += 1
            qtd = nfloat(v(r, "QT_MAT_MED"))
            if v(r, "IN_MED") != "1" and not (qtd is not None and qtd > 0):
                continue
            estadual_em += 1
            if qtd is not None and qtd >= 0: matriculas += qtd
            cod = v(r, "CO_ENTIDADE")
            if not cod: faltas["CO_ENTIDADE"] += 1
            elif cod in escolas: repeticoes += 1
            else: escolas.add(cod)
            mun = v(r, "CO_MUNICIPIO")
            if not mun: faltas["CO_MUNICIPIO"] += 1
            else: municipios.add(mun)
            for key in INFRA:
                infra[key][v(r, key) or "(vazio)"] += 1
    finally:
        f.close()
        zf.close()
    return {"registros_nacionais_escolas": total, "escolas_PB": pb,
            "escolas_estaduais_PB": pb_estadual, "escolas_estaduais_ensino_medio_PB": estadual_em,
            "escolas_estaduais_EM_com_codigo": len(escolas), "municipios_estaduais_EM": len(municipios),
            "matriculas_ensino_medio_somadas": int(matriculas),
            "codigos_escola_repetidos_no_recorte": repeticoes, "chaves_vazias": dict(faltas),
            "valores_infraestrutura": {k: dict(counter) for k, counter in infra.items()},
            "alerta": "Cada linha representa uma escola. Matrículas são quantidades declaradas por escola; confirmar conceitos no dicionário."}


def ideb():
    from openpyxl import load_workbook
    with zipfile.ZipFile(BASE / ZIP_IDEB) as zf:
        members = [x for x in zf.infolist() if x.filename.endswith("divulgacao_ensino_medio_escolas_2025.xlsx")]
        if len(members) != 1: raise ValueError("Planilha IDEB não encontrada ou ambígua.")
        with zf.open(members[0]) as f:
            wb = load_workbook(io.BytesIO(f.read()), read_only=True, data_only=True)
            try:
                info = []
                for ws in wb.worksheets:
                    primeiros = []
                    for linha in ws.iter_rows(min_row=1, max_row=15, values_only=True):
                        primeiros.append([{"coluna": i + 1, "texto": str(c)[:100]}
                                         for i, c in enumerate(linha) if c is not None][:18])
                    info.append({"aba": ws.title, "total_linhas_incluindo_cabecalhos": ws.max_row,
                                 "total_colunas": ws.max_column, "amostra_cabecalhos": primeiros})
            finally:
                wb.close()
    return {"planilhas": info, "alerta": "Contagem inclui títulos, cabeçalhos e notas. Ainda não é contagem validada de escolas da PB."}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    out = {"gerado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "fontes": {}, "falhas": {}}
    for name, func in [("PARTICIPANTES_ENEM_2024", participantes),
                       ("RESULTADOS_ENEM_2024", resultados),
                       ("CENSO_ESCOLAR_2024", censo), ("IDEB_2025", ideb)]:
        print("Executando", name, flush=True)
        try:
            out["fontes"][name] = func()
            print("OK:", name, flush=True)
        except Exception as exc:
            out["falhas"][name] = f"{type(exc).__name__}: {exc}"
            print("ERRO:", name, str(exc), flush=True)
    (OUT / "perfil_paraiba.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    partes = ["# Perfil dos dados — Paraíba", "",
              "Relatório agregado, sem linhas individuais e sem junções entre participantes e resultados.",
              "O filtro por escola da rede estadual usa SG_UF_ESC=PB e TP_DEPENDENCIA_ADM_ESC=2.",
              "O filtro de Censo usa SG_UF=PB, TP_DEPENDENCIA=2 e oferta de ensino médio.",
              "As médias do ENEM abrangem apenas participantes com escola identificada e nota válida.",
              "A validade e o significado das variáveis exigem conferência dos dicionários oficiais.",
              ""]
    for name, data in out["fontes"].items():
        partes += ["## " + name, "", "~~~json",
                   json.dumps(data, indent=2, ensure_ascii=False), "~~~", ""]
    if out["falhas"]:
        partes += ["## Erros", "", "~~~json",
                   json.dumps(out["falhas"], indent=2, ensure_ascii=False), "~~~", ""]
    partes += ["## Restrição de integração do ENEM 2024", "",
               "PARTICIPANTES_2024 usa NU_INSCRICAO; RESULTADOS_2024 usa NU_SEQUENCIAL.",
               "Não existe chave comum validada; não juntar por índice ou posição das linhas.",
               "", "## Próximos passos", "",
               "- Conferir códigos e definições dos dicionários oficiais.",
               "- Testar correspondência de CO_ESCOLA com CO_ENTIDADE somente após validar formato e completude.",
               "- Identificar os cabeçalhos e colunas relevantes da planilha IDEB 2025.",
               "- Adicionar os dados ENEM e Censo de 2025 quando disponíveis.", ""]
    (OUT / "perfil_paraiba.md").write_text("\n".join(partes), encoding="utf-8")
    print("Relatório escrito em", OUT, "Falhas:", len(out["falhas"]), flush=True)
    if out["falhas"]: raise SystemExit(1)


if __name__ == "__main__":
    main()
