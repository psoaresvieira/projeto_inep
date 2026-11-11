#!/usr/bin/env python3
"""Issue #1: inventário não destrutivo dos ZIPs oficiais do INEP.

Uso:
    python src/01_inspecao.py --pasta dados_brutos
    python src/01_inspecao.py --arquivos /caminho/enem.zip /caminho/censo.zip

Não extrai os arquivos nem modifica as bases. As contagens de registros,
valores nulos e filtragem por UF exigem etapa posterior/execução adicional.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

TABULARES = {".csv", ".txt", ".tsv", ".xlsx", ".xlsm", ".xls", ".parquet"}
LIMITE_EXCEL = 75 * 1024 * 1024  # evita ler em memória planilhas enormes
LIMITE_AMOSTRA = 65536


def tamanho(n: int) -> str:
    for unidade in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unidade == "TB":
            return f"{n:.1f} {unidade}"
        n /= 1024
    return ""


def texto_amostra(raw: bytes) -> tuple[str, str]:
    for codificacao in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(codificacao), codificacao
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1", errors="replace"), "latin-1"


def amostrar_csv(arquivo: zipfile.ZipFile, membro: zipfile.ZipInfo) -> dict:
    with arquivo.open(membro) as f:
        raw = f.read(LIMITE_AMOSTRA)
    texto, codificacao = texto_amostra(raw)
    linhas = texto.splitlines()
    if not linhas:
        return {"codificacao_amostra": codificacao, "colunas": [], "separador": None}
    amostra = "\n".join(linhas[:15])
    try:
        separador = csv.Sniffer().sniff(amostra, delimiters=";,\t|").delimiter
    except csv.Error:
        separador = "\t" if membro.filename.lower().endswith(".tsv") else max(
            (";", ",", "\t", "|"), key=lambda s: linhas[0].count(s)
        )
    cabecalho = next(csv.reader([linhas[0]], delimiter=separador), [])
    return {
        "codificacao_amostra": codificacao,
        "separador": repr(separador),
        "quantidade_colunas_amostra": len(cabecalho),
        "colunas": [str(col).strip() for col in cabecalho],
        "observacao": "Cabeçalho inferido por amostragem; validar no dicionário oficial.",
    }


def amostrar_excel(arquivo: zipfile.ZipFile, membro: zipfile.ZipInfo) -> dict:
    if membro.file_size > LIMITE_EXCEL:
        return {"observacao": "Excel maior que 75 MiB; leitura de abas adiada."}
    try:
        from openpyxl import load_workbook
    except ImportError:
        return {"observacao": "Instale openpyxl para inspecionar planilhas Excel."}
    with arquivo.open(membro) as f:
        dados = f.read()
    pasta = load_workbook(io.BytesIO(dados), read_only=True, data_only=True)
    try:
        abas = []
        for planilha in pasta.worksheets:
            primeira = next(planilha.iter_rows(min_row=1, max_row=1, values_only=True), ())
            abas.append({
                "aba": planilha.title,
                "linhas_estimadas": planilha.max_row,
                "colunas_primeira_linha": [str(v) if v is not None else "" for v in primeira],
            })
        return {"abas": abas}
    finally:
        pasta.close()


def inspecionar_zip(caminho: Path) -> dict:
    saida = {
        "arquivo": caminho.name,
        "tamanho_zip_bytes": caminho.stat().st_size,
        "zip_valido": False,
        "membros": [],
        "erros": [],
    }
    try:
        with zipfile.ZipFile(caminho) as zf:
            saida["zip_valido"] = True
            for membro in zf.infolist():
                if membro.is_dir():
                    continue
                ext = Path(membro.filename).suffix.lower()
                item = {
                    "nome": membro.filename,
                    "extensao": ext,
                    "bytes_compactados": membro.compress_size,
                    "bytes_descompactados": membro.file_size,
                    "tipo_tabela": ext in TABULARES,
                }
                if ext in (".csv", ".txt", ".tsv"):
                    try:
                        item.update(amostrar_csv(zf, membro))
                    except Exception as exc:
                        item["erro_amostragem"] = str(exc)
                elif ext in (".xlsx", ".xlsm"):
                    try:
                        item.update(amostrar_excel(zf, membro))
                    except Exception as exc:
                        item["erro_amostragem"] = str(exc)
                elif ext == ".zip":
                    item["observacao"] = "ZIP interno detectado; requer inspeção complementar."
                saida["membros"].append(item)
    except (OSError, zipfile.BadZipFile) as exc:
        saida["erros"].append(str(exc))
    return saida


def montar_markdown(dados: list[dict]) -> str:
    texto = [
        "# Inventário técnico — Projeto ENEM Paraíba",
        "",
        f"Gerado em UTC: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "",
        "## Escopo e limites",
        "",
        "- Inspeção não destrutiva de arquivos ZIP oficiais fornecidos pelo grupo.",
        "- Nomes, extensões, tamanhos e amostras de cabeçalhos são evidências observadas.",
        "- A leitura de cabeçalhos não valida os significados das variáveis.",
        "- Quantidade de registros, nulos, duplicatas e integridade das chaves: **pendentes**.",
        "- Nenhuma junção ENEM–Censo–IDEB foi executada nesta etapa.",
        "",
        "## Arquivos inspecionados",
        "",
        "| Arquivo | Tamanho ZIP | ZIP válido | Arquivos internos | Tabelas candidatas |",
        "|---|---:|:---:|---:|---:|",
    ]
    for z in dados:
        texto.append(
            f"| `{z['arquivo']}` | {tamanho(z['tamanho_zip_bytes'])} | "
            f"{'sim' if z['zip_valido'] else 'não'} | {len(z['membros'])} | "
            f"{sum(x['tipo_tabela'] for x in z['membros'])} |"
        )
    for z in dados:
        texto.extend(["", f"## {z['arquivo']}", ""])
        if z["erros"]:
            texto.append("Erros: " + "; ".join(z["erros"]))
        texto.extend([
            "| Arquivo interno | Extensão | Descompactado |",
            "|---|---|---:|",
        ])
        for x in z["membros"]:
            nome = x["nome"].replace("|", "\\|")
            texto.append(f"| `{nome}` | {x['extensao']} | {tamanho(x['bytes_descompactados'])} |")
        for x in z["membros"]:
            if not x["tipo_tabela"]:
                continue
            texto.extend(["", f"### {x['nome']}", ""])
            if x.get("colunas"):
                texto.append(f"Colunas amostradas ({len(x['colunas'])}):")
                texto.append("")
                texto.append("```text")
                texto.append(", ".join(x["colunas"]))
                texto.append("```")
            if x.get("abas"):
                for aba in x["abas"]:
                    texto.append(
                        f"- Aba **{aba['aba']}**; linhas estimadas pela planilha: "
                        f"{aba['linhas_estimadas']}; primeira linha: "
                        f"{', '.join(aba['colunas_primeira_linha'])}"
                    )
            if x.get("observacao"):
                texto.append(x["observacao"])
            if x.get("erro_amostragem"):
                texto.append("Falha de amostragem: " + x["erro_amostragem"])
    texto.extend([
        "",
        "## Próximas validações",
        "",
        "1. Conferir dicionários e documentação de cada edição.",
        "2. Confirmar variável de escola/rede/UF nos microdados do ENEM.",
        "3. Medir contagem exata de registros e cobertura da Paraíba.",
        "4. Avaliar completude, unicidade e granularidade das chaves.",
        "5. Definir modelos separados se não houver relacionamento individual viável.",
        "",
        "Não compartilhar arquivos brutos grandes nem informações individuais no GitHub.",
    ])
    return "\n".join(texto) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pasta", type=Path, default=Path("dados_brutos"))
    parser.add_argument("--arquivos", nargs="*", type=Path)
    parser.add_argument("--saida", type=Path, default=Path("reports/inspecao"))
    args = parser.parse_args()
    caminhos = args.arquivos if args.arquivos else sorted(args.pasta.glob("*.zip"))
    if not caminhos:
        parser.error("Nenhum ZIP encontrado. Coloque arquivos em dados_brutos/ ou use --arquivos.")
    args.saida.mkdir(parents=True, exist_ok=True)
    inventario = [inspecionar_zip(p) for p in caminhos if p.is_file()]
    (args.saida / "inventario.json").write_text(
        json.dumps(inventario, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (args.saida / "inventario.md").write_text(montar_markdown(inventario), encoding="utf-8")
    for z in inventario:
        print(f"{z['arquivo']}: válido={z['zip_valido']}, membros={len(z['membros'])}")
    print("Inventário salvo em", args.saida.resolve())


if __name__ == "__main__":
    main()
