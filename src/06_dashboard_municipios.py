#!/usr/bin/env python3
"""Gera dashboard municipal HTML a partir de JSON agregado validado.

Uso: python src/06_dashboard_municipios.py
Não carrega microdados e não precisa de servidor ou chamadas externas.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports/municipios/municipios_agregados.json"
DEST = ROOT / "dashboard/municipios.html"


def checar(dados):
    t = dados["totais"]
    ms = dados["municipios"]
    if t["escolas_censo_2024"] != 482 or t["escolas_ideb_2025"] != 478:
        raise ValueError("Totais de escolas incorretos para Censo 2024 ou IDEB 2025.")
    if t["notas_validas_ideb_2025"] != 458 or t["matriculas_censo_2024"] != 116779:
        raise ValueError("Matrículas ou notas IDEB não conferem.")
    if len(ms) != t["municipios"] or not ms:
        raise ValueError("Municípios ausentes.")
    codes = [m["codigo_municipio"] for m in ms]
    if len(set(codes)) != len(codes):
        raise ValueError("Códigos de municípios duplicados.")
    if sum(m["censo_2024"]["escolas"] for m in ms) != 482:
        raise ValueError("Total de escolas Censo não fecha.")
    if sum(m["ideb_2025"]["notas_validas"] for m in ms) != 458:
        raise ValueError("Notas IDEB não fecham.")
    if any(m["ideb_2025"]["notas_validas"] < 3 and m["ideb_2025"]["media_simples"] is not None for m in ms):
        raise ValueError("Média IDEB não suprimida em município com menos de 3 notas.")
    return True


def pagina(dados):
    checar(dados)
    # Não inserir tags ou HTML de fontes externas na estrutura da página.
    j = json.dumps(dados, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    template = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Análise por Município — Educação Estadual da Paraíba</title>
<style>
:root{--ink:#14253a;--sub:#52667a;--bg:#f3f6fa;--paper:#fff;--border:#dce5ed;--accent:#167b73;--navy:#102339}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Inter,Arial,sans-serif;line-height:1.55}
.shell{max-width:1240px;margin:auto;padding:0 22px}
header{background:var(--navy);color:#fff;padding:25px 0 30px}
.eyebrow{color:#9ce4da;font-size:12px;font-weight:750;letter-spacing:1.4px;text-transform:uppercase}
h1{margin:8px 0 12px;font-size:clamp(26px,3.4vw,38px);line-height:1.15}
header p{max-width:920px;color:#dce7ed;margin:0;font-size:14px}
header a{color:#9ce4da}
main{padding-top:26px;padding-bottom:40px}
.summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:17px}
.kpi,.box{background:var(--paper);border:1px solid var(--border);border-radius:11px;padding:18px}
.kpi strong{display:block;font-size:27px;letter-spacing:-.6px}.kpi span{display:block;font-size:12px;color:var(--sub);margin-top:8px}
.box{margin-bottom:16px}
h2{font-size:19px;margin:0 0 10px}h3{font-size:15px;margin:0 0 9px}
.desc{font-size:13px;color:var(--sub);margin:0 0 14px}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:end;margin:12px 0}
.field{display:flex;flex-direction:column;gap:5px;font-size:12px;font-weight:650}
input,select{border:1px solid #b6c7d5;border-radius:7px;padding:10px;background:#fff;color:var(--ink);font-size:14px}
input{min-width:260px;max-width:100%}button{cursor:pointer}button:focus-visible,input:focus-visible,select:focus-visible,a:focus-visible{outline:3px solid #edb84c;outline-offset:2px}
.columns{display:grid;grid-template-columns:minmax(300px,1fr) minmax(300px,1.1fr);gap:16px}
.scroll{max-height:560px;overflow:auto;border:1px solid var(--border);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:12px}
thead th{position:sticky;top:0;background:#eaf1f5;z-index:1;text-align:left;padding:11px;border-bottom:1px solid #ccd8e3}
td{padding:9px 11px;border-bottom:1px solid #e8edf1}
td.num{text-align:right;white-space:nowrap;font-variant-numeric:tabular-nums}
.city-btn{border:0;background:transparent;color:#115a57;text-align:left;font-weight:700;font-size:12px;padding:3px 0;text-decoration:underline;text-decoration-color:#b7d5d1}
.city-btn[aria-current="true"]{color:#083a35;text-decoration:underline}
.citytitle{font-size:22px;font-weight:750;margin:0}
.pill{display:inline-flex;background:#eaf6f3;color:#0b6158;border-radius:20px;padding:3px 10px;font-size:11px;font-weight:700}
.details{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin:14px 0}
.detail{background:#f5f8fa;padding:13px;border:1px solid #e1e9ef;border-radius:8px}
.detail strong{font-size:21px;display:block}.detail span{font-size:11px;color:var(--sub)}
.baritem{margin:14px 0}.barline{display:flex;justify-content:space-between;gap:8px;font-size:12px;font-weight:650;margin-bottom:5px}
.track{background:#e5edf1;border-radius:6px;height:14px;overflow:hidden}.fill{background:var(--accent);height:100%}
.small{font-size:11px;color:var(--sub)}.note{border-left:3px solid var(--accent);background:#f1faf8;padding:11px 13px;font-size:12px;margin-top:15px}
footer{font-size:12px;color:var(--sub);padding:5px 0 30px}
@media(max-width:850px){.summary{grid-template-columns:repeat(2,minmax(0,1fr))}.columns{grid-template-columns:1fr}.scroll{max-height:420px}}
@media(max-width:460px){.shell{padding:0 13px}.summary{gap:8px}.kpi{padding:14px}.kpi strong{font-size:22px}.details{grid-template-columns:repeat(2,minmax(0,1fr))}input{min-width:210px;width:100%}}
</style>
</head>
<body>
<header><div class="shell">
<div class="eyebrow">Projeto INEP · Visão territorial</div>
<h1>Indicadores educacionais por município</h1>
<p>Compare cobertura e infraestrutura de escolas estaduais com ensino médio no Censo Escolar 2024 e consulte indicadores do IDEB 2025, apresentados separadamente por ano.</p>
<p style="margin-top:12px"><a href="index.html">Voltar ao painel geral</a> · <a href="../docs/metodologia_DEILAS.md">Metodologia</a></p>
</div></header>
<main class="shell">
<div class="summary">
<div class="kpi"><strong id="total-municipios"></strong><span>Municípios representados</span></div>
<div class="kpi"><strong id="total-escolas"></strong><span>Escolas estaduais com ensino médio — 2024</span></div>
<div class="kpi"><strong id="total-matriculas"></strong><span>Matrículas declaradas — 2024</span></div>
<div class="kpi"><strong id="total-ideb"></strong><span>Escolas com IDEB válido — 2025</span></div>
</div>
<div class="box">
<h2>Explorar municípios</h2>
<p class="desc">Pesquise pelo nome ou código IBGE, ordene a lista e selecione um município para ver o detalhamento. Todos os percentuais de infraestrutura usam como denominador as escolas estaduais com ensino médio naquele município em 2024.</p>
<div class="controls">
<label class="field">Pesquisar município
<input id="busca" type="search" placeholder="Ex.: João Pessoa" autocomplete="off">
</label>
<label class="field">Ordenar
<select id="ordem">
<option value="nome">Nome (A–Z)</option>
<option value="escolas">Mais escolas</option>
<option value="matriculas">Mais matrículas</option>
<option value="banda">Menor percentual com banda larga</option>
</select>
</label>
</div>
<p id="quantidade" class="small" role="status"></p>
</div>
<div class="columns">
<section class="box">
<h2>Municípios</h2>
<div class="scroll">
<table>
<thead><tr><th>Município</th><th>Escolas 2024</th><th>Matrículas 2024</th></tr></thead>
<tbody id="lista"></tbody>
</table>
</div>
</section>
<section class="box" aria-live="polite">
<div class="pill">Detalhamento por município</div>
<h2 class="citytitle" id="cidade-titulo" style="margin-top:8px">Selecione um município</h2>
<p class="small" id="cidade-codigo"></p>
<div class="details">
<div class="detail"><strong id="d-escolas">—</strong><span>Escolas com EM · Censo 2024</span></div>
<div class="detail"><strong id="d-matriculas">—</strong><span>Matrículas EM · Censo 2024</span></div>
<div class="detail"><strong id="d-ideb-escolas">—</strong><span>Escolas na planilha IDEB 2025</span></div>
<div class="detail"><strong id="d-ideb-media">—</strong><span>IDEB 2025: média simples, quando publicável</span></div>
</div>
<h3>Infraestrutura declarada — Censo 2024</h3>
<p class="small">Presença entre as escolas do município; os dados ausentes são mantidos à parte.</p>
<div id="indicadores"></div>
<div class="note" id="nota">Escolha um município na tabela.</div>
</section>
</div>
<div class="box">
<h2>Como interpretar</h2>
<p class="desc">As duas fontes retratam anos diferentes e não foram cruzadas no nível de escola. IDEB municipal, quando exibido, é somente a média simples das escolas com resultado válido e não representa o índice oficial da rede. Municípios com menos de três resultados válidos têm a média e a mediana ocultadas. A ausência de um recurso na declaração escolar não comprova, isoladamente, insuficiência de ensino ou efeito sobre a aprendizagem.</p>
</div>
</main>
<footer class="shell">Fonte: INEP · Censo Escolar 2024 e IDEB por escola 2025 · Análise acadêmica exploratória.</footer>
<script id="dados-municipios" type="application/json">__DATA__</script>
<script>
(() => {
const dados=JSON.parse(document.getElementById("dados-municipios").textContent);
const lista=document.getElementById("lista");
const busca=document.getElementById("busca");
const ordem=document.getElementById("ordem");
const num=(n)=>new Intl.NumberFormat("pt-BR").format(n);
const pct=(a,b)=>b ? new Intl.NumberFormat("pt-BR",{maximumFractionDigits:1}).format(100*a/b)+"%" : "—";
const nomes={
IN_INTERNET:"Internet",IN_BANDA_LARGA:"Banda larga",IN_BIBLIOTECA:"Biblioteca",
IN_LABORATORIO_CIENCIAS:"Laboratório de ciências",IN_LABORATORIO_INFORMATICA:"Laboratório de informática",
IN_QUADRA_ESPORTES:"Quadra esportiva",IN_AGUA_POTAVEL:"Água potável"
};
let atual=null;
document.getElementById("total-municipios").textContent=num(dados.totais.municipios);
document.getElementById("total-escolas").textContent=num(dados.totais.escolas_censo_2024);
document.getElementById("total-matriculas").textContent=num(dados.totais.matriculas_censo_2024);
document.getElementById("total-ideb").textContent=num(dados.totais.notas_validas_ideb_2025);
function setText(id,value){document.getElementById(id).textContent=String(value);}
function selecionar(m){
  atual=m.codigo_municipio;
  setText("cidade-titulo",m.nome_municipio);
  setText("cidade-codigo","Código IBGE: "+m.codigo_municipio);
  setText("d-escolas",num(m.censo_2024.escolas));
  setText("d-matriculas",num(m.censo_2024.matriculas));
  setText("d-ideb-escolas",num(m.ideb_2025.escolas));
  setText("d-ideb-media",m.ideb_2025.media_simples===null?"—":new Intl.NumberFormat("pt-BR",{maximumFractionDigits:3}).format(m.ideb_2025.media_simples));
  let nota="";
  const valid=m.ideb_2025.notas_validas,tot=m.ideb_2025.escolas;
  if(valid===0) nota="Nenhuma escola do município possui nota IDEB 2025 válida na planilha.";
  else if(valid<3) nota="Há "+valid+" resultado(s) IDEB 2025 válido(s) entre "+tot+" escola(s), mas a média foi ocultada por grupo pequeno (n < 3).";
  else nota="A média IDEB 2025 usa "+valid+" escola(s) com nota válida entre "+tot+" da planilha; não equivale ao índice oficial da rede.";
  document.getElementById("nota").textContent=nota;
  const area=document.getElementById("indicadores");
  area.replaceChildren();
  for(const [k,nome] of Object.entries(nomes)){
    const v=m.censo_2024.infraestrutura[k], base=m.censo_2024.escolas;
    const wrap=document.createElement("div");wrap.className="baritem";
    const line=document.createElement("div");line.className="barline";
    const label=document.createElement("span");label.textContent=nome;
    const value=document.createElement("span");value.textContent=pct(v.sim,base)+" · "+v.sim+"/"+base;
    line.append(label,value);
    const track=document.createElement("div");track.className="track";
    const fill=document.createElement("div");fill.className="fill";
    fill.style.width=(base?100*v.sim/base:0)+"%";
    track.append(fill);
    const detail=document.createElement("div");detail.className="small";
    detail.textContent="Ausente: "+v.nao+" · Sem informação: "+v.sem_informacao;
    wrap.append(line,track,detail);area.append(wrap);
  }
  document.querySelectorAll(".city-btn").forEach(b=>b.setAttribute("aria-current",String(b.dataset.code===atual)));
}
function ordenar(m){
  const metodo=ordem.value;
  if(metodo==="escolas")return m.sort((a,b)=>b.censo_2024.escolas-a.censo_2024.escolas || a.nome_municipio.localeCompare(b.nome_municipio,"pt-BR"));
  if(metodo==="matriculas")return m.sort((a,b)=>b.censo_2024.matriculas-a.censo_2024.matriculas || a.nome_municipio.localeCompare(b.nome_municipio,"pt-BR"));
  if(metodo==="banda")return m.sort((a,b)=> {
    const pa=a.censo_2024.escolas? a.censo_2024.infraestrutura.IN_BANDA_LARGA.sim/a.censo_2024.escolas : 2;
    const pb=b.censo_2024.escolas? b.censo_2024.infraestrutura.IN_BANDA_LARGA.sim/b.censo_2024.escolas : 2;
    return pa-pb || a.nome_municipio.localeCompare(b.nome_municipio,"pt-BR");
  });
  return m.sort((a,b)=>a.nome_municipio.localeCompare(b.nome_municipio,"pt-BR"));
}
function render(){
  const term=busca.value.trim().normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase();
  const matches=dados.municipios.filter(m=>(m.nome_municipio+" "+m.codigo_municipio).normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase().includes(term));
  ordenar(matches);
  lista.replaceChildren();
  for(const m of matches){
    const tr=document.createElement("tr");
    const td=document.createElement("td");
    const btn=document.createElement("button");btn.type="button";btn.className="city-btn";
    btn.dataset.code=m.codigo_municipio;btn.textContent=m.nome_municipio;
    btn.setAttribute("aria-current",String(m.codigo_municipio===atual));
    btn.addEventListener("click",()=>selecionar(m));
    td.append(btn);
    const n1=document.createElement("td");n1.className="num";n1.textContent=num(m.censo_2024.escolas);
    const n2=document.createElement("td");n2.className="num";n2.textContent=num(m.censo_2024.matriculas);
    tr.append(td,n1,n2);lista.append(tr);
  }
  setText("quantidade",matches.length+" município(s) encontrado(s).");
}
busca.addEventListener("input",render);
ordem.addEventListener("change",render);
render();
if(dados.municipios.length) selecionar(dados.municipios.find(m=>m.nome_municipio==="João Pessoa")||dados.municipios[0]);
})();
</script>
</body></html>"""
    out=template.replace("__DATA__",j)
    if "__DATA__" in out:
        raise ValueError("Marcador do JSON não foi substituído.")
    return out


def main():
    dados=json.loads(SOURCE.read_text(encoding="utf-8"))
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(pagina(dados), encoding="utf-8")
    print("Dashboard municipal gerado:",DEST)


if __name__ == "__main__":
    main()
