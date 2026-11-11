"""Testes sintéticos dos indicadores municipais e do dashboard, sem microdados."""
from __future__ import annotations
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def carregar(path):
    spec=importlib.util.spec_from_file_location("municipio_"+path.stem,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m=carregar(ROOT/"src/05_indicadores_municipais.py")
d=carregar(ROOT/"src/06_dashboard_municipios.py")


class MunicipiosTest(unittest.TestCase):
    def test_nota_nula_nao_vira_zero(self):
        self.assertIsNone(m.nota("-"))
        self.assertIsNone(m.nota(""))
        self.assertEqual(m.nota("0"),0.0)
        self.assertIsNone(m.nota("11"))

    def test_matriculas_invalidas_nao_vira_zero(self):
        self.assertIsNone(m.inteiro(""))
        self.assertIsNone(m.inteiro("-2"))
        self.assertEqual(m.inteiro("0"),0)

    def fake(self,quantidade_notas=2):
        g=m.novo()
        g["nome"]="Município Fictício"
        g["censo"]["escolas"]=482
        g["censo"]["matriculas"]=116779
        for campo in m.INFRA:
            g["censo"]["infraestrutura"][campo]["sim"]=482
        g["ideb"]["escolas"]=478
        g["ideb"]["notas_validas"]=458
        g["ideb"]["sem_nota"]=20
        g["ideb"]["_notas"]=[4.1]*458
        return m.montar({"2500000":g},482,478)

    def test_validacao_agregados(self):
        x=self.fake()
        self.assertEqual(x["totais"]["escolas_censo_2024"],482)
        self.assertEqual(x["municipios"][0]["ideb_2025"]["media_simples"],4.1)
        self.assertTrue(d.checar(x))

    def test_dashboard_usa_agregados_e_nao_lista_escolas(self):
        x=self.fake()
        page=d.pagina(x)
        self.assertIn("Município Fictício",page)
        self.assertIn("116779",page)
        self.assertIn("dados-municipios",page)
        self.assertNotIn("__DATA__",page)

    def test_suprime_media_ideb_municipios_pequenos(self):
        a=m.novo();b=m.novo()
        a["nome"]="Fictício A";b["nome"]="Fictício B"
        a["censo"]["escolas"]=482;a["censo"]["matriculas"]=116779
        for k in m.INFRA:
            a["censo"]["infraestrutura"][k]["sim"]=482
        a["ideb"]["escolas"]=2;a["ideb"]["notas_validas"]=2;a["ideb"]["_notas"]=[3.1,4.1]
        b["ideb"]["escolas"]=476;b["ideb"]["notas_validas"]=456;b["ideb"]["sem_nota"]=20;b["ideb"]["_notas"]=[5.0]*456
        x=m.montar({"2500000":a,"2500001":b},482,478)
        self.assertIsNone(x["municipios"][0]["ideb_2025"]["media_simples"])
        self.assertTrue(x["municipios"][0]["ideb_2025"]["media_suprimida_grupo_pequeno"])
        self.assertTrue(d.checar(x))


if __name__=="__main__":
    unittest.main()
