"""Testes da exportação de indicadores agregados para Power BI."""
from __future__ import annotations

import copy
import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARQUIVO = ROOT / "src/07_exportar_powerbi.py"
spec = importlib.util.spec_from_file_location("exportar_powerbi", ARQUIVO)
modulo = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(modulo)


def csv_lido(caminho):
    with caminho.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file, delimiter=";"))


class TestarExportacaoPowerBI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(modulo.MUNICIPIOS.read_text(encoding="utf-8"))
        cls.enem = modulo.secao_json(
            modulo.ENEM.read_text(encoding="utf-8"), "RESULTADOS_ENEM_2024"
        )
        auditoria_md = modulo.CHAVES.read_text(encoding="utf-8")
        cls.auditoria = {
            chave: modulo.valor_tabela(auditoria_md, chave)
            for chave in [
                "escolas_distintas_censo",
                "escolas_distintas_enem_resultados",
                "escolas_em_ambas_as_bases",
                "linhas_participantes_enem_com_codigo",
                "linhas_enem_com_correspondencia_escolar",
            ]
        }

    def test_exporta_6_tabelas_com_totais_auditados(self):
        with tempfile.TemporaryDirectory() as temp:
            pasta = Path(temp)
            manifesto = modulo.construir(self.base, self.enem, self.auditoria, pasta)
            self.assertEqual(manifesto["tabelas_linhas"]["dim_municipio.csv"], 223)
            self.assertEqual(manifesto["tabelas_linhas"]["fato_infra_municipio_2024.csv"], 223 * 7)
            self.assertEqual(manifesto["tabelas_linhas"]["fato_enem_areas_2024.csv"], 5)
            self.assertEqual(len(csv_lido(pasta / "fato_censo_municipio_2024.csv")), 223)
            censo = csv_lido(pasta / "fato_censo_municipio_2024.csv")
            self.assertEqual(sum(int(x["escolas_ensino_medio"]) for x in censo), 482)
            self.assertEqual(sum(int(x["matriculas_declaradas"]) for x in censo), 116779)
            ideb = csv_lido(pasta / "fato_ideb_municipio_2025.csv")
            self.assertEqual(sum(int(x["escolas_nota_valida"]) for x in ideb), 458)
            self.assertTrue(any(x["media_suprimida"] == "1" for x in ideb))
            self.assertTrue(all(
                x["media_simples_escolas"] == "" and x["mediana_escolas"] == ""
                for x in ideb if x["media_suprimida"] == "1"
            ))
            self.assertTrue(all(x["ano"] == "2024" for x in censo))
            self.assertTrue(all(x["ano"] == "2025" for x in ideb))
            self.assertTrue(all(len(x["codigo_municipio"]) == 7 for x in censo))
            self.assertEqual(
                sum(int(x["escolas_sim"]) + int(x["escolas_nao"]) + int(x["escolas_sem_informacao"])
                    for x in csv_lido(pasta / "fato_infra_municipio_2024.csv")),
                482 * 7,
            )
            cobertura = csv_lido(pasta / "fato_cobertura_escolar_2024.csv")
            self.assertEqual(cobertura[0]["escolas_pareadas"], "456")
            self.assertEqual(cobertura[0]["registros_enem_pareados"], "29393")

    def test_nao_exporta_media_de_grupo_pequeno(self):
        alterada = copy.deepcopy(self.base)
        municipio = next(m for m in alterada["municipios"]
                         if m["ideb_2025"]["media_suprimida_grupo_pequeno"])
        municipio["ideb_2025"]["media_simples"] = 4.5
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "Supressão IDEB violada"):
                modulo.construir(alterada, self.enem, self.auditoria, Path(temp))

    def test_valida_totais_do_censo(self):
        alterada = copy.deepcopy(self.base)
        alterada["municipios"][0]["censo_2024"]["matriculas"] += 1
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "Total de matrículas divergente"):
                modulo.construir(alterada, self.enem, self.auditoria, Path(temp))


if __name__ == "__main__":
    unittest.main()
