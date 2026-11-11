#!/usr/bin/env python3
"""Issue #3: auditoria e limpeza conservadora dos recortes ENEM/Censo 2024.

Entradas privadas em dados_filtrados/; saídas privadas em dados_limpos/.
Somente relatórios agregados (sem linhas de participantes) em reports/qualidade/.
Não remove registros, não preenche nulos com zero e não altera ZIPs originais.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

INPUT = Path("dados_filtrados")
OUTPUT = Path("dados_limpos")
REPORT = Path("reports/qualidade")
csv.field_size_limit(20_000_000)

CONFIG = {
    "enem": ("enem_escola_estadual_PB_2024.csv", "CO_ESCOLA"),
    "censo": ("censo_escolas_estaduais_EM_PB_2024.csv", "CO_ENTIDADE"),
    "participantes": ("enem_local_prova_PB_2024.csv", None),
}
NOTAS = {
    "NU_NOTA_CN": "TP_PRESENCA_CN",
    "NU_NOTA_CH": "TP_PRESENCA_CH",
    "NU_NOTA_LC": "TP_PRESENCA_LC",
    "NU_NOTA_MT": "TP_PRESENCA_MT",
    "NU_NOTA_REDACAO": None,
}
INFRAESTRUTURA = (
    "IN_INTERNET", "IN_INTERNET_APRENDIZAGEM", "IN_BANDA_LARGA",
    "IN_BIBLIOTECA", "IN_SALA_LEITURA", "IN_LABORATORIO_CIENCIAS",
    "IN_LABORATORIO_INFORMATICA", "IN_QUADRA_ESPORTES", "IN_AGUA_POTAVEL",
)


def str_valor(v):
    return "" if v is None else str(v).strip()


def validar_codigo(v):
    """Código íntegro; não converter para int (preserva eventuais zeros à esquerda)."""
    s = str_valor(v)
    return s if s.isdigit() else ""


def validar_nota(v):
    """Retorna (texto normalizado, categoria de qualidade).

    Zero é nota possível; string vazia permanece ausente.
    Não infere presença só pelo valor da nota.
    """
    s = str_valor(v)
    if s == "":
        return "", "ausente"
    try:
        nota = float(s.replace(",", "."))
    except ValueError:
        return "", "invalida_nao_numerica"
    if not (0 <= nota <= 1000):
        return "", "invalida_fora_da_faixa"
    return str(nota), "valida"


def validar_quantidade(v):
    s = str_valor(v)
    if s == "":
        return "", "ausente"
    try:
        n = int(s)
    except ValueError:
        return "", "invalida"
    if n < 0:
        return "", "invalida"
    return str(n), "valida"


def limpar_linha(tipo, row, estat):
    r = {k: str_valor(v) for k, v in row.items()}
    chave = CONFIG[tipo][1]
    if chave:
        orig = r.get(chave, "")
        normal = validar_codigo(orig)
        if orig and not normal:
            estat["codigo_escola_invalido"] += 1
        if not orig:
            estat["codigo_escola_vazio"] += 1
        r[chave] = normal
    if tipo == "enem":
        for nota, presenca in NOTAS.items():
            if nota not in r:
                continue
            novo, categoria = validar_nota(r[nota])
            estat[f"{nota}:{categoria}"] += 1
            if presenca and presenca in r:
                p = r[presenca]
                estat[f"{presenca}:{p or '(vazio)'}"] += 1
                if categoria == "valida" and p != "1":
                    estat[f"{nota}:nota_com_presenca_diferente_de_1"] += 1
                elif categoria == "ausente" and p == "1":
                    estat[f"{nota}:ausencia_com_presenca_1"] += 1
            r[nota] = novo
    if tipo == "censo":
        for coluna in INFRAESTRUTURA:
            if coluna in r:
                valor = r[coluna]
                estat[f"{coluna}:{valor or '(vazio)'}"] += 1
                if valor and valor not in {"0", "1"}:
                    estat[f"{coluna}:categoria_nao_binaria"] += 1
        for coluna in ("QT_MAT_MED", "QT_DOC_MED", "QT_TUR_MED"):
            if coluna in r:
                novo, categoria = validar_quantidade(r[coluna])
                estat[f"{coluna}:{categoria}"] += 1
                r[coluna] = novo
    return r


def processar(tipo, pasta_entrada=INPUT, pasta_saida=OUTPUT):
    arquivo, chave = CONFIG[tipo]
    caminho = pasta_entrada / arquivo
    if not caminho.is_file():
        raise FileNotFoundError(f"Arquivo filtrado não encontrado: {caminho}")
    pasta_saida.mkdir(parents=True, exist_ok=True)
    destino = pasta_saida / arquivo.replace(".csv", "_limpo.csv")
    estat = Counter()
    codigos = set()
    duplicados = 0
    total = 0
    vazio_por_coluna = Counter()
    with caminho.open(encoding="utf-8-sig", newline="") as fin:
        leitor = csv.DictReader(fin, delimiter=";")
        cols = leitor.fieldnames
        if not cols:
            raise ValueError(f"{arquivo}: cabeçalho ausente")
        if chave and chave not in cols:
            raise ValueError(f"{arquivo}: código de escola ausente: {chave}")
        with destino.open("w", encoding="utf-8-sig", newline="") as fout:
            escritor = csv.DictWriter(fout, fieldnames=cols, delimiter=";")
            escritor.writeheader()
            for item in leitor:
                total += 1
                row = limpar_linha(tipo, item, estat)
                for k, val in row.items():
                    if not val:
                        vazio_por_coluna[k] += 1
                if chave and tipo == "censo" and row[chave]:
                    if row[chave] in codigos:
                        duplicados += 1
                    else:
                        codigos.add(row[chave])
                escritor.writerow(row)
    resultado = {
        "arquivo_entrada": str(caminho),
        "arquivo_saida_privado": str(destino),
        "registros": total,
        "colunas": len(cols),
        "campos_vazios_por_coluna": dict(vazio_por_coluna),
        "ocorrencias_de_qualidade": dict(estat),
        "codigos_censo_duplicados": duplicados if tipo == "censo" else None,
        "metodo": "Normalizacao por strip; codigos nao numericos anulados; notas invalidas anuladas; nenhuma linha excluida.",
        "avisos": [
            "Nulos não foram substituídos por zero.",
            "Presença, ausência e nota zero são estados distintos.",
            "As linhas individuais permanecem fora do GitHub.",
            "Censo com escola duplicada impede integração muitos-para-um até resolução.",
        ],
    }
    return resultado


def main():
    REPORT.mkdir(parents=True, exist_ok=True)
    resultado = {
        "gerado_em_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "bases": {}, "falhas": {},
    }
    for tipo in CONFIG:
        print("Limpando:", tipo, flush=True)
        try:
            resultado["bases"][tipo] = processar(tipo)
        except Exception as e:
            resultado["falhas"][tipo] = f"{type(e).__name__}: {e}"
            print("Erro:", resultado["falhas"][tipo], flush=True)
    (REPORT / "qualidade_2024.json").write_text(
        json.dumps(resultado, indent=2, ensure_ascii=False), encoding="utf-8")
    partes = [
        "# Qualidade dos recortes INEP 2024 — Paraíba",
        "",
        "Limpeza conservadora, rastreável, sem imputação de valores e sem exclusão de linhas.",
        "Somente informações agregadas são divulgadas neste documento.",
        "",
    ]
    for nome, info in resultado["bases"].items():
        partes += [
            "## " + nome,
            "",
            f"- Registros preservados: {info['registros']}",
            f"- Colunas: {info['colunas']}",
            f"- Códigos escolares duplicados no Censo: {info['codigos_censo_duplicados']}",
            "",
            "### Qualidade por tipo de ocorrência",
            "",
            "~~~json",
            json.dumps(info["ocorrencias_de_qualidade"], indent=2, ensure_ascii=False),
            "~~~", "",
            "### Campos vazios após limpeza",
            "",
            "~~~json",
            json.dumps(info["campos_vazios_por_coluna"], indent=2, ensure_ascii=False),
            "~~~", "",
        ]
    if resultado["falhas"]:
        partes += [
            "## Falhas", "", "~~~json",
            json.dumps(resultado["falhas"], indent=2, ensure_ascii=False), "~~~", "",
        ]
    partes += [
        "## Limitações", "",
        "- Os valores brutos foram preservados nos ZIPs originais e nos arquivos filtrados.",
        "- O tratamento de valores especiais segue uma abordagem conservadora e requer o dicionário oficial.",
        "- Não houve vinculação individual de PARTICIPANTES_2024 com RESULTADOS_2024.",
        "- A integração escolar depende da auditoria de correspondência e unicidade das chaves.",
        "",
    ]
    (REPORT / "qualidade_2024.md").write_text("\n".join(partes), encoding="utf-8")
    if resultado["falhas"] or resultado["bases"].get("censo", {}).get("codigos_censo_duplicados", 0):
        raise SystemExit("Falha de limpeza ou duplicidade no Censo; não prosseguir para integração.")
    print("Relatório agregado:", REPORT / "qualidade_2024.md")


if __name__ == "__main__":
    main()
