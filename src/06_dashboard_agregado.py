#!/usr/bin/env python3
"""Gera dashboard executivo estático a partir de relatórios agregados do INEP.

Sem microdados individuais; sem chamadas externas. A fonte dos números
é validada pelo módulo src/05_exploracao_preliminar.py.
Uso: python src/06_dashboard_agregado.py
"""
from __future__ import annotations

import html
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULO = ROOT / "src" / "05_exploracao_preliminar.py"
DESTINO = ROOT / "dashboard" / "index.html"


def carregar_analise():
    spec = importlib.util.spec_from_file_location("eda_aggregada", MODULO)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fontes = mod.carregar()
    mod.validar(fontes)
    return mod, fontes


def inteiro(n):
    return f"{n:,}".replace(",", ".")


def decimal(n, casas=1):
    return f"{n:.{casas}f}".replace(".", ",")


def gerar_html(mod, dados):
    c = dados["censo"]
    e = dados["resultados"]
    a = dados["auditoria"]
    i = dados["ideb"]
    escolas = c["escolas_estaduais_ensino_medio_PB"]
    if escolas != a["escolas_censo"]:
        raise ValueError("Total de escolas incoerente entre Censo e auditoria.")
    pct = mod.percentual
    linhas_infra = []
    for codigo, titulo in mod.INFRA_LABELS.items():
        v = c["valores_infraestrutura"][codigo]
        sim, nao, vazio = v.get("1", 0), v.get("0", 0), v.get("(vazio)", 0)
        p = pct(sim, escolas)
        linhas_infra.append((titulo, sim, nao, vazio, p))
    linhas_infra.sort(key=lambda x: x[4], reverse=True)

    barras = "\n".join(
        f'<div class="bar-row" data-presenca="{p:.2f}">'
        f'<div class="bar-name">{html.escape(titulo)}</div>'
        f'<div class="bar-track" role="img" aria-label="{html.escape(titulo)}: {decimal(p)} por cento presentes">'
        f'<span class="bar-fill" style="width:{p:.2f}%"></span></div>'
        f'<div class="bar-amount">{decimal(p)}% <small>({sim}/{escolas})</small></div>'
        f'<div class="bar-alt">Ausentes: {nao} · Sem informação: {vazio}</div>'
        f'</div>' for titulo, sim, nao, vazio, p in linhas_infra
    )

    notas = "\n".join(
        f'<tr><th scope="row">{html.escape(rotulo)}</th><td>{inteiro(e["notas_de_participantes_com_escola_estadual_PB"][campo]["validas"])}</td>'
        f'<td>{decimal(e["notas_de_participantes_com_escola_estadual_PB"][campo]["media"],2)}</td></tr>'
        for campo, rotulo in mod.ENEM_LABELS.items()
    )
    gerado = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
    template = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Panorama Educacional da Paraíba — Projeto INEP</title>
<meta name="description" content="Panorama da educação estadual da Paraíba com dados agregados INEP 2024 e IDEB 2025.">
<style>
:root{color-scheme:light;--bg:#f4f6f9;--surface:#fff;--text:#182536;--muted:#526174;--line:#dae2ea;--nav:#102339;--accent:#167b73;--track:#e5ebf0}
*{box-sizing:border-box}body{margin:0;font-family:Inter,Arial,Helvetica,sans-serif;background:var(--bg);color:var(--text);line-height:1.55}
a{color:#095e59}a:focus-visible,button:focus-visible,select:focus-visible{outline:3px solid #e4a53d;outline-offset:2px}
.wrap{max-width:1160px;margin:0 auto;padding:0 22px}header{background:var(--nav);color:#fff;padding:26px 0 32px}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#82dbce}
header h1{margin:8px 0;font-size:clamp(26px,3.4vw,39px);letter-spacing:-.8px;line-height:1.15}
header p{max-width:840px;margin:12px 0;color:#dae5ed}
header .meta{font-size:12px;color:#c9d5df}
header a{color:#b2fcf0}
main{padding-top:25px;padding-bottom:50px}.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px}
.tabs button{cursor:pointer;padding:10px 16px;background:#fff;border:1px solid var(--line);border-radius:8px;color:var(--nav);font-weight:650}
.tabs button[aria-selected=true]{background:var(--nav);border-color:var(--nav);color:#fff}
.panel[hidden]{display:none}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:13px;margin:0 0 24px}
.card,.section{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:20px}
.card .number{font-size:30px;line-height:1.1;font-weight:780;letter-spacing:-.8px}.card .label{font-size:13px;color:var(--muted);margin-top:11px}
h2{font-size:20px;margin:0 0 14px}h3{font-size:16px;margin:16px 0 8px}
.section{margin-bottom:18px}.muted{color:var(--muted)}.note{border-left:3px solid var(--accent);padding:11px 15px;background:#f2faf8;border-radius:0 8px 8px 0}
.small{font-size:13px}.bar-row{display:grid;grid-template-columns:200px 1fr 160px;gap:12px;align-items:center;padding:12px 0;border-bottom:1px solid #ebeff4}
.bar-name{font-size:14px;font-weight:650}.bar-track{background:var(--track);height:19px;border-radius:5px;overflow:hidden}
.bar-fill{display:block;background:var(--accent);height:100%;border-radius:5px}.bar-amount{font-weight:700;white-space:nowrap}
.bar-amount small{display:block;color:var(--muted);font-size:11px;font-weight:400}
.bar-alt{grid-column:2 / -1;font-size:11px;color:var(--muted);margin-top:-9px}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{text-align:left;padding:12px;border-bottom:1px solid var(--line)}
thead th{background:#f0f5f8}td{text-align:right;font-variant-numeric:tabular-nums}
.info-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px}
select{background:#fff;border:1px solid #b9c7d3;border-radius:8px;padding:9px}
footer{font-size:12px;color:var(--muted);padding:20px 0}
@media (max-width:700px){.bar-row{grid-template-columns:1fr 115px}.bar-name{grid-column:1/-1}.bar-track{grid-column:1}.bar-amount{grid-column:2}.bar-alt{grid-column:1/-1;margin:0}header{padding-top:22px}}
</style>
</head>
<body>
<header><div class="wrap">
<div class="eyebrow">Análise de dados · Projeto INEP</div>
<h1>Panorama da educação pública na Paraíba</h1>
<p>Diagnóstico descritivo do ensino médio estadual, com dados oficiais do Censo Escolar e ENEM 2024 e IDEB 2025. Informações destinadas à discussão de prioridades e políticas educacionais.</p>
<div class="meta">Atualizado: __GERADO__ · Dados de anos diferentes são analisados separadamente · <a href="../README.md">Metodologia e código</a></div>
</div></header>
<main class="wrap">
<nav class="tabs" role="tablist" aria-label="Seções do painel">
<button role="tab" aria-selected="true" aria-controls="panorama" id="tab-panorama">Panorama</button>
<button role="tab" aria-selected="false" aria-controls="infra" id="tab-infra">Infraestrutura</button>
<button role="tab" aria-selected="false" aria-controls="desempenho" id="tab-desempenho">Aprendizagem</button>
<button role="tab" aria-selected="false" aria-controls="metodo" id="tab-metodo">Metodologia</button>
</nav>
<p class="small" style="margin:0 0 19px"><a href="municipios.html" style="font-weight:700">Explorar indicadores por município (Censo 2024 e IDEB 2025)</a></p>
<section class="panel" id="panorama" role="tabpanel" aria-labelledby="tab-panorama">
<div class="cards">
<div class="card"><div class="number">__ESCOLAS__</div><div class="label">Escolas estaduais com ensino médio — Censo 2024</div></div>
<div class="card"><div class="number">__MATRICULAS__</div><div class="label">Matrículas de ensino médio declaradas — Censo 2024</div></div>
<div class="card"><div class="number">__MUNICIPIOS__</div><div class="label">Municípios com escolas estaduais de ensino médio — Censo 2024</div></div>
<div class="card"><div class="number">__PAREADAS__</div><div class="label">Escolas com correspondência ENEM–Censo 2024</div></div>
</div>
<div class="section"><h2>O que os dados permitem observar</h2>
<p>As informações apontam oportunidades de investigar diferenças de infraestrutura e cobertura da rede. Os números <strong>não</strong> demonstram, por si só, que determinado recurso seja causa de notas melhores ou piores.</p>
<div class="note small"><strong>Próxima prioridade analítica:</strong> estudar desigualdades territoriais e a distribuição dos indicadores escolares usando bases validadas por escola e ano.</div></div>
<div class="section"><h2>Cobertura do cruzamento por escola em 2024</h2>
<p><strong>__REGISTROS_PAREADOS__</strong> dos <strong>__REGISTROS_ENEM__</strong> registros do ENEM com escola estadual na PB encontraram escola correspondente no Censo 2024 (<strong>__TAXA_MATCH__%</strong>).</p>
<p class="muted small">A integração por escola não equivale à ligação individual dos questionários socioeconômicos às notas. As bases possuem restrições de identificação.</p>
</div>
</section>
<section class="panel" id="infra" role="tabpanel" aria-labelledby="tab-infra" hidden>
<div class="section">
<h2>Infraestrutura escolar — Censo Escolar 2024</h2>
<p class="muted small">Denominador: __ESCOLAS__ escolas estaduais com ensino médio. Percentual com valor declarado 1; ausências e não informados são mostrados separadamente.</p>
<div class="info-row">
<label for="filtro-infra"><strong>Filtrar indicadores</strong></label>
<select id="filtro-infra">
<option value="todos">Todos</option>
<option value="baixo">Presença inferior a 50%</option>
<option value="alto">Presença de 50% ou mais</option>
</select>
<span id="quant-indicadores" class="small muted"></span>
</div>
<div id="barras-infra">__BARRAS__</div>
<div class="note small">Os campos medem declaração de existência. Internet e banda larga são indicadores diferentes; a qualidade efetiva da conexão requer diagnóstico complementar.</div>
</div>
</section>
<section class="panel" id="desempenho" role="tabpanel" aria-labelledby="tab-desempenho" hidden>
<div class="section"><h2>ENEM 2024 — médias de notas válidas</h2>
<p class="muted small">Somente participantes com escola estadual da PB identificada nos microdados. O número de notas válidas varia entre áreas, e o ENEM não representa automaticamente a rede inteira.</p>
<table><thead><tr><th scope="col">Área</th><th scope="col">Notas válidas</th><th scope="col">Média</th></tr></thead><tbody>__NOTAS__</tbody></table></div>
<div class="section"><h2>IDEB 2025 — escolas estaduais com nota divulgada</h2>
<div class="cards">
<div class="card"><div class="number">__IDEB_VALIDAS__</div><div class="label">Escolas com IDEB 2025 numérico, dentre __IDEB_TOTAL__ na planilha</div></div>
<div class="card"><div class="number">__IDEB_MEDIA__</div><div class="label">Média simples das escolas com nota (não é IDEB oficial da rede)</div></div>
<div class="card"><div class="number">__IDEB_MEDIANA__</div><div class="label">Mediana entre as escolas com nota válida</div></div>
</div>
<p class="muted small">Vinte escolas estaduais da planilha não possuem valor numérico válido no campo observado de 2025. Não se atribuiu nota zero.</p></div>
</section>
<section class="panel" id="metodo" role="tabpanel" aria-labelledby="tab-metodo" hidden>
<div class="section"><h2>Critérios de análise e privacidade</h2>
<p>O método segue D.E.I.L.A.S. e utiliza microdados oficiais apenas para contagens e relatórios agregados. As bases nacionais não são publicadas neste repositório.</p>
<ul>
<li>ENEM 2024: o local de prova não equivale à escola ou residência.</li>
<li>ENEM e Censo 2024: relacionamento apenas por código de escola, com unicidade e cobertura auditadas.</li>
<li>Os questionários socioeconômicos do ENEM não foram relacionados individualmente às notas.</li>
<li>IDEB 2025: média simples de escolas com resultado não equivale ao índice oficial da rede.</li>
<li>2025: ENEM e Censo estão em processo de coleta e inspeção antes da análise longitudinal.</li>
</ul>
<p class="small"><a href="../docs/metodologia_DEILAS.md">Metodologia D.E.I.L.A.S.</a> · <a href="../reports/qualidade/qualidade_2024.md">Relatório de qualidade</a> · <a href="../reports/integracao/integracao_2024.md">Integração escolar</a> · <a href="../reports/analise_exploratoria/analise_preliminar.md">Análise exploratória</a></p>
</div></section>
</main>
<footer class="wrap">INEP · Análise acadêmica descritiva · Elaboração com dados oficiais. Não atribuir causalidade às associações observadas.</footer>
<script>
(function () {
  const tabs = document.querySelectorAll('[role="tab"]');
  for (const tab of tabs) tab.addEventListener('click', () => {
    for (const other of tabs) {
      const active = other === tab;
      other.setAttribute('aria-selected', String(active));
      document.getElementById(other.getAttribute('aria-controls')).hidden = !active;
    }
  });
  const filtro = document.getElementById('filtro-infra');
  const linhas = Array.from(document.querySelectorAll('.bar-row'));
  function aplicar() {
    let visiveis = 0;
    for (const row of linhas) {
      const p = Number(row.dataset.presenca);
      const mostrar = filtro.value === 'todos' ||
          (filtro.value === 'baixo' && p < 50) ||
          (filtro.value === 'alto' && p >= 50);
      row.hidden = !mostrar;
      if (mostrar) visiveis += 1;
    }
    document.getElementById('quant-indicadores').textContent = visiveis + ' indicadores exibidos';
  }
  filtro.addEventListener('change', aplicar);
  aplicar();
})();
</script>
</body></html>
"""
    replacements = {
        "__GERADO__": gerado,
        "__ESCOLAS__": inteiro(escolas),
        "__MATRICULAS__": inteiro(c["matriculas_ensino_medio_somadas"]),
        "__MUNICIPIOS__": inteiro(c["municipios_estaduais_EM"]),
        "__PAREADAS__": inteiro(a["escolas_pareadas"]),
        "__REGISTROS_PAREADOS__": inteiro(a["linhas_pareadas"]),
        "__REGISTROS_ENEM__": inteiro(a["linhas_enem"]),
        "__TAXA_MATCH__": decimal(pct(a["linhas_pareadas"], a["linhas_enem"]), 2),
        "__BARRAS__": barras,
        "__NOTAS__": notas,
        "__IDEB_VALIDAS__": inteiro(i["validas"]),
        "__IDEB_TOTAL__": inteiro(i["total"]),
        "__IDEB_MEDIA__": decimal(i["media_simples"], 3),
        "__IDEB_MEDIANA__": decimal(i["mediana"], 1),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    if "__" in template:
        raise ValueError("Placeholder não preenchido no dashboard.")
    return template


def main():
    mod, dados = carregar_analise()
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    pag = gerar_html(mod, dados)
    DESTINO.write_text(pag, encoding="utf-8")
    print("Dashboard agregado gerado:", DESTINO)


if __name__ == "__main__":
    main()
