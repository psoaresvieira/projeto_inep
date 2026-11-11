#!/usr/bin/env python3
"""Baixa dados oficiais do INEP para inspeção via GitHub Actions.

Os downloads são mantidos em dados_brutos/ (ignorado pelo Git).
Os arquivos originais enviados na conversa não são usados neste script.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ORIGENS = [
    ("microdados_enem_2024.zip", "https://download.inep.gov.br/microdados/microdados_enem_2024.zip", 526073856),
    ("microdados_censo_escolar_2024.zip", "https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2024.zip", 33829396),
    ("divulgacao_ensino_medio_escolas_2025.zip", "https://download.inep.gov.br/ideb/resultados/divulgacao_ensino_medio_escolas_2025.zip", 18989748),
]
DESTINO = Path("dados_brutos")
RELATORIOS = Path("reports/inspecao")


def baixar(nome: str, url: str, bytes_anexo: int) -> dict:
    info: dict = {
        "nome": nome,
        "url_oficial": url,
        "tamanho_anexo_usuario_bytes": bytes_anexo,
        "origem_do_download": "INEP (GitHub Actions; não é o anexo enviado na conversa)",
        "status": "falhou",
    }
    arquivo = DESTINO / nome
    for tentativa in range(1, 4):
        temporario = arquivo.with_name(arquivo.name + ".part")
        try:
            pedido = urllib.request.Request(
                url, headers={"User-Agent": "INEP-Paraiba-Projeto-Academico/1.0"}
            )
            with urllib.request.urlopen(pedido, timeout=90) as resposta, temporario.open("wb") as saida:
                while True:
                    bloco = resposta.read(4 * 1024 * 1024)
                    if not bloco:
                        break
                    saida.write(bloco)
            temporario.replace(arquivo)
            info["tamanho_baixado_bytes"] = arquivo.stat().st_size
            info["tamanho_coincide_com_anexo"] = arquivo.stat().st_size == bytes_anexo
            info["estrutura_zip_valida"] = zipfile.is_zipfile(arquivo)
            if not info["estrutura_zip_valida"]:
                raise ValueError("Conteúdo não é ZIP válido")
            info["status"] = "baixado"
            return info
        except Exception as exc:
            info["ultimo_erro"] = f"{type(exc).__name__}: {exc}"
            print(f"{nome}: tentativa {tentativa}/3: {info['ultimo_erro']}", file=sys.stderr)
            temporario.unlink(missing_ok=True)
            arquivo.unlink(missing_ok=True)
            if tentativa < 3:
                time.sleep(3 * tentativa)
    return info


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    RELATORIOS.mkdir(parents=True, exist_ok=True)
    resultados = []
    for nome, url, bytes_anexo in ORIGENS:
        print("Baixando", nome, flush=True)
        resultado = baixar(nome, url, bytes_anexo)
        resultados.append(resultado)
        print(nome, resultado["status"], flush=True)
    saida = {
        "data_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "nota": "Comparação de tamanhos não equivale a comprovação de igualdade de conteúdo.",
        "downloads": resultados,
    }
    (RELATORIOS / "downloads.json").write_text(
        json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    qtd = sum(item["status"] == "baixado" for item in resultados)
    print(f"Downloads válidos: {qtd}/{len(resultados)}")


if __name__ == "__main__":
    main()
