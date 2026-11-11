"""Testes locais sintéticos das regras de filtragem, sem microdados reais."""
from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

SOURCE = Path(__file__).resolve().parents[1] / "src" / "02_filtragem.py"
spec = importlib.util.spec_from_file_location("filtragem", SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def csv_bytes(columns, linhas):
    import io
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=columns, delimiter=";")
    writer.writeheader()
    for row in linhas:
        writer.writerow(row)
    return stream.getvalue().encode("utf-8-sig")


class RegrasFiltragemTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.base = self.root / "dados_brutos"
        self.output = self.root / "dados_filtrados"
        self.base.mkdir()
        p = patch.object(mod, "BASE", self.base)
        p.start()
        self.addCleanup(p.stop)
        p2 = patch.object(mod, "OUTPUT", self.output)
        p2.start()
        self.addCleanup(p2.stop)

    def criar_zip(self, config, rows):
        caminho = self.base / config["zip"]
        with zipfile.ZipFile(caminho, "a", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("simulado/" + config["suffix"], csv_bytes(config["colunas"], rows))

    def test_recorte_enem_escola_estadual(self):
        config = mod.CONFIGS[0]
        self.criar_zip(config, [
            {"SG_UF_ESC": "PB", "TP_DEPENDENCIA_ADM_ESC": "2",
             "CO_ESCOLA": "25000001", "CO_MUNICIPIO_ESC": "2507507", "NU_NOTA_MT": "620"},
            {"SG_UF_ESC": "PB", "TP_DEPENDENCIA_ADM_ESC": "3",
             "CO_ESCOLA": "25000002", "CO_MUNICIPIO_ESC": "2507507"},
            {"SG_UF_ESC": "SP", "TP_DEPENDENCIA_ADM_ESC": "2",
             "CO_ESCOLA": "35000001", "CO_MUNICIPIO_ESC": "3550308"},
        ])
        r = mod.filtrar(config, True)
        self.assertEqual(r["registros_origem"], 3)
        self.assertEqual(r["registros_selecionados"], 1)
        self.assertEqual(r["escolas_distintas"], 1)
        with (self.output / (config["nome"] + ".csv")).open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f, delimiter=";"))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["CO_ESCOLA"], "25000001")

    def test_recorte_censo_exige_rede_e_ensino_medio(self):
        config = mod.CONFIGS[1]
        self.criar_zip(config, [
            {"SG_UF": "PB", "TP_DEPENDENCIA": "2", "IN_MED": "1",
             "CO_ENTIDADE": "25000001", "CO_MUNICIPIO": "2507507"},
            {"SG_UF": "PB", "TP_DEPENDENCIA": "2", "IN_MED": "0",
             "QT_MAT_MED": "15", "CO_ENTIDADE": "25000002", "CO_MUNICIPIO": "2507507"},
            {"SG_UF": "PB", "TP_DEPENDENCIA": "2", "IN_MED": "0",
             "QT_MAT_MED": "0", "CO_ENTIDADE": "25000003"},
            {"SG_UF": "PB", "TP_DEPENDENCIA": "3", "IN_MED": "1",
             "CO_ENTIDADE": "25000004"},
        ])
        r = mod.filtrar(config, False)
        self.assertEqual(r["registros_origem"], 4)
        self.assertEqual(r["registros_selecionados"], 2)
        self.assertEqual(r["escolas_distintas"], 2)
        self.assertFalse((self.output / (config["nome"] + ".csv")).exists())

    def test_local_de_prova_independe_da_escola(self):
        config = mod.CONFIGS[2]
        self.criar_zip(config, [
            {"SG_UF_PROVA": "PB", "CO_MUNICIPIO_PROVA": "2507507",
             "TP_FAIXA_ETARIA": "5", "Q001": "A"},
            {"SG_UF_PROVA": "PE", "CO_MUNICIPIO_PROVA": "2611606",
             "TP_FAIXA_ETARIA": "5", "Q001": "B"},
        ])
        r = mod.filtrar(config, False)
        self.assertEqual(r["registros_origem"], 2)
        self.assertEqual(r["registros_selecionados"], 1)
        self.assertEqual(r["municipios_distintos"], 1)
        self.assertIsNone(r["escolas_distintas"])


if __name__ == "__main__":
    unittest.main()
