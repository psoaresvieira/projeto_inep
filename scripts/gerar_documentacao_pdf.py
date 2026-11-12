"""Renderiza documentação acadêmica revisada em PDF A4 profissional.

Fonte editável: docs/documentacao_projeto_final_revisada.md
Saída: reports/documentacao_projeto_final_revisada.pdf
"""
from __future__ import annotations

import html
import re
from pathlib import Path
from markdown import markdown
from weasyprint import HTML
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/documentacao_projeto_final_revisada.md"
OUTPUT = ROOT / "reports/documentacao_projeto_final_revisada.pdf"


def organizar():
    text = SOURCE.read_text(encoding="utf-8")
    if not text.startswith("# Projeto INEP"):
        raise ValueError("O arquivo de origem não corresponde à documentação revisada.")
    head, mark, body = text.partition("\n---\n")
    if not mark or len(body) < 8000:
        raise ValueError("Documento com conteúdo insuficiente.")
    headings = re.findall(r"(?m)^#\s+(\d+)\.\s+(.+)$", body)
    if len(headings) != 12:
        raise ValueError(f"Esperadas 12 seções, encontradas {len(headings)}.")
    toc = '<ol class="toc">' + "\n".join(
        f'<li><span>{html.escape(num)}.</span> {html.escape(title)}</li>'
        for num, title in headings
    ) + "</ol>"
    page_html = markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
    # Keep source code and data out of the PDF: source is documentation only.
    return toc, page_html


CSS = """
@page { size: A4; margin: 18mm 17mm 19mm 17mm;
  @top-right { content: "PROJETO INEP  •  DOCUMENTAÇÃO REVISADA"; font-family: 'DejaVu Sans',Arial,sans-serif;
    font-size: 7pt; color: #7b8996; letter-spacing: 0.7px; }
  @bottom-left { content: "ANÁLISE DE DADOS  |  PARAÍBA"; font-family: 'DejaVu Sans',Arial,sans-serif;
    font-size: 7pt; color: #8191a0; }
  @bottom-right { content: counter(page); font-family: 'DejaVu Sans',Arial,sans-serif;
    font-size: 9pt; font-weight: bold; color: #1b776f; }
}
@page cover { size:A4; margin:0;
  @top-right {content:none;} @bottom-left{content:none;} @bottom-right {content:none;}
}
body { margin: 0; font-family: 'DejaVu Sans', Arial, sans-serif; color: #243649;
       font-size: 9.2pt; line-height: 1.49; }
.cover { page: cover; height: 297mm; position: relative; box-sizing:border-box;
         background: #f6f9fb; page-break-after: always; }
.cover-top { background: #10273f; color: white; padding: 32mm 23mm 25mm; height: 152mm; box-sizing:border-box; }
.stripe { background: #188477; height: 5.5mm; }
.cover-label { text-transform:uppercase; color:#76d8c8; letter-spacing:1.9px;
               font-size:10pt; font-weight:bold; padding-bottom:16mm; }
.cover-title { font-size:31pt; font-weight:bold; line-height:1.17; letter-spacing:-1.2px; margin: 0 0 7mm; }
.cover-subtitle { font-size:14pt; line-height:1.3; color:#d5e5ee; font-weight:normal; }
.cover-lower {padding: 17mm 23mm 12mm;}
.cover-pill {display:inline-block; color:#0d625b; font-size:9pt; font-weight:bold;
             background:#dff5f1; border-radius:15px; padding: 3mm 5mm;}
.cover-team { font-size:10pt; color:#364657; margin-top:14mm; }
.cover-team strong { display:block; margin-bottom:4mm; font-size:9pt; color:#1c2f42; }
.cover-footer {position:absolute; bottom:16mm; left:23mm; right:23mm; border-top:1px solid #d6e2e9;
               padding-top:6mm; color:#60758a; font-size:9pt; }
.intro { page-break-after:always; padding-top: 10mm; }
.intro .section-label {color:#118176; text-transform:uppercase; font-size:9pt; font-weight:bold;letter-spacing:1.5px}
.intro h1 {font-size:23pt; color:#142a43; margin:7mm 0}
.summary-box { border-left:4px solid #188477; background:#edf7f5; padding: 4mm 5mm;
               margin: 9mm 0 10mm; font-size:10pt; }
.toc { columns:2; column-gap:14mm; margin-top:8mm; padding-left:0; list-style:none;}
.toc li { break-inside:avoid; padding:4mm 2mm; border-bottom:1px solid #e3e9ef;font-size:9pt}
.toc li span {font-weight:bold;color:#158175;display:inline-block;width:12mm}
.intro small {font-size:8.5pt;color:#66798a}
.content h1 { font-size:17pt; line-height:1.3; color:#142e47; font-weight:bold;
              margin: 11mm 0 4mm; padding-bottom:2mm; border-bottom:2px solid #16877b;
              page-break-after: avoid; break-after:avoid; }
.content h2 { font-size:11.2pt; color:#155d63; font-weight:bold;
              margin: 6mm 0 2.5mm; page-break-after:avoid; break-after:avoid; }
.content h3 { font-size:10pt; color:#1b5964; font-weight:bold;
              margin:5mm 0 2mm; page-break-after:avoid; }
.content p { margin:0 0 3.1mm; text-align:justify; overflow-wrap:break-word; }
.content blockquote {margin:5mm 0 5mm; padding: 3mm 5mm; background:#eaf6f3;
                    border-left:3px solid #188477; font-size:9.4pt;}
.content blockquote p { margin:0; }
.content table { width:100%; border-collapse:collapse; margin: 4mm 0 6mm; font-size: 7.8pt;
                 table-layout: fixed; }
.content th { background:#102a43; color:#fff; font-weight:bold; padding:2.6mm 2.3mm;
              text-align:left; vertical-align:top; overflow-wrap:anywhere; }
.content td { padding:2.5mm 2.3mm; border-bottom:1px solid #dfe7ed; vertical-align:top;
              overflow-wrap:anywhere; }
.content tr:nth-child(even) td {background:#f4f8fa;}
.content tr {break-inside:avoid;}
.content thead {display:table-header-group;}
.content ul,.content ol {margin:2mm 0 5mm 6mm; padding-left:5mm;}
.content li {margin:0 0 2mm; break-inside:avoid;}
.content strong {color:#172d40;}
.content a {color:#147c72; text-decoration:none; overflow-wrap:anywhere;}
.content code { font-family: 'DejaVu Sans Mono',monospace; font-size:8pt; color:#235670; }
.content hr {border:0;border-top:1px solid #d2dce5;margin:9mm 0}
"""
def build():
    toc, article = organizar()
    doc = f"""<!doctype html><html lang="pt-BR"><head>
    <meta charset="utf-8"><title>Documentação Projeto INEP — Versão Revisada</title>
    <style>{CSS}</style></head><body>
    <div class="cover">
      <div class="cover-top">
        <div class="cover-label">PROJETO ACADÊMICO • ANÁLISE DE DADOS</div>
        <div class="cover-title">Projeto INEP</div>
        <div class="cover-subtitle">Diagnóstico da qualidade do ensino médio público da Paraíba</div>
        <p style="font-size:12pt;color:#bbd5de;margin-top:15mm;">Documentação acadêmica, técnica e funcional</p>
      </div>
      <div class="stripe"></div>
      <div class="cover-lower">
        <span class="cover-pill">VERSÃO REVISADA • NOVEMBRO DE 2026</span>
        <div class="cover-team"><strong>EQUIPE</strong>Pedro Alexandre<br>Pedro Henrique Faustino<br>
          Maria Vitória Espínola Carneiro</div>
      </div>
      <div class="cover-footer">Governo do Estado da Paraíba • Metodologia D.E.I.L.A.S. • Proposta de 5 dashboards Power BI</div>
    </div>
    <section class="intro">
      <div class="section-label">VISÃO GERAL</div>
      <h1>Do dado educacional à decisão pública</h1>
      <div class="summary-box">O projeto converte bases oficiais do INEP em diagnósticos de infraestrutura,
      oferta e aprendizagem, com um relatório Power BI planejado em cinco páginas.
      Os dados de 2024 já possuem preparação, auditoria e análise exploratória iniciais;
      a implementação final em Power BI e a harmonização das bases de 2025 permanecem pendentes.</div>
      <h2 style="font-size:13pt;color:#102a43">Conteúdo do documento</h2>
      {toc}
      <p style="clear:both; margin-top:12mm"><small>O documento distingue resultados executados,
      protótipos já disponíveis e entregas ainda previstas. Indicadores de anos diferentes são apresentados
      com suas limitações de comparação.</small></p>
    </section>
    <main class="content">{article}</main>
    </body></html>"""
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=doc, base_url=str(ROOT)).write_pdf(str(OUTPUT))
    rd = PdfReader(str(OUTPUT))
    if len(rd.pages) < 8:
        raise ValueError(f"PDF inesperadamente curto: {len(rd.pages)} páginas")
    first = (rd.pages[0].extract_text() or "")
    full = "\n".join((page.extract_text() or "") for page in rd.pages)
    for phrase in ["Projeto INEP","Cinco dashboards","Power BI","482","29.393","IDEB"]:
        if phrase not in full:
            raise ValueError(f"Texto obrigatório ausente no PDF: {phrase}")
    print(f"PDF gerado: {OUTPUT} | páginas={len(rd.pages)} | bytes={OUTPUT.stat().st_size}")


if __name__ == "__main__":
    build()
