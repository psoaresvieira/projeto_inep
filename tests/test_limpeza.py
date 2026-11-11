"""Testes de limpeza com dados inteiramente fictícios."""
from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

MOD = Path(__file__).resolve().parents[1] / "src" / "03_limpeza.py"
spec = importlib.util.spec_from_file_location("limpeza_modulo", MOD)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class TestarLimpeza(unittest.TestCase):
    def test_nota_zero_preservada(self):
        self.assertEqual(m.validar_nota("0"), ("0.0", "valida"))

    def test_nota_ausente_nao_virar_zero(self):
        self.assertEqual(m.validar_nota(""), ("", "ausente"))
        self.assertEqual(m.validar_nota(" "), ("", "ausente"))

    def test_nota_invalida_e_range(self):
        self.assertEqual(m.validar_nota("1001"), ("", "invalida_fora_da_faixa"))
        self.assertEqual(m.validar_nota("-1"), ("", "invalida_fora_da_faixa"))
        self.assertEqual(m.validar_nota("texto"), ("", "invalida_nao_numerica"))

    def test_codigo_preserva_zeros_a_esquerda(self):
        self.assertEqual(m.validar_codigo("001234"), "001234")
        self.assertEqual(m.validar_codigo("ABC"), "")

    def test_contradiccao_presenca_nota(self):
        from collections import Counter
        estat = Counter()
        r = m.limpar_linha("enem", {
            "CO_ESCOLA": "25000001", "NU_NOTA_MT": "0",
            "TP_PRESENCA_MT": "0", "NU_NOTA_REDACAO": ""
        }, estat)
        self.assertEqual(r["NU_NOTA_MT"], "0.0")
        self.assertEqual(estat["NU_NOTA_MT:nota_com_presenca_diferente_de_1"], 1)

    def test_censo_conserva_ausencia_de_matriculas(self):
        from collections import Counter
        estat = Counter()
        r = m.limpar_linha("censo", {
            "CO_ENTIDADE": "25000001",
            "QT_MAT_MED": "", "IN_INTERNET": "1",
            "QT_DOC_MED": "10", "QT_TUR_MED": "5"
        }, estat)
        self.assertEqual(r["QT_MAT_MED"], "")
        self.assertEqual(r["QT_DOC_MED"], "10")
        self.assertEqual(estat["QT_MAT_MED:ausente"], 1)

    def test_processamento_nao_remove_registros_e_detecta_duplicidade(self):
        with tempfile.TemporaryDirectory() as folder:
            entrada = Path(folder) / "dados_filtrados"
            saida = Path(folder) / "dados_limpos"
            entrada.mkdir()
            f = entrada / m.CONFIG["censo"][0]
            cols = ["CO_ENTIDADE", "QT_MAT_MED", "IN_INTERNET"]
            with f.open("w", newline="", encoding="utf-8-sig") as stream:
                w = csv.DictWriter(stream, fieldnames=cols, delimiter=";")
                w.writeheader()
                w.writerow({"CO_ENTIDADE": "25000001", "QT_MAT_MED": "100", "IN_INTERNET": "1"})
                w.writerow({"CO_ENTIDADE": "25000001", "QT_MAT_MED": "", "IN_INTERNET": "0"})
            resultado = m.processar("censo", entrada, saida)
            self.assertEqual(resultado["registros"], 2)
            self.assertEqual(resultado["codigos_censo_duplicados"], 1)
            with (saida / "censo_escolas_estaduais_EM_PB_2024_limpo.csv").open(
                encoding="utf-8-sig", newline=""
            ) as stream:
                linhas = list(csv.DictReader(stream, delimiter=";"))
                self.assertEqual(len(linhas), 2)
                self.assertEqual(linhas[1]["QT_MAT_MED"], "")


if __name__ == "__main__":
    unittest.main()
