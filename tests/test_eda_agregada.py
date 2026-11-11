"""Testes de consistência do relatório exploratório (dados agregados já publicados)."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "05_exploracao_preliminar.py"
spec = importlib.util.spec_from_file_location("eda_agregada", SRC)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class RelatorioAgregadoTest(unittest.TestCase):
    def test_fontes_publicadas_coerentes(self):
        f = m.carregar()
        self.assertTrue(m.validar(f))
        self.assertEqual(f["auditoria"]["escolas_pareadas"], 456)
        self.assertEqual(f["censo"]["escolas_estaduais_ensino_medio_PB"], 482)
        self.assertEqual(f["ideb"]["validas"], 458)

    def test_percentual_usa_denominador_e_validacao(self):
        self.assertEqual(m.percentual(25, 100), 25.0)
        with self.assertRaises(ValueError):
            m.percentual(101, 100)
        with self.assertRaises(ValueError):
            m.percentual(0, 0)

    def test_relatorio_e_figuras_reproduziveis(self):
        f = m.carregar()
        with tempfile.TemporaryDirectory() as d:
            raiz = Path(d)
            rel = m.gerar(f, raiz / "relatorio", raiz / "figuras")
            conteudo = rel.read_text(encoding="utf-8")
            self.assertIn("456", conteudo)
            self.assertIn("482", conteudo)
            self.assertIn("458", conteudo)
            self.assertIn("98.69%", conteudo)
            svg = raiz / "figuras" / "infraestrutura_censo_PB_2024.svg"
            self.assertTrue(svg.is_file())
            self.assertIn("<svg", svg.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
