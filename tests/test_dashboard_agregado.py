"""Testes do painel executivo com dados agregados publicados."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "src" / "06_dashboard_agregado.py"
spec = importlib.util.spec_from_file_location("dashboard_agregado", SOURCE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class DashboardAgregadoTest(unittest.TestCase):
    def test_gera_html_com_dados_validados(self):
        eda, data = m.carregar_analise()
        html = m.gerar_html(eda, data)
        self.assertIn("<!doctype html>", html.lower())
        self.assertIn("482", html)
        self.assertIn("29.393", html)
        self.assertIn("116.779", html)
        self.assertIn("95", html)
        self.assertIn("role=\"tablist\"", html)
        self.assertIn("Censo Escolar 2024", html)
        self.assertNotIn("__BARRAS__", html)

    def test_percentual_coerente_com_auditoria(self):
        eda, data = m.carregar_analise()
        audit = data["auditoria"]
        self.assertEqual(
            eda.percentual(audit["linhas_pareadas"], audit["linhas_enem"]),
            98.69,
        )


if __name__ == "__main__":
    unittest.main()
