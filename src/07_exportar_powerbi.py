#!/usr/bin/env python3
"""Exporta apenas indicadores agregados e auditados para importação no Power BI.

Origem: relatórios existentes neste repositório, sem baixar microdados individuais.
Censo 2024 e IDEB 2025 permanecem em tabelas distintas e por ano.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MUNICIPIOS = ROOT / "reports/municipios/municipios_agregados.json"
ENEM = ROOT / "reports/inspecao/perfil_paraiba.md"
CHAVES = ROOT / "reports/filtragem/validacao_chaves_2024.md"
OUTPUT = ROOT / "powerbi/dados"
RECURSOS = {
    "IN_INTERNET": "Internet",
    "IN_BANDA_LARGA": "Banda larga",
    "IN_BIBLIOTECA": "Biblioteca",
    "IN_LABORATORIO_CIENCIAS": "Laboratório de ciências",
    "IN_LABORATORIO_INFORMATICA": "Laboratório de informática",
    "IN_QUADRA_ESPORTES": "Quadra de esportes",
    "IN_AGUA_POTAVEL": "Água potável",
}
AREAS = {
    "NU_NOTA_CN": "Ciências da Natureza",
    "NU_NOTA_CH": "Ciências Humanas",
    "NU_NOTA_LC": "Linguagens",
    "NU_NOTA_MT": "Matemática",
    "NU_NOTA_REDACAO": "Redação",
}


def escrever_csv(path: Path, cabecalho: list[str], linhas: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        writer.writerow(cabecalho)
        for linha in linhas:
            assert len(linha) == len(cabecalho), (path, linha)
            writer.writerow(["" if value is None else str(value).replace(".", ",")
                             if isinstance(value, float) else value for value in linha])


def secao_json(markdown: str, nome: str) -> dict:
    expressao = rf"(?ms)^## {re.escape(nome)}\s*\n\s*~~~json\s*\n(.*?)\n~~~"
    resultado = re.search(expressao, markdown)
    if not resultado:
        raise ValueError("Bloco agregado ausente: " + nome)
    return json.loads(resultado.group(1))


def valor_tabela(markdown: str, metrica: str) -> int:
    expressao = rf"(?m)^\|\s*{re.escape(metrica)}\s*\|\s*([0-9]+)\s*\|"
    resultado = re.search(expressao, markdown)
    if not resultado:
        raise ValueError("Métrica da auditoria ausente: " + metrica)
    return int(resultado.group(1))


def construir(base: dict, desempenho: dict, auditoria: dict, destino: Path) -> dict:
    municipios = base["municipios"]
    total = base["totais"]
    if len(municipios) != total["municipios"]:
        raise ValueError("Quantidade municipal divergente")
    codigos = [m["codigo_municipio"] for m in municipios]
    if len(set(codigos)) != len(codigos) or any(len(c) != 7 or not c.isdigit() for c in codigos):
        raise ValueError("Código IBGE duplicado ou inválido")
    if sum(m["censo_2024"]["escolas"] for m in municipios) != total["escolas_censo_2024"]:
        raise ValueError("Total de escolas Censo divergente")
    if sum(m["censo_2024"]["matriculas"] for m in municipios) != total["matriculas_censo_2024"]:
        raise ValueError("Total de matrículas divergente")
    if sum(m["ideb_2025"]["escolas"] for m in municipios) != total["escolas_ideb_2025"]:
        raise ValueError("Total de escolas IDEB divergente")
    if sum(m["ideb_2025"]["notas_validas"] for m in municipios) != total["notas_validas_ideb_2025"]:
        raise ValueError("Total de notas válidas IDEB divergente")
    if auditoria["escolas_distintas_censo"] != total["escolas_censo_2024"]:
        raise ValueError("Auditoria escolar e Censo divergem")
    if auditoria["linhas_enem_com_correspondencia_escolar"] > auditoria["linhas_participantes_enem_com_codigo"]:
        raise ValueError("Correspondência escolar inválida")
    if auditoria["escolas_em_ambas_as_bases"] > min(
        auditoria["escolas_distintas_censo"], auditoria["escolas_distintas_enem_resultados"]
    ):
        raise ValueError("Número de escolas pareadas impossível")

    dimensao, censo, infra, ideb = [], [], [], []
    for m in municipios:
        cod = m["codigo_municipio"]
        dimensao.append([cod, m["nome_municipio"], "PB"])
        c = m["censo_2024"]
        d = m["ideb_2025"]
        censo.append([cod, 2024, c["escolas"], c["matriculas"],
                      c["matriculas_nao_informadas"]])
        for chave, nome in RECURSOS.items():
            r = c["infraestrutura"][chave]
            sim, nao, ausente = r["sim"], r["nao"], r["sem_informacao"]
            if sim + nao + ausente != c["escolas"]:
                raise ValueError(f"Denominador inconsistente: {cod} / {chave}")
            infra.append([cod, 2024, chave, nome, sim, nao, ausente, c["escolas"]])
        if d["notas_validas"] + d["sem_nota"] != d["escolas"]:
            raise ValueError(f"IDEB inválido: {cod}")
        suprimida = d["media_suprimida_grupo_pequeno"]
        if suprimida and (d["media_simples"] is not None or d["mediana"] is not None):
            raise ValueError(f"Supressão IDEB violada: {cod}")
        if d["notas_validas"] < base["supressao_ideb_municipio_minimo_notas"] and (
            d["media_simples"] is not None or d["mediana"] is not None
        ):
            raise ValueError(f"Média divulgada para grupo pequeno: {cod}")
        ideb.append([cod, 2025, d["escolas"], d["notas_validas"],
                     d["sem_nota"], d["media_simples"], d["mediana"],
                     1 if suprimida else 0])

    notas = desempenho["notas_de_participantes_com_escola_estadual_PB"]
    enem = []
    for campo, nome in AREAS.items():
        info = notas[campo]
        if not (0 < info["validas"] <= desempenho["escola_estadual_na_PB"]):
            raise ValueError(f"Quantidade ENEM inválida: {campo}")
        enem.append([2024, campo, nome, info["validas"], info["media"]])
    if desempenho["escola_estadual_na_PB"] != auditoria["linhas_participantes_enem_com_codigo"]:
        raise ValueError("Recorte ENEM difere da auditoria")

    cobertura = [[2024, auditoria["escolas_distintas_censo"],
                  auditoria["escolas_distintas_enem_resultados"],
                  auditoria["escolas_em_ambas_as_bases"],
                  auditoria["linhas_participantes_enem_com_codigo"],
                  auditoria["linhas_enem_com_correspondencia_escolar"]]]

    arquivos = {
        "dim_municipio.csv": (["codigo_municipio", "municipio", "uf"], dimensao),
        "fato_censo_municipio_2024.csv": (
            ["codigo_municipio", "ano", "escolas_ensino_medio", "matriculas_declaradas",
             "escolas_matriculas_nao_informadas"], censo),
        "fato_infra_municipio_2024.csv": (
            ["codigo_municipio", "ano", "codigo_recurso", "recurso", "escolas_sim",
             "escolas_nao", "escolas_sem_informacao", "total_escolas"], infra),
        "fato_ideb_municipio_2025.csv": (
            ["codigo_municipio", "ano", "escolas_ideb", "escolas_nota_valida",
             "escolas_sem_nota", "media_simples_escolas", "mediana_escolas",
             "media_suprimida"], ideb),
        "fato_enem_areas_2024.csv": (
            ["ano", "codigo_area", "area", "notas_validas", "media_notas_validas"], enem),
        "fato_cobertura_escolar_2024.csv": (
            ["ano", "escolas_censo", "escolas_enem", "escolas_pareadas",
             "registros_enem_com_codigo_escola", "registros_enem_pareados"], cobertura),
    }
    for nome, (cabecalho, linhas) in arquivos.items():
        escrever_csv(destino / nome, cabecalho, linhas)
    manifesto = {
        "origem": ["reports/municipios/municipios_agregados.json",
                   "reports/inspecao/perfil_paraiba.md",
                   "reports/filtragem/validacao_chaves_2024.md"],
        "abrangencia": "Ensino médio estadual da Paraíba; ENEM restrito a participantes com escola estadual identificada",
        "fonte": {"censo": "INEP, Censo Escolar 2024",
                  "ideb": "INEP, IDEB escolar 2025",
                  "enem": "INEP, ENEM 2024"},
        "tabelas_linhas": {nome: len(linhas) for nome, (_, linhas) in arquivos.items()},
        "alertas": [
            "Censo 2024 e IDEB 2025 têm anos e universos distintos; não correlacionar como mesmo período.",
            "Médias de IDEB municipal são médias simples escolares, NÃO IDEB oficial agregado da rede.",
            "Médias do IDEB com menos de 3 notas válidas estão suprimidas, nunca imputar.",
            "Médias ENEM não representam todos os estudantes da rede.",
            "Para percentuais de infraestrutura por grupo, somar escolas_sim e total_escolas APENAS por um recurso.",
            "Códigos IBGE de município devem ser texto, com relacionamento 1:N da dimensão às tabelas municipais.",
        ],
    }
    (destino / "manifesto.json").write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifesto


def main() -> None:
    municipios = json.loads(MUNICIPIOS.read_text(encoding="utf-8"))
    desempenho = secao_json(ENEM.read_text(encoding="utf-8"), "RESULTADOS_ENEM_2024")
    auditoria_md = CHAVES.read_text(encoding="utf-8")
    campos = ["escolas_distintas_censo", "escolas_distintas_enem_resultados",
              "escolas_em_ambas_as_bases", "linhas_participantes_enem_com_codigo",
              "linhas_enem_com_correspondencia_escolar"]
    auditoria = {campo: valor_tabela(auditoria_md, campo) for campo in campos}
    manifesto = construir(municipios, desempenho, auditoria, OUTPUT)
    print("Arquivos Power BI gerados:", manifesto["tabelas_linhas"])


if __name__ == "__main__":
    main()
