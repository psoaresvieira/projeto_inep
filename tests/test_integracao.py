"""Testes sintéticos da integração ENEM→Censo por escola, sem microdados reais."""
from __future__ import annotations

import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "src" / "04_integracao.py"
spec = importlib.util.spec_from_file_location("integracao_mod", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def escrever_csv(path, cols, linhas):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols, delimiter=";")
        writer.writeheader()
        for linha in linhas:
            writer.writerow(linha)


class IntegracaoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p = Path(self.tmp.name)
        self.censo = p / "censo.csv"
        self.enem = p / "enem.csv"
        self.audit = p / "auditoria.json"
        self.destino = p / "integradas"
        self.censo_cols = ["CO_ENTIDADE", "CO_MUNICIPIO", "NU_ANO_CENSO",
                           "SG_UF", "TP_DEPENDENCIA", "QT_MAT_MED"]
        self.enem_cols = ["CO_ESCOLA", "NU_ANO", "SG_UF_ESC", "TP_DEPENDENCIA_ADM_ESC",
                          *mod.NOTAS.keys(), *[x for x in mod.NOTAS.values() if x]]
        self.enem_cols = list(dict.fromkeys(self.enem_cols))
        escrever_csv(self.censo, self.censo_cols, [
            {"CO_ENTIDADE": "00001", "CO_MUNICIPIO": "2507507",
             "SG_UF": "PB", "TP_DEPENDENCIA": "2", "NU_ANO_CENSO": "2024", "QT_MAT_MED": "100"},
            {"CO_ENTIDADE": "00002", "CO_MUNICIPIO": "2507507",
             "SG_UF": "PB", "TP_DEPENDENCIA": "2", "NU_ANO_CENSO": "2024", "QT_MAT_MED": "200"},
        ])
        def enemrow(cod, grade="500.0", presenca="1"):
            return {"CO_ESCOLA": cod, "NU_ANO": "2024", "SG_UF_ESC": "PB",
                    "TP_DEPENDENCIA_ADM_ESC": "2", "NU_NOTA_MT": grade,
                    "TP_PRESENCA_MT": presenca}
        escrever_csv(self.enem, self.enem_cols,
                     [enemrow("00001") for _ in range(5)] +
                     [enemrow("00001", "600", "0")] +
                     [enemrow("00003", "600", "1")])
        self.audit.write_text(json.dumps({
            "codigos_censo_duplicados": 0,
            "validade_juncao": "CANDIDATA_APROVADA_PARA_ANÁLISE_POR_ESCOLA",
            "escolas_em_ambas_as_bases": 1,
            "linhas_enem_com_correspondencia_escolar": 6,
            "linhas_participantes_enem_com_codigo": 7,
        }), encoding="utf-8")

    def test_escolas_sao_unicas_e_media_exige_presenca_igual_a_1(self):
        res = mod.integrar(self.censo, self.enem, self.audit, self.destino)
        self.assertEqual(res["escolas_censo"], 2)
        self.assertEqual(res["escolas_enem"], 2)
        self.assertEqual(res["escolas_com_correspondencia"], 1)
        self.assertEqual(res["linhas_enem_pareadas"], 6)
        with (self.destino / "base_escolar_enem_censo_PB_2024.csv").open(
            encoding="utf-8-sig", newline=""
        ) as f:
            rows = list(csv.DictReader(f, delimiter=";"))
        self.assertEqual(len(rows), 2)
        valid = next(r for r in rows if r["CO_ENTIDADE"] == "00001")
        self.assertEqual(valid["NU_NOTA_MT_n_publicavel"], "5")
        self.assertEqual(valid["NU_NOTA_MT_media_publicavel"], "500.0")
        self.assertEqual(next(r for r in rows if r["CO_ENTIDADE"] == "00002")["tem_participantes_enem"], "0")

    def test_rejeita_auditoria_com_chaves_divergentes(self):
        j = json.loads(self.audit.read_text(encoding="utf-8"))
        j["escolas_em_ambas_as_bases"] = 0
        self.audit.write_text(json.dumps(j), encoding="utf-8")
        with self.assertRaises(ValueError):
            mod.integrar(self.censo, self.enem, self.audit, self.destino)

    def test_rejeita_duplicatas_no_censo(self):
        escrever_csv(self.censo, self.censo_cols, [
            {"CO_ENTIDADE": "001", "CO_MUNICIPIO": "2507507",
             "SG_UF": "PB", "TP_DEPENDENCIA": "2", "NU_ANO_CENSO": "2024"},
            {"CO_ENTIDADE": "001", "CO_MUNICIPIO": "2507507",
             "SG_UF": "PB", "TP_DEPENDENCIA": "2", "NU_ANO_CENSO": "2024"},
        ])
        with self.assertRaisesRegex(ValueError, "duplicada"):
            mod.integrar(self.censo, self.enem, self.audit, self.destino)


if __name__ == "__main__":
    unittest.main()
