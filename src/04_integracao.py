#!/usr/bin/env python3
"""Issue #4: integração escolar ENEM–Censo 2024, com auditoria e agregação.

Usa apenas RESULTADOS do ENEM e Censo (ambos recortados para a rede estadual
da PB). Nunca relaciona RESULTADOS a PARTICIPANTES pela posição das linhas.

Saída escolar agregada é PRIVADA, em dados_integrados/.
Relatório público agrega apenas contagens globais sem identificar alunos.
"""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("dados_limpos")
AUDIT = Path("reports/filtragem/validacao_chaves_2024.json")
OUTPUT = Path("dados_integrados")
REPORT = Path("reports/integracao")
CENSO = BASE / "censo_escolas_estaduais_EM_PB_2024_limpo.csv"
ENEM = BASE / "enem_escola_estadual_PB_2024_limpo.csv"
NOTAS = {
    "NU_NOTA_CN": "TP_PRESENCA_CN",
    "NU_NOTA_CH": "TP_PRESENCA_CH",
    "NU_NOTA_LC": "TP_PRESENCA_LC",
    "NU_NOTA_MT": "TP_PRESENCA_MT",
    "NU_NOTA_REDACAO": "TP_STATUS_REDACAO",
}
MIN_N = 5


def valor(r, campo):
    v = r.get(campo)
    return "" if v is None else str(v).strip()


def validar_nota(texto):
    try:
        val = float(texto.replace(",", "."))
    except (ValueError, AttributeError):
        return None
    return val if 0 <= val <= 1000 else None


def ler_censo(path):
    dados = {}
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        obrig = {"CO_ENTIDADE", "CO_MUNICIPIO", "SG_UF", "TP_DEPENDENCIA", "NU_ANO_CENSO"}
        if not obrig.issubset(reader.fieldnames or []):
            raise ValueError("Colunas do Censo ausentes: " + str(obrig - set(reader.fieldnames or [])))
        for r in reader:
            codigo = valor(r, "CO_ENTIDADE")
            if not codigo or not codigo.isdigit():
                raise ValueError("Código de escola vazio ou inválido no Censo; integração bloqueada.")
            if codigo in dados:
                raise ValueError(f"Escola duplicada no Censo: {codigo}; integração bloqueada.")
            if (valor(r, "SG_UF"), valor(r, "TP_DEPENDENCIA"),
                valor(r, "NU_ANO_CENSO")) != ("PB", "2", "2024"):
                raise ValueError("Linha do Censo fora do recorte PB/rede estadual/2024.")
            dados[codigo] = r
    if not dados:
        raise ValueError("Censo escolar vazio.")
    return dados


def ler_enem(path):
    dados = defaultdict(lambda: {"registros": 0,
        "notas": {k: {"n": 0, "soma": 0.0} for k in NOTAS}})
    total = 0
    com_codigo = 0
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        obrig = {"CO_ESCOLA", "SG_UF_ESC", "TP_DEPENDENCIA_ADM_ESC", "NU_ANO", *NOTAS}
        if not obrig.issubset(reader.fieldnames or []):
            raise ValueError("Colunas do ENEM ausentes: " + str(obrig - set(reader.fieldnames or [])))
        for r in reader:
            total += 1
            if (valor(r, "SG_UF_ESC"), valor(r, "TP_DEPENDENCIA_ADM_ESC"),
                valor(r, "NU_ANO")) != ("PB", "2", "2024"):
                raise ValueError("Linha ENEM fora do recorte PB/rede estadual/2024.")
            codigo = valor(r, "CO_ESCOLA")
            if not codigo:
                continue
            if not codigo.isdigit():
                raise ValueError("Código de escola não numérico no ENEM.")
            com_codigo += 1
            dados[codigo]["registros"] += 1
            for nota, campo_status in NOTAS.items():
                n = validar_nota(valor(r, nota))
                if n is None or valor(r, campo_status) != "1":
                    continue
                dados[codigo]["notas"][nota]["n"] += 1
                dados[codigo]["notas"][nota]["soma"] += n
    if not total:
        raise ValueError("ENEM resultados vazio.")
    return dados, total, com_codigo


def integrar(censo_path=CENSO, enem_path=ENEM, auditoria_path=AUDIT, saida=OUTPUT):
    if not auditoria_path.is_file():
        raise FileNotFoundError("Falta auditoria de chaves da Issue #2.")
    audit = json.loads(auditoria_path.read_text(encoding="utf-8"))
    if audit.get("codigos_censo_duplicados") != 0:
        raise ValueError("Auditoria informa duplicidades no Censo. Integração bloqueada.")
    if audit.get("validade_juncao") != "CANDIDATA_APROVADA_PARA_ANÁLISE_POR_ESCOLA":
        raise ValueError("Chave escolar não foi aprovada na auditoria da Issue #2.")

    escolas = ler_censo(censo_path)
    desempenho, registros, com_codigo = ler_enem(enem_path)
    codigos_censo, codigos_enem = set(escolas), set(desempenho)
    correspondentes = codigos_censo & codigos_enem
    registros_pareados = sum(desempenho[c]["registros"] for c in correspondentes)
    # Confere o relatório da filtragem para detectar relatório antigo ou arquivo misturado.
    if audit.get("escolas_em_ambas_as_bases") != len(correspondentes):
        raise ValueError("A auditoria de chaves não corresponde aos dados usados na integração.")
    if audit.get("linhas_enem_com_correspondencia_escolar") != registros_pareados:
        raise ValueError("Quantidade de linhas pareadas não coincide com a auditoria.")
    if audit.get("linhas_participantes_enem_com_codigo") != com_codigo:
        raise ValueError("Contagem ENEM diverge da auditoria. Não integrar.")

    colunas_base = [
        "NU_ANO_CENSO", "CO_ENTIDADE", "CO_MUNICIPIO", "NO_MUNICIPIO",
        "TP_DEPENDENCIA", "TP_LOCALIZACAO", "IN_MED", "QT_MAT_MED",
        "QT_DOC_MED", "QT_TUR_MED", "IN_INTERNET", "IN_BIBLIOTECA",
        "IN_LABORATORIO_CIENCIAS", "IN_LABORATORIO_INFORMATICA",
        "IN_BANDA_LARGA", "IN_QUADRA_ESPORTES",
    ]
    colunas_notas = []
    for nota in NOTAS:
        colunas_notas.extend((nota + "_n_publicavel", nota + "_media_publicavel"))
    campos = colunas_base + ["tem_participantes_enem", "ano_enem"] + colunas_notas
    saida.mkdir(parents=True, exist_ok=True)
    destino = saida / "base_escolar_enem_censo_PB_2024.csv"
    suprimidas = Counter()
    publicaveis = Counter()

    with destino.open("w", encoding="utf-8-sig", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos, delimiter=";")
        escritor.writeheader()
        for codigo, c in sorted(escolas.items()):
            dado_enem = desempenho.get(codigo)
            row = {key: valor(c, key) for key in colunas_base}
            row["tem_participantes_enem"] = "1" if dado_enem else "0"
            row["ano_enem"] = "2024"
            for nota in NOTAS:
                n = dado_enem["notas"][nota]["n"] if dado_enem else 0
                soma = dado_enem["notas"][nota]["soma"] if dado_enem else 0
                if n >= MIN_N:
                    row[nota + "_n_publicavel"] = str(n)
                    row[nota + "_media_publicavel"] = str(round(soma / n, 2))
                    publicaveis[nota] += 1
                else:
                    row[nota + "_n_publicavel"] = ""
                    row[nota + "_media_publicavel"] = ""
                    if dado_enem and n:
                        suprimidas[nota] += 1
            escritor.writerow(row)
    return {
        "ano_censo": 2024, "ano_enem": 2024,
        "escolas_censo": len(codigos_censo),
        "escolas_enem": len(codigos_enem),
        "escolas_com_correspondencia": len(correspondentes),
        "escolas_censo_sem_enem": len(codigos_censo - codigos_enem),
        "escolas_enem_sem_censo": len(codigos_enem - codigos_censo),
        "linhas_enem_no_recorte": registros,
        "linhas_enem_com_codigo": com_codigo,
        "linhas_enem_pareadas": registros_pareados,
        "linhas_enem_nao_pareadas_com_codigo": com_codigo - registros_pareados,
        "escolas_com_nota_e_n_suficientes": dict(publicaveis),
        "escolas_com_n_pequeno_suprimido": dict(suprimidas),
        "minimo_notas_validas_para_media_escolar": MIN_N,
        "arquivo_escolar_privado": str(destino),
        "observacao": "Junção por código de escola do mesmo ano após validação. Médias por escola apenas com n>=5; nunca vinculou questionário socioeconômico ao desempenho. Não interpretar causalmente.",
    }


def main():
    resumo = integrar()
    REPORT.mkdir(parents=True, exist_ok=True)
    resumo["gerado_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    (REPORT / "integracao_2024.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# Integração ENEM–Censo 2024 por escola — Paraíba", "",
        "Indicadores agregados; a base escolar detalhada não é publicada no GitHub.", "",
        "| Métrica | Valor |", "|---|---:|",
    ]
    for key, value in resumo.items():
        if isinstance(value, (str, list, dict)):
            continue
        lines.append(f"| {key} | {value} |")
    lines += ["", "## Regras", "",
              "- Chaves: CO_ESCOLA do ENEM RESULTADOS → CO_ENTIDADE do Censo, ambos 2024.",
              "- A auditoria valida unicidade do Censo, correspondência de códigos e contagens.",
              "- Unidades: escolas (não indivíduos). A base final é uma linha por escola do Censo.",
              "- Médias por escola são omitidas com menos de cinco notas válidas da área.",
              "- Apenas participantes com presença igual a 1 e nota numérica válida entram na média.",
              "- Dados de PARTICIPANTES ENEM não foram relacionados ao RESULTADOS ENEM.", "",
              "## Atenção", "",
              "Métricas do ENEM refletem participantes identificados, não todos os alunos da escola.",
              "A correspondência da chave não demonstra representatividade nem causalidade.", ""]
    (REPORT / "integracao_2024.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
