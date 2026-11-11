#!/usr/bin/env python3
"""Issue #5: análise exploratória preliminar com relatórios agregados já publicados.

Não utiliza ou expõe microdados individuais. Não compara as médias ENEM 2024
com a média IDEB 2025. Produz relatório Markdown e figuras SVG reproduzíveis.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
INSPECAO = ROOT / "reports/inspecao"
FILTRAGEM = ROOT / "reports/filtragem"
SAIDA = ROOT / "reports/analise_exploratoria"
FIGURAS = ROOT / "reports/figuras"

INFRA_LABELS = {
    "IN_INTERNET": "Internet",
    "IN_BANDA_LARGA": "Banda larga",
    "IN_BIBLIOTECA": "Biblioteca",
    "IN_SALA_LEITURA": "Sala de leitura",
    "IN_LABORATORIO_CIENCIAS": "Laboratório de ciências",
    "IN_LABORATORIO_INFORMATICA": "Laboratório de informática",
    "IN_QUADRA_ESPORTES": "Quadra de esportes",
}
ENEM_LABELS = {
    "NU_NOTA_CN": "Ciências da Natureza",
    "NU_NOTA_CH": "Ciências Humanas",
    "NU_NOTA_LC": "Linguagens",
    "NU_NOTA_MT": "Matemática",
    "NU_NOTA_REDACAO": "Redação",
}


def ler_json_de_secao(markdown: str, titulo: str) -> dict:
    inicio = re.search(r"(?m)^## " + re.escape(titulo) + r"\s*$", markdown)
    if not inicio:
        raise ValueError(f"Seção não encontrada: {titulo}")
    seguinte = re.search(r"(?m)^## ", markdown[inicio.end():])
    secao = markdown[inicio.end():inicio.end() + seguinte.start()] if seguinte else markdown[inicio.end():]
    achado = re.search(r"~~~json\s*([\s\S]*?)\s*~~~", secao)
    if not achado:
        raise ValueError(f"Bloco JSON não encontrado em {titulo}")
    return json.loads(achado.group(1))


def tabela_md(markdown: str, chave: str) -> str:
    padrao = re.compile(r"(?m)^\|\s*" + re.escape(chave) + r"\s*\|\s*([^|]+)\|")
    m = padrao.search(markdown)
    if not m:
        raise ValueError(f"Indicador ausente em tabela: {chave}")
    return m.group(1).strip()


def carregar(fontes_dir=INSPECAO, filtragem_dir=FILTRAGEM):
    perfil = (fontes_dir / "perfil_paraiba.md").read_text(encoding="utf-8")
    chaves = (filtragem_dir / "validacao_chaves_2024.md").read_text(encoding="utf-8")
    ideb = (fontes_dir / "ideb_pb_2025.md").read_text(encoding="utf-8")
    return {
        "censo": ler_json_de_secao(perfil, "CENSO_ESCOLAR_2024"),
        "resultados": ler_json_de_secao(perfil, "RESULTADOS_ENEM_2024"),
        "participantes": ler_json_de_secao(perfil, "PARTICIPANTES_ENEM_2024"),
        "auditoria": {
            "escolas_censo": int(tabela_md(chaves, "escolas_distintas_censo")),
            "escolas_enem": int(tabela_md(chaves, "escolas_distintas_enem_resultados")),
            "escolas_pareadas": int(tabela_md(chaves, "escolas_em_ambas_as_bases")),
            "linhas_enem": int(tabela_md(chaves, "linhas_participantes_enem_com_codigo")),
            "linhas_pareadas": int(tabela_md(chaves, "linhas_enem_com_correspondencia_escolar")),
            "duplicados": int(tabela_md(chaves, "codigos_censo_duplicados")),
        },
        "ideb": {
            "total": int(tabela_md(ideb, "quantidade_escolas_estaduais_PB_na_planilha")),
            "validas": int(tabela_md(ideb, "quantidade_com_IDEB_2025_valido")),
            "sem_nota": int(tabela_md(ideb, "quantidade_sem_IDEB_2025_valido")),
            "media_simples": float(tabela_md(ideb, "media_simples_escolas_com_nota")),
            "mediana": float(tabela_md(ideb, "mediana_escolas_com_nota")),
        },
    }


def percentual(a: int, b: int) -> float:
    if b <= 0:
        raise ValueError("Denominador deve ser maior que zero.")
    if a < 0 or a > b:
        raise ValueError(f"Numerador fora do intervalo: {a} / {b}")
    return round(100 * a / b, 2)


def validar(fontes):
    c = fontes["censo"]
    e = fontes["resultados"]
    a = fontes["auditoria"]
    i = fontes["ideb"]
    total = c["escolas_estaduais_ensino_medio_PB"]
    if a["escolas_censo"] != total or a["escolas_enem"] > e["codigos_escola_distintos_PB"]:
        raise ValueError("Contagens de escolas não condizem com o perfil da inspeção.")
    if a["duplicados"] or a["escolas_pareadas"] > min(a["escolas_enem"], total):
        raise ValueError("Auditoria de chaves inconsistente.")
    if a["linhas_enem"] != e["escola_estadual_na_PB"]:
        raise ValueError("Contagem de linhas do ENEM diverge entre fontes.")
    if a["linhas_pareadas"] > a["linhas_enem"]:
        raise ValueError("Linhas pareadas superam total.")
    if i["validas"] + i["sem_nota"] != i["total"]:
        raise ValueError("IDEB: escolas com e sem nota não somam total.")
    for nome, valores in c["valores_infraestrutura"].items():
        if nome in INFRA_LABELS and sum(valores.values()) != total:
            raise ValueError(f"Infraestrutura {nome} não soma {total} escolas.")
    return True


def svg_barras(titulo, sub, linhas, caminho):
    """Gráfico percentual com barras e denominador explícito; desenho local em SVG."""
    w = 1000
    linha_h = 56
    topo = 116
    h = topo + linha_h * len(linhas) + 58
    corpo = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="35" y="43" font-size="23" font-family="Arial,sans-serif" font-weight="bold" fill="#1e293b">{escape(titulo)}</text>',
        f'<text x="35" y="71" font-size="14" font-family="Arial,sans-serif" fill="#475569">{escape(sub)}</text>',
    ]
    for pos, (nome, sim, base) in enumerate(linhas):
        p = percentual(sim, base)
        y = topo + pos * linha_h
        label = escape(nome)
        corpo += [
            f'<text x="35" y="{y+9}" font-size="15" font-family="Arial,sans-serif" fill="#0f172a">{label}</text>',
            f'<rect x="320" y="{y-9}" width="480" height="22" rx="4" fill="#e2e8f0"/>',
            f'<rect x="320" y="{y-9}" width="{480*p/100:.2f}" height="22" rx="4" fill="#334155"/>',
            f'<text x="821" y="{y+9}" font-size="14" font-family="Arial,sans-serif" fill="#334155">{p:.1f}% ({sim}/{base})</text>',
        ]
    corpo.append(f'<text x="35" y="{h-22}" font-size="12" font-family="Arial,sans-serif" fill="#64748b">Fonte: INEP. Elaboração própria com as contagens agregadas verificadas.</text>')
    corpo.append("</svg>")
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("\n".join(corpo) + "\n", encoding="utf-8")


def gerar(fontes, pasta_saida=SAIDA, pasta_figuras=FIGURAS):
    validar(fontes)
    c = fontes["censo"]
    e = fontes["resultados"]
    a = fontes["auditoria"]
    i = fontes["ideb"]
    total = c["escolas_estaduais_ensino_medio_PB"]
    infra = []
    for chave, nome in INFRA_LABELS.items():
        contagem = c["valores_infraestrutura"].get(chave)
        if contagem is None:
            continue
        infra.append((nome, contagem.get("1", 0), total, contagem.get("0", 0), contagem.get("(vazio)", 0)))
    infra.sort(key=lambda t: (t[1]/t[2], t[0]), reverse=True)
    pasta_saida.mkdir(parents=True, exist_ok=True)
    pasta_figuras.mkdir(parents=True, exist_ok=True)
    svg_barras("Infraestrutura escolar — PB, Censo 2024",
               f"Escolas estaduais com ensino médio (n={total}); percentual de escolas com valor 1",
               [(nome, sim, n) for nome, sim, n, _, _ in infra],
               pasta_figuras / "infraestrutura_censo_PB_2024.svg")
    svg_barras("Cobertura do vínculo escolar ENEM–Censo 2024",
               "Proporções descritivas com denominadores diferentes, não representam a rede inteira",
               [
                   ("Escolas ENEM pareadas", a["escolas_pareadas"], a["escolas_enem"]),
                   ("Escolas Censo pareadas", a["escolas_pareadas"], a["escolas_censo"]),
                   ("Registros ENEM pareados", a["linhas_pareadas"], a["linhas_enem"]),
               ],
               pasta_figuras / "cobertura_chaves_PB_2024.svg")
    lines = [
        "# Análise exploratória preliminar — Educação estadual da Paraíba", "",
        "Relatório gerado automaticamente a partir de **dados agregados publicados**.",
        "Não realizou junção de participantes, não calculou causalidade e não extrapola o ENEM para toda a rede.", "",
        "## 1. Escolas e matrículas (Censo Escolar 2024)", "",
        f"- Escolas estaduais com oferta de ensino médio: **{total}**.",
        f"- Municípios com escolas estaduais de ensino médio: **{c['municipios_estaduais_EM']}**.",
        f"- Matrículas de ensino médio declaradas no recorte: **{c['matriculas_ensino_medio_somadas']:,}**.".replace(",", "."),
        "",
        "## 2. Infraestrutura das escolas estaduais com ensino médio (2024)", "",
        "| Indicador declarado | Presente (1) | Ausente (0) | Não informado | Percentual presente do total |",
        "|---|---:|---:|---:|---:|",
    ]
    for nome, sim, n, nao, vazio in infra:
        lines.append(f"| {nome} | {sim} | {nao} | {vazio} | {percentual(sim,n):.2f}% |".replace(".", ",") if False else
                     f"| {nome} | {sim} | {nao} | {vazio} | {percentual(sim,n):.2f}% |")
    lines += [
        "", "![Infraestrutura escolar — Censo 2024](../figuras/infraestrutura_censo_PB_2024.svg)", "",
        "A diferença entre internet declarada e banda larga declarada sugere uma **pergunta para auditoria de conectividade**,",
        "mas os códigos e a infraestrutura efetiva devem ser conferidos antes de propor intervenção.", "",
        "## 3. Cobertura do relacionamento por escola (ENEM–Censo 2024)", "",
        "| Indicador | Valor |",
        "|---|---:|",
        f"| Escolas ENEM estaduais PB | {a['escolas_enem']} |",
        f"| Escolas Censo estaduais com ensino médio | {a['escolas_censo']} |",
        f"| Escolas em ambas as bases | {a['escolas_pareadas']} |",
        f"| Cobertura das escolas ENEM | {percentual(a['escolas_pareadas'], a['escolas_enem']):.2f}% |",
        f"| Cobertura das escolas Censo | {percentual(a['escolas_pareadas'], a['escolas_censo']):.2f}% |",
        f"| Registros ENEM pareados | {a['linhas_pareadas']} / {a['linhas_enem']} ({percentual(a['linhas_pareadas'], a['linhas_enem']):.2f}%) |",
        "",
        "![Cobertura da ligação escolar](../figuras/cobertura_chaves_PB_2024.svg)", "",
        "Os denominadores são diferentes. As 41 escolas do ENEM sem par no Censo e as 26 do Censo sem",
        "participantes pareados precisam de investigação; não são necessariamente erros.", "",
        "## 4. Notas válidas no ENEM 2024 — participantes com escola estadual identificada", "",
        "| Área | Registros com nota válida | Média descritiva |",
        "|---|---:|---:|",
    ]
    for campo, titulo in ENEM_LABELS.items():
        s = e["notas_de_participantes_com_escola_estadual_PB"][campo]
        lines.append(f"| {titulo} | {s['validas']} | {s['media']:.2f} |")
    lines += [
        "", "As quantidades variam por área, e cada nota pertence somente aos participantes com escola identificada",
        "e nota válida. As escalas e composições dos grupos não autorizam classificar áreas apenas pela média.", "",
        "## 5. IDEB 2025 — escolas estaduais com nota divulgada", "",
        f"- Escolas estaduais na planilha: **{i['total']}**.",
        f"- Escolas com IDEB 2025 numérico: **{i['validas']}** ({percentual(i['validas'],i['total']):.2f}%).",
        f"- Escolas sem nota válida: **{i['sem_nota']}**.",
        f"- Média aritmética simples por escola com nota: **{i['media_simples']:.3f}**.",
        f"- Mediana por escola com nota: **{i['mediana']:.1f}**.",
        "",
        "A média simples não corresponde necessariamente ao IDEB oficial da rede. O IDEB de 2025 e o Censo de 2024",
        "referem-se a períodos distintos; as suas populações não devem ser comparadas como se fossem idênticas.", "",
        "## 6. Perguntas para próxima análise", "",
        "1. Quais municípios apresentam maior proporção de escolas sem determinados recursos?",
        "2. A cobertura do ENEM por escola varia sistematicamente com porte e território?",
        "3. Como diferem as distribuições escolares do IDEB 2025 quando consideradas as 20 escolas sem nota válida?",
        "4. Quais variáveis permanecem consistentes após a limpeza e a integração por escola?",
        "",
        "## 7. Limitações", "",
        "- As proporções de infraestrutura são quantidades declaradas pelas escolas.",
        "- O ENEM é voluntário; este subconjunto não representa todos os estudantes da rede.",
        "- Nenhuma informação socioeconômica foi vinculada individualmente às notas.",
        "- Nenhuma correlação ou efeito causal foi estimado entre infraestrutura e aprendizagem.",
        "- Não se deve igualar a média simples do IDEB 2025 ao índice oficial agregado da rede.",
        "- As escolas não pareadas necessitam de investigação de cobertura e período.",
        "",
        "## Fontes reprodutíveis", "",
        "- [Perfil agregado ENEM e Censo](../inspecao/perfil_paraiba.md)",
        "- [IDEB 2025 por escola](../inspecao/ideb_pb_2025.md)",
        "- [Auditoria de correspondência ENEM–Censo](../filtragem/validacao_chaves_2024.md)",
        "- [Código de geração do relatório](../../src/05_exploracao_preliminar.py)",
        "",
    ]
    out = pasta_saida / "analise_preliminar.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main():
    data = carregar()
    arq = gerar(data)
    print("Análise gerada:", arq)


if __name__ == "__main__":
    main()
