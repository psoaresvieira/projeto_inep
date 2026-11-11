#!/usr/bin/env python3
"""Issue #2 — filtro reprodutível dos microdados 2024 para a Paraíba.

Lê os ZIPs oficiais em streaming, sem descompactá-los por inteiro.
Os CSVs gerados contêm somente as colunas analíticas necessárias e devem
permanecer no computador, NÃO no GitHub. Estatísticas agregadas são
exportadas em reports/filtragem/.

Uso:
    python src/02_filtragem.py
    python src/02_filtragem.py --somente-resumo
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(20_000_000)

ENEM_ZIP = "microdados_enem_2024.zip"
CENSO_ZIP = "microdados_censo_escolar_2024.zip"
BASE = Path("dados_brutos")
OUTPUT = Path("dados_filtrados")
REPORT = Path("reports/filtragem")

ENEM_COLS = [
    "NU_ANO", "CO_ESCOLA", "CO_MUNICIPIO_ESC", "NO_MUNICIPIO_ESC",
    "CO_UF_ESC", "SG_UF_ESC", "TP_DEPENDENCIA_ADM_ESC",
    "TP_LOCALIZACAO_ESC", "TP_SIT_FUNC_ESC",
    "TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC",
    "TP_PRESENCA_MT", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC",
    "NU_NOTA_MT", "TP_STATUS_REDACAO", "NU_NOTA_REDACAO"
]
CENSO_COLS = [
    "NU_ANO_CENSO", "CO_ENTIDADE", "NO_ENTIDADE", "CO_MUNICIPIO",
    "NO_MUNICIPIO", "SG_UF", "TP_DEPENDENCIA", "TP_LOCALIZACAO",
    "TP_SITUACAO_FUNCIONAMENTO", "IN_MED", "QT_MAT_MED", "QT_DOC_MED",
    "QT_TUR_MED", "IN_INTERNET", "IN_INTERNET_APRENDIZAGEM",
    "IN_BANDA_LARGA", "IN_BIBLIOTECA", "IN_SALA_LEITURA",
    "IN_LABORATORIO_CIENCIAS", "IN_LABORATORIO_INFORMATICA",
    "IN_QUADRA_ESPORTES", "IN_AGUA_POTAVEL"
]
PART_COLS = [
    "NU_ANO", "TP_FAIXA_ETARIA", "TP_SEXO", "TP_ST_CONCLUSAO",
    "TP_ENSINO", "IN_TREINEIRO", "CO_UF_PROVA", "SG_UF_PROVA",
    "CO_MUNICIPIO_PROVA", "Q001", "Q002", "Q005", "Q006", "Q007"
]
CONFIGS = [
    {
        "nome": "enem_escola_estadual_PB_2024",
        "zip": ENEM_ZIP, "suffix": "DADOS/RESULTADOS_2024.csv",
        "colunas": ENEM_COLS,
        "filtro": "SG_UF_ESC=PB e TP_DEPENDENCIA_ADM_ESC=2",
        "tipo": "resultados",
    },
    {
        "nome": "censo_escolas_estaduais_EM_PB_2024",
        "zip": CENSO_ZIP, "suffix": "dados/microdados_ed_basica_2024.csv",
        "colunas": CENSO_COLS,
        "filtro": "SG_UF=PB, TP_DEPENDENCIA=2 e oferta de ensino medio",
        "tipo": "censo",
    },
    {
        "nome": "enem_local_prova_PB_2024",
        "zip": ENEM_ZIP, "suffix": "DADOS/PARTICIPANTES_2024.csv",
        "colunas": PART_COLS,
        "filtro": "SG_UF_PROVA=PB (somente local de prova)",
        "tipo": "participantes",
    },
]


def val(r, name):
    obj = r.get(name)
    return "" if obj is None else str(obj).strip()


def selecionado(r, tipo):
    if tipo == "resultados":
        return val(r, "SG_UF_ESC") == "PB" and val(r, "TP_DEPENDENCIA_ADM_ESC") == "2"
    if tipo == "participantes":
        return val(r, "SG_UF_PROVA") == "PB"
    if tipo == "censo":
        oferta = val(r, "IN_MED") == "1"
        mat = val(r, "QT_MAT_MED")
        try:
            oferta = oferta or float(mat.replace(",", ".")) > 0
        except ValueError:
            pass
        return val(r, "SG_UF") == "PB" and val(r, "TP_DEPENDENCIA") == "2" and oferta
    raise ValueError(f"Tipo de base desconhecido: {tipo}")


def filtrar(config, salvar):
    caminho = BASE / config["zip"]
    if not caminho.exists():
        raise FileNotFoundError(f"Falta {caminho}. Não baixe arquivos diretamente no GitHub.")
    nome = config["nome"]
    saida = OUTPUT / f"{nome}.csv"
    contagem = 0
    selecionadas = 0
    sem_escola = 0
    cidades = set()
    escolas = set()
    with zipfile.ZipFile(caminho) as zf:
        membros = [x for x in zf.namelist() if x.lower().endswith(config["suffix"].lower())]
        if len(membros) != 1:
            raise ValueError(f"{nome}: arquivo interno não localizado unicamente: {config['suffix']}")
        with zf.open(membros[0]) as raw:
            with io.TextIOWrapper(raw, encoding="utf-8-sig", errors="replace", newline="") as f:
                leitor = csv.DictReader(f, delimiter=";")
                faltantes = set(config["colunas"]) - set(leitor.fieldnames or [])
                if faltantes:
                    raise ValueError(f"{nome}: colunas ausentes: {sorted(faltantes)}")
                if salvar:
                    OUTPUT.mkdir(parents=True, exist_ok=True)
                    destino = saida.open("w", newline="", encoding="utf-8-sig")
                    escritor = csv.DictWriter(destino, fieldnames=config["colunas"], delimiter=";")
                    escritor.writeheader()
                else:
                    destino = None
                    escritor = None
                try:
                    for r in leitor:
                        contagem += 1
                        if not selecionado(r, config["tipo"]):
                            continue
                        selecionadas += 1
                        if config["tipo"] in ("resultados", "censo"):
                            key = "CO_ESCOLA" if config["tipo"] == "resultados" else "CO_ENTIDADE"
                            if val(r, key):
                                escolas.add(val(r, key))
                            else:
                                sem_escola += 1
                            mun = "CO_MUNICIPIO_ESC" if config["tipo"] == "resultados" else "CO_MUNICIPIO"
                        else:
                            mun = "CO_MUNICIPIO_PROVA"
                        if val(r, mun):
                            cidades.add(val(r, mun))
                        if escritor:
                            escritor.writerow({c: val(r, c) for c in config["colunas"]})
                finally:
                    if destino:
                        destino.close()
    return {
        "dataset": nome, "arquivo_original": config["zip"], "filtro": config["filtro"],
        "registros_origem": contagem, "registros_selecionados": selecionadas,
        "percentual_selecionado": round(100 * selecionadas / contagem, 3) if contagem else 0,
        "municipios_distintos": len(cidades),
        "escolas_distintas": len(escolas) if config["tipo"] != "participantes" else None,
        "registros_sem_codigo_escola": sem_escola if config["tipo"] != "participantes" else None,
        "colunas_exportadas": config["colunas"], "arquivo_local": str(saida) if salvar else None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--somente-resumo", action="store_true",
                        help="Calcula contagens sem gerar CSVs reduzidos.")
    args = parser.parse_args()
    resumo = {
        "data_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "aviso": "Os datasets do ENEM são distintos: a base de local de prova NÃO tem vínculo individual validado com a base de notas. Não associar as linhas por posição.",
        "bases": [], "erros": [],
    }
    for config in CONFIGS:
        print("Filtrando", config["nome"], flush=True)
        try:
            res = filtrar(config, not args.somente_resumo)
            resumo["bases"].append(res)
            print("Selecionados", res["registros_selecionados"], "de", res["registros_origem"])
        except Exception as exc:
            print("ERRO:", str(exc), flush=True)
            resumo["erros"].append({"dataset": config["nome"], "mensagem": str(exc)})
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / "resumo_2024.json").write_text(
        json.dumps(resumo, indent=2, ensure_ascii=False), encoding="utf-8")
    texto = [
        "# Relatório de filtragem — INEP Paraíba (2024)", "",
        "Filtros aplicados diretamente nos microdados oficiais, em streaming.", "",
        "| Base | Origem | Selecionados | Municípios distintos | Escolas distintas |",
        "|---|---:|---:|---:|---:|",
    ]
    for b in resumo["bases"]:
        texto.append(
            f"| {b['dataset']} | {b['registros_origem']} | {b['registros_selecionados']} | "
            f"{b['municipios_distintos']} | {b['escolas_distintas'] if b['escolas_distintas'] is not None else 'N/A'} |"
        )
    texto += [
        "", "## Interpretação dos recortes", "",
        "- ENEM Resultados: participantes com escola identificada como estadual na Paraíba; não representa todos os alunos.",
        "- Censo Escolar: escolas estaduais que ofertam ensino médio, conforme campos da edição.",
        "- ENEM Participantes: candidatos cujo município da prova está na Paraíba. Isso não significa que estudaram na Paraíba.",
        "- Não cruzar linhas dos arquivos de participantes e resultados sem chave individual documentada.",
        "", "## Fontes", "",
        "- [ENEM](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem)",
        "- [Censo Escolar](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar)",
        "", "## Erros", "",
    ]
    texto.extend(f"- {x['dataset']}: {x['mensagem']}" for x in resumo["erros"])
    if not resumo["erros"]:
        texto.append("- Nenhum erro na execução.")
    (REPORT / "resumo_2024.md").write_text("\n".join(texto) + "\n", encoding="utf-8")
    if resumo["erros"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
