#!/usr/bin/env python3
"""Agrega por município: infraestrutura Censo 2024 e IDEB 2025 (anos separados).

Não combina linhas individuais entre anos nem publica registros escolares.
Notas IDEB de municípios com menos de 3 resultados válidos são suprimidas.
"""
from __future__ import annotations
import csv
import io
import json
import statistics
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from openpyxl import load_workbook

BASE = Path("dados_brutos")
OUT = Path("reports/municipios")
INFRA = ("IN_INTERNET", "IN_BANDA_LARGA", "IN_BIBLIOTECA",
         "IN_LABORATORIO_CIENCIAS", "IN_LABORATORIO_INFORMATICA",
         "IN_QUADRA_ESPORTES", "IN_AGUA_POTAVEL")
MIN_IDEB = 3


def valor(x):
    return "" if x is None else str(x).strip()


def inteiro(x):
    try:
        n = int(valor(x))
        return n if n >= 0 else None
    except ValueError:
        return None


def nota(x):
    try:
        n = float(valor(x).replace(",", "."))
        return n if 0 <= n <= 10 else None
    except ValueError:
        return None


def novo():
    return {
        "nome": "",
        "censo": {"escolas": 0, "matriculas": 0, "matriculas_nao_informadas": 0,
                  "infraestrutura": {k: {"sim": 0, "nao": 0, "sem_informacao": 0} for k in INFRA}},
        "ideb": {"escolas": 0, "notas_validas": 0, "sem_nota": 0, "_notas": []},
    }


def ler_censo(pasta=BASE):
    municipios = defaultdict(novo)
    escolas = set()
    with zipfile.ZipFile(pasta / "microdados_censo_escolar_2024.zip") as z:
        members = [x for x in z.infolist() if x.filename.lower().endswith("dados/microdados_ed_basica_2024.csv")]
        if len(members) != 1:
            raise ValueError("Arquivo principal Censo 2024 não localizado")
        with z.open(members[0]) as raw:
            with io.TextIOWrapper(raw, encoding="latin-1", newline="") as file:
                reader = csv.DictReader(file, delimiter=";")
                expected = {"NU_ANO_CENSO", "SG_UF", "TP_DEPENDENCIA", "CO_ENTIDADE",
                            "CO_MUNICIPIO", "NO_MUNICIPIO", "IN_MED", "QT_MAT_MED", *INFRA}
                if not expected.issubset(reader.fieldnames or []):
                    raise ValueError("Colunas Censo ausentes: " + str(expected - set(reader.fieldnames or [])))
                for row in reader:
                    if valor(row["SG_UF"]) != "PB" or valor(row["TP_DEPENDENCIA"]) != "2":
                        continue
                    mat = inteiro(row["QT_MAT_MED"])
                    if valor(row["IN_MED"]) != "1" and not (mat is not None and mat > 0):
                        continue
                    if valor(row["NU_ANO_CENSO"]) != "2024":
                        raise ValueError("Ano Censo divergente")
                    mun, escola = valor(row["CO_MUNICIPIO"]), valor(row["CO_ENTIDADE"])
                    if len(mun) != 7 or not mun.isdigit() or not escola.isdigit():
                        raise ValueError("Código escolar ou município inválido")
                    if escola in escolas:
                        raise ValueError("Código de escola duplicado no Censo")
                    escolas.add(escola)
                    m = municipios[mun]
                    m["nome"] = valor(row["NO_MUNICIPIO"])
                    c = m["censo"]
                    c["escolas"] += 1
                    if mat is None:
                        c["matriculas_nao_informadas"] += 1
                    else:
                        c["matriculas"] += mat
                    for k in INFRA:
                        v = valor(row[k])
                        estado = "sim" if v == "1" else "nao" if v == "0" else "sem_informacao"
                        c["infraestrutura"][k][estado] += 1
    return municipios, len(escolas)


def ler_ideb(municipios, pasta=BASE):
    escolas = set()
    with zipfile.ZipFile(pasta / "divulgacao_ensino_medio_escolas_2025.zip") as z:
        matches = [x for x in z.infolist()
                   if x.filename.endswith("divulgacao_ensino_medio_escolas_2025.xlsx")]
        if len(matches) != 1:
            raise ValueError("Planilha IDEB 2025 não encontrada")
        with z.open(matches[0]) as raw:
            wb = load_workbook(io.BytesIO(raw.read()), read_only=True, data_only=True)
    try:
        rows = iter(wb.worksheets[0].iter_rows(values_only=True))
        header = None
        for row in rows:
            cols = [valor(v) for v in row]
            if len(cols) >= 6 and cols[0] == "SG_UF" and cols[3] == "ID_ESCOLA":
                header = {name: i for i, name in enumerate(cols) if name}
                break
        required = {"SG_UF", "CO_MUNICIPIO", "NO_MUNICIPIO", "ID_ESCOLA",
                    "REDE", "VL_OBSERVADO_2025"}
        if header is None or not required.issubset(header):
            raise ValueError("Campos técnicos IDEB 2025 indisponíveis")
        for row in rows:
            if valor(row[header["SG_UF"]]) != "PB" or valor(row[header["REDE"]]).casefold() != "estadual":
                continue
            school = valor(row[header["ID_ESCOLA"]])
            if not school:
                continue
            if school in escolas:
                raise ValueError("Escola duplicada no IDEB")
            escolas.add(school)
            code = valor(row[header["CO_MUNICIPIO"]])
            if len(code) != 7 or not code.isdigit():
                raise ValueError("Município inválido no IDEB")
            grupo = municipios[code]
            if not grupo["nome"]:
                grupo["nome"] = valor(row[header["NO_MUNICIPIO"]])
            d = grupo["ideb"]
            d["escolas"] += 1
            n = nota(row[header["VL_OBSERVADO_2025"]])
            if n is None:
                d["sem_nota"] += 1
            else:
                d["notas_validas"] += 1
                d["_notas"].append(n)
    finally:
        wb.close()
    return len(escolas)


def montar(municipios, quantidade_censo, quantidade_ideb):
    if quantidade_censo != 482 or quantidade_ideb != 478:
        raise ValueError("Totais incompatíveis com Censo 2024 ou IDEB 2025 publicados")
    dados = []
    for code, row in sorted(municipios.items(), key=lambda item: (item[1]["nome"], item[0])):
        c, d = row["censo"], row["ideb"]
        notas = d.pop("_notas")
        d["media_simples"] = round(statistics.mean(notas), 3) if len(notas) >= MIN_IDEB else None
        d["mediana"] = round(statistics.median(notas), 3) if len(notas) >= MIN_IDEB else None
        d["media_suprimida_grupo_pequeno"] = 0 < len(notas) < MIN_IDEB
        for k, v in c["infraestrutura"].items():
            if sum(v.values()) != c["escolas"]:
                raise ValueError("Infraestrutura não confere: " + code + " " + k)
        dados.append({"codigo_municipio": code, "nome_municipio": row["nome"],
                      "censo_2024": c, "ideb_2025": d})
    matriculas = sum(x["censo_2024"]["matriculas"] for x in dados)
    validas = sum(x["ideb_2025"]["notas_validas"] for x in dados)
    if matriculas != 116779 or validas != 458:
        raise ValueError("Matrículas ou notas IDEB não coincidem com relatórios publicados")
    return {
        "gerado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "aviso": "Bases de anos e universos diferentes: agregadas por município, sem junção de escolas ou inferência causal.",
        "supressao_ideb_municipio_minimo_notas": MIN_IDEB,
        "totais": {"municipios": len(dados), "escolas_censo_2024": quantidade_censo,
                   "matriculas_censo_2024": matriculas, "escolas_ideb_2025": quantidade_ideb,
                   "notas_validas_ideb_2025": validas},
        "municipios": dados,
    }


def executar(pasta=BASE):
    municipios, censo = ler_censo(pasta)
    ideb = ler_ideb(municipios, pasta)
    return montar(municipios, censo, ideb)


def salvar(resultado, pasta=OUT):
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "municipios_agregados.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    t = resultado["totais"]
    md = [
        "# Indicadores territoriais da educação estadual — Paraíba", "",
        "Censo Escolar 2024 e IDEB 2025 em visões separadas, agregados por código IBGE do município.",
        "Não foram relacionados registros escolares entre anos nem atribuídos resultados individuais.", "",
        "| Indicador | Total |", "|---|---:|",
        f"| Municípios com escolas registradas | {t['municipios']} |",
        f"| Escolas estaduais com EM no Censo 2024 | {t['escolas_censo_2024']} |",
        f"| Matrículas declaradas no recorte 2024 | {t['matriculas_censo_2024']} |",
        f"| Escolas estaduais na planilha IDEB 2025 | {t['escolas_ideb_2025']} |",
        f"| Escolas com IDEB 2025 válido | {t['notas_validas_ideb_2025']} |", "",
        "## Procedimento", "",
        "- O denominador da infraestrutura é o número de escolas estaduais com EM do município em 2024.",
        "- Valores 0, 1 e ausentes das variáveis de infraestrutura são mantidos separadamente.",
        "- IDEB 2025 não é misturado com o Censo 2024 em análises de escola.",
        "- Médias/medianas municipais do IDEB são ocultadas se houver menos de três notas válidas.",
        "- Média simples do IDEB não equivale ao indicador oficial agregado da rede.", "",
        "O arquivo municipios_agregados.json contém somente os resultados agregados por município.",
        "Fonte: INEP, Censo Escolar 2024 e resultados IDEB 2025.", "",
    ]
    (pasta / "resumo_municipios.md").write_text("\n".join(md), encoding="utf-8")


def main():
    dados = executar()
    salvar(dados)
    print(json.dumps(dados["totais"], ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
