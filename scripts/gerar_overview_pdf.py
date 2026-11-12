#!/usr/bin/env python3
"""Relatório executivo do Projeto INEP — PDF vetorial A4, 5 páginas.

Fonte: resultados e status já consolidados no GitHub do projeto.
A saída é um resumo executivo, não um relatório estatístico final.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
import math

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/"reports"/"overview_executivo_projeto_inep.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
W,H=A4
NAVY=HexColor("#11283A")
DARK=HexColor("#162B3D")
TEAL=HexColor("#087F77")
MINT=HexColor("#C9F1EB")
LIGHT=HexColor("#F3F7F9")
WHITE=HexColor("#FFFFFF")
INK=HexColor("#192A3A")
MUTED=HexColor("#506376")
BORDER=HexColor("#E1E8ED")
PALE=HexColor("#E8F6F3")
AMBER=HexColor("#BD791C")
AMBER_PALE=HexColor("#FFF4DC")
BLUE=HexColor("#245D78")
GREY=HexColor("#A2B2BC")
GITHUB="https://github.com/psoaresvieira/projeto_inep"
FONT_DIR=Path("/usr/share/fonts/truetype/dejavu")
if (FONT_DIR/"DejaVuSans.ttf").exists():
    pdfmetrics.registerFont(TTFont("Text",str(FONT_DIR/"DejaVuSans.ttf")))
    pdfmetrics.registerFont(TTFont("TextBold",str(FONT_DIR/"DejaVuSans-Bold.ttf")))
else:
    pdfmetrics.registerFontFamily("Helvetica",normal="Helvetica",bold="Helvetica-Bold")
    # Fallback sem identidade visual customizada quando fontes externas indisponíveis.
    FONT_DIR=None
BODY="Text" if FONT_DIR else "Helvetica"
BOLD="TextBold" if FONT_DIR else "Helvetica-Bold"


def background(c,color=LIGHT):
    c.setFillColor(color)
    c.rect(0,0,W,H,fill=1,stroke=0)


def label(c,s,x,y,color=TEAL,size=9.0,tracking=0):
    c.setFillColor(color)
    c.setFont(BOLD,size)
    c.drawString(x,y,s)


def txt(c,s,x,y,size=10,color=INK,bold=False):
    c.setFillColor(color)
    c.setFont(BOLD if bold else BODY,size)
    c.drawString(x,y,str(s))


def wrap(c,text,x,y,maxwidth,size=10,leading=15,color=INK,bold=False,max_lines=None):
    font=BOLD if bold else BODY
    words=str(text).split()
    lines=[]
    line=""
    for word in words:
        trial=(line+" "+word).strip()
        if stringWidth(trial,font,size)<=maxwidth or not line:
            line=trial
        else:
            lines.append(line)
            line=word
    if line:lines.append(line)
    if max_lines is not None:lines=lines[:max_lines]
    for line in lines:
        txt(c,line,x,y,size,color,bold)
        y-=leading
    return y


def rect(c,x,y,w,h,fill=WHITE,stroke=BORDER,r=13):
    c.setFillColor(fill); c.setStrokeColor(stroke);c.setLineWidth(.8)
    c.roundRect(x,y,w,h,r,stroke=1,fill=1)


def line(c,x1,y1,x2,y2,color=BORDER,width=.8):
    c.setStrokeColor(color);c.setLineWidth(width);c.line(x1,y1,x2,y2)


def page(c,index,kicker):
    background(c)
    c.setFillColor(NAVY);c.rect(0,H-13,W,13,fill=1,stroke=0)
    label(c,"PROJETO INEP / PARAÍBA",42,H-48,TEAL,9.3)
    txt(c,kicker,W-42-stringWidth(kicker,BODY,8.6),H-48,8.6,MUTED)
    line(c,42,H-62,W-42,H-62)
    footer(c,index)


def footer(c,index):
    line(c,42,51,W-42,51)
    txt(c,"RELATÓRIO EXECUTIVO  |  12 NOV 2026",42,34,7.5,MUTED)
    n=f"{index:02d} / 05"
    txt(c,n,W-42-stringWidth(n,BOLD,8),33.5,8,MUTED,True)


def heading(c,kicker,title,subtitle):
    label(c,kicker.upper(),42,750,TEAL,9)
    txt(c,title,42,717,21,NAVY,True)
    wrap(c,subtitle,42,693,W-85,9.5,15,MUTED)


def metric(c,x,y,w,h,value,caption,extra=None):
    rect(c,x,y,w,h)
    c.setFillColor(TEAL);c.roundRect(x+13,y+h-8,27,3,1.5,fill=1,stroke=0)
    txt(c,value,x+15,y+h-37,23,NAVY,True)
    yy=wrap(c,caption,x+15,y+h-55,w-29,8.3,12,MUTED)
    if extra:
        txt(c,extra,x+15,y+10,7.2,TEAL,True)


def status(c,x,y,w,h,num,name,desc,chip,ready=True):
    rect(c,x,y,w,h)
    c.setFillColor(PALE if ready else AMBER_PALE)
    c.roundRect(x+13,y+h-33,38,20,8,fill=1,stroke=0)
    txt(c,num,x+24,y+h-27,9,TEAL if ready else AMBER,True)
    txt(c,name,x+60,y+h-29,10,NAVY,True)
    wrap(c,desc,x+15,y+h-51,w-30,8.2,11.5,MUTED,max_lines=3)
    txt(c,chip,x+15,y+10,7.6,TEAL if ready else AMBER,True)


def link(c,text,url,x,y,size=8.3):
    txt(c,text,x,y,size,BLUE,True)
    width=stringWidth(text,BOLD,size)
    line(c,x,y-2,x+width,y-2,BLUE,.7)
    c.linkURL(url,(x,y-4,x+width,y+size+2),relative=0,thickness=0)


def p1(c):
    background(c,NAVY)
    c.setFillColor(TEAL);c.rect(0,H-18,W,18,fill=1,stroke=0)
    c.setFillColor(HexColor("#1B394C"))
    c.circle(W+110,H-88,245,stroke=0,fill=1)
    c.setFillColor(HexColor("#214659"))
    c.circle(W+40,H-150,155,stroke=0,fill=1)
    label(c,"RELATÓRIO EXECUTIVO  /  VISÃO CONSOLIDADA",42,738,MINT,9.5)
    txt(c,"PROJETO INEP",42,655,35,WHITE,True)
    txt(c,"Educação pública na",42,602,23,WHITE,True)
    txt(c,"Paraíba",42,565,29,MINT,True)
    c.setFillColor(TEAL);c.roundRect(42,526,76,5,2.5,fill=1,stroke=0)
    wrap(c,"Panorama do desenvolvimento técnico e dos principais resultados da análise de dados sobre o ensino médio estadual da Paraíba.",42,489,438,11.5,19,HexColor("#DDEAF0"))
    rect(c,42,247,W-84,160,HexColor("#193849"),HexColor("#2C5362"),12)
    label(c,"O PROJETO EM NÚMEROS",60,378,MINT,8.6)
    points=[("482","escolas estaduais"),("223","municípios"),("456","escolas pareadas")]
    colw=(W-120)/3
    for i,(num,cap) in enumerate(points):
        x=62+i*colw
        txt(c,num,x,323,27,WHITE,True)
        wrap(c,cap,x,298,colw-12,8.6,13,HexColor("#C7DBE4"))
        if i<2:line(c,x+colw-12,288,x+colw-12,350,HexColor("#395A6C"))
    txt(c,"PROCESSAMENTO 2024 CONCLUÍDO",42,198,10,MINT,True)
    wrap(c,"Inclui filtragem, auditoria de chaves, limpeza e integração escolar. Os painéis e as análises de 2025 permanecem em evolução.",42,177,481,9.2,16,HexColor("#DDEAF0"))
    txt(c,"Fonte: INEP  |  Repositório: psoaresvieira/projeto_inep",42,71,8.8,HexColor("#B8D1DB"))
    c.linkURL(GITHUB,(42,65,490,89),relative=0,thickness=0)
    c.setStrokeColor(HexColor("#557488"));c.line(42,51,W-42,51)
    txt(c,"NOVEMBRO 2026  •  DOCUMENTO DE ACOMPANHAMENTO",42,32,7.7,HexColor("#A9C5D1"))
    c.showPage()


def p2(c):
    page(c,2,"VISÃO GERAL")
    heading(c,"01 / Visão geral","O que foi entregue","O projeto já conta com um fluxo reproduzível para 2024, indicadores consolidados e duas visualizações executivas.")
    x0=42;gap=10;mw=(W-84-2*gap)/3;h=94
    data=[
        ("482","Escolas estaduais com ensino médio","Censo 2024"),
        ("116.779","Matrículas declaradas","Censo 2024"),
        ("223","Municípios contemplados","Análise territorial"),
        ("456","Escolas ENEM–Censo pareadas","Integração 2024"),
        ("458","Escolas com IDEB válido","IDEB 2025"),
        ("98,69%","Registros ENEM pareados","ENEM–Censo 2024"),
    ]
    for i,(num,cap,extra) in enumerate(data):
        row,col=divmod(i,3)
        metric(c,x0+col*(mw+gap),560-row*106,mw,h,num,cap,extra)
    label(c,"PROGRESSO DAS SEIS ETAPAS",42,429,TEAL,9)
    specs=[
        ("01","Inspeção","Inventário das bases e análise de cabeçalhos.","2024 verificado; 2025 parcial",True),
        ("02","Filtragem","Recortes da PB e seleção da rede estadual.","2024 concluído",True),
        ("03","Limpeza","Ausências, notas inválidas e duplicidades.","2024 concluído",True),
        ("04","Integração","Junção segura pelo identificador escolar.","2024 concluído",True),
        ("05","Análise exploratória","Indicadores, gráficos e leitura municipal.","Preliminar publicada",False),
        ("06","Documentação","D.E.I.L.A.S., README e dashboards.","Em desenvolvimento",False),
    ]
    cw=(W-84-12)/2
    for i,(num,name,desc,chip,ready) in enumerate(specs):
        row,col=divmod(i,2)
        status(c,42+col*(cw+12),309-row*111,cw,100,num,name,desc,chip,ready)
    c.showPage()


def bar(c,x,y,width,name,count,total):
    pct=count/total
    txt(c,name,x,y+14,9,INK,True)
    rect(c,x,y-5,width,9,HexColor("#E4ECEF"),HexColor("#E4ECEF"),4)
    c.setFillColor(TEAL);c.roundRect(x,y-5,max(3,width*pct),9,4,stroke=0,fill=1)
    number=f"{count}/{total}  •  {pct*100:.1f}%".replace(".",",")
    right=x+width+7
    txt(c,number,right,y-3,7.7,MUTED)


def p3(c):
    page(c,3,"RESULTADOS ANALÍTICOS")
    heading(c,"02 / Evidências","Principais indicadores","Os indicadores descrevem redes, escolas e participantes distintos. Não são interpretações causais.")
    leftx=42;rightx=324;lw=270;rw=W-rightx-42
    rect(c,leftx,322,lw,342)
    txt(c,"Infraestrutura escolar",leftx+17,634,12,NAVY,True)
    txt(c,"Censo 2024 • 482 escolas estaduais",leftx+17,616,8.1,MUTED)
    infrastructure=[
        ("Internet",459),("Biblioteca",358),("Lab. informática",284),
        ("Quadra esportiva",248),("Lab. de ciências",233),
        ("Banda larga",139),("Sala de leitura",38)
    ]
    for idx,(name,num) in enumerate(infrastructure):
        # Barras em escala fixa, legendas numéricas à direita.
        bar(c,leftx+18,568-35.5*idx,143,name,num,482)
    rect(c,rightx,322,rw,342)
    txt(c,"ENEM 2024",rightx+16,634,12,NAVY,True)
    wrap(c,"Médias entre participantes com escola estadual da PB identificada e nota válida.",rightx+16,615,rw-32,8.2,13,MUTED)
    enem=[
        ("Natureza","456,53","21.786"),
        ("Humanas","467,67","22.487"),
        ("Linguagens","489,85","22.487"),
        ("Matemática","476,81","21.786"),
        ("Redação","571,92","22.487"),
    ]
    txt(c,"ÁREA",rightx+16,547,7.5,MUTED,True)
    txt(c,"MÉDIA",rightx+119,547,7.5,MUTED,True)
    for idx,(name,mean,nn) in enumerate(enem):
        yy=521-40*idx
        line(c,rightx+16,yy-11,rightx+rw-16,yy-11,BORDER)
        txt(c,name,rightx+16,yy,8.8,INK,True)
        txt(c,mean,rightx+119,yy,9.4,TEAL,True)
        txt(c,"n="+nn,rightx+119,yy-14,7.2,MUTED)
    # IDEB breakout
    rect(c,42,186,W-84,120,WHITE)
    label(c,"IDEB 2025  /  ESCOLAS ESTADUAIS",57,283,TEAL,8.7)
    ideb=[("478","Escolas na planilha"),("458","Com resultado válido"),("4,267","Média simples"),("4,3","Mediana")]
    cell=(W-114)/4
    for i,(value,caption) in enumerate(ideb):
        x=58+i*cell
        txt(c,value,x,247,19,NAVY,True)
        wrap(c,caption,x,228,cell-10,7.7,11,MUTED)
        if i<3:line(c,x+cell-10,211,x+cell-10,265,BORDER)
    rect(c,42,69,W-84,103,PALE,HexColor("#D3EDE7"),11)
    label(c,"COMO INTERPRETAR",56,149,TEAL,9)
    wrap(c,"A média simples do IDEB não equivale ao índice oficial agregado da rede. Os dados do ENEM cobrem apenas participantes identificáveis nos microdados, e não a totalidade das matrículas. Censo 2024 e IDEB 2025 referem-se a anos diferentes.",56,131,W-113,8.6,14,INK)
    c.showPage()


def mini_ui(c,x,y,w,h,variant):
    # Miniatura vetorial meramente esquemática, sem alegar screenshot exato.
    rect(c,x,y,w,h,WHITE,HexColor("#DAE6E8"),9)
    c.setFillColor(NAVY);c.roundRect(x+1,y+h-34,w-2,33,8,fill=1,stroke=0)
    c.setFillColor(NAVY);c.rect(x+1,y+h-34,w-2,16,fill=1,stroke=0)
    txt(c,"PAINEL  /  PARAÍBA",x+10,y+h-21,7,WHITE,True)
    if variant==1:
        for i,v in enumerate(("482","116.779","456")):
            xx=x+12+i*(w-28)/3
            rect(c,xx,y+h-89,(w-45)/3,41,LIGHT,LIGHT,4)
            txt(c,v,xx+7,y+h-69,10,NAVY,True)
        vals=[.95,.74,.59,.52,.48]
        for i,v in enumerate(vals):
            yy=y+h-111-i*17
            c.setFillColor(HexColor("#E6EFF1"));c.roundRect(x+18,yy,w-56,7,3,fill=1,stroke=0)
            c.setFillColor(TEAL);c.roundRect(x+18,yy,(w-56)*v,7,3,fill=1,stroke=0)
    else:
        rect(c,x+11,y+h-72,w-22,25,LIGHT,BORDER,4)
        txt(c,"Buscar município",x+20,y+h-63,7.5,MUTED)
        for i in range(4):
            yy=y+h-94-i*26
            line(c,x+14,yy-8,x+w-14,yy-8,BORDER)
            txt(c,["João Pessoa","Campina Grande","Sousa","Patos"][i],x+19,yy,7,NAVY,i==0)
            c.setFillColor(TEAL);c.roundRect(x+w-65,yy-1,34,4,2,fill=1,stroke=0)


def panel_card(c,y,heading,subtitle,bullets,linkname,url,variant):
    x=42;w=W-84;h=246
    rect(c,x,y,w,h)
    txt(c,heading,x+18,y+h-30,14,NAVY,True)
    wrap(c,subtitle,x+18,y+h-53,228,8.7,13,MUTED)
    yy=y+h-106
    for bullet in bullets:
        c.setFillColor(TEAL);c.circle(x+21,yy+3,2.4,fill=1,stroke=0)
        yy=wrap(c,bullet,x+32,yy,220,8.5,13,INK)-10
    link(c,linkname,url,x+18,y+20,8.1)
    mini_ui(c,x+274,y+26,w-292,h-77,variant)


def p4(c):
    page(c,4,"DASHBOARDS")
    heading(c,"03 / Produtos visuais","Dashboards desenvolvidos","Duas páginas HTML interativas foram geradas e testadas no GitHub Actions, usando indicadores agregados.")
    panel_card(
        c,416,"01  |  Painel executivo geral",
        "Visão macro para leitura das principais evidências educacionais.",
        [
            "Indicadores de escolas, matrículas e cobertura.",
            "Infraestrutura, médias do ENEM e IDEB.",
            "Abas de panorama, aprendizagem e metodologia.",
        ],
        "Abrir dashboard geral",
        GITHUB+"/blob/main/dashboard/index.html",1
    )
    panel_card(
        c,153,"02  |  Visão territorial",
        "Exploração dos 223 municípios da Paraíba.",
        [
            "Pesquisa por nome ou código IBGE.",
            "Ordenação por escolas, matrículas e banda larga.",
            "Dados Censo 2024 e IDEB 2025 em visões separadas.",
        ],
        "Abrir dashboard municipal",
        GITHUB+"/blob/main/dashboard/municipios.html",2
    )
    txt(c,"Pré-visualizações esquemáticas das interfaces; não são capturas de tela.",42,86,7.8,MUTED)
    c.showPage()


def priority(c,y,num,title,text,status="ALTA PRIORIDADE",optional=False):
    rect(c,42,y,W-84,95)
    c.setFillColor(AMBER_PALE if not optional else LIGHT)
    c.roundRect(56,y+56,35,25,8,fill=1,stroke=0)
    txt(c,num,67,y+64,9,AMBER if not optional else MUTED,True)
    txt(c,title,103,y+68,10.5,NAVY,True)
    wrap(c,text,103,y+50,W-175,8.6,13,MUTED,max_lines=2)
    txt(c,status,103,y+13,7.4,AMBER if not optional else MUTED,True)


def p5(c):
    page(c,5,"PLANO DE CONTINUIDADE")
    heading(c,"04 / Próximos passos","Do painel ao diagnóstico","As próximas entregas devem aprofundar o significado dos dados e apoiar propostas verificáveis de política pública.")
    priority(c,576,"01","Completar a base temporal de 2025",
             "Adaptar a nova estrutura do Censo 2025 e resolver a leitura do arquivo de resultados do ENEM 2025.")
    priority(c,473,"02","Aprofundar a análise educacional",
             "Estudar desigualdades territoriais, distribuições por escola e indicadores comparáveis ao longo do tempo.")
    priority(c,370,"03","Consolidar recomendações ao governador",
             "Transformar achados em hipóteses de intervenção, com critérios de priorização, limites e métricas de monitoramento.")
    priority(c,267,"04","Finalizar entrega acadêmica e visual",
             "Revisar os dashboards, concluir o relatório final e a documentação D.E.I.L.A.S.; hospedagem é opcional.")
    rect(c,42,85,W-84,166,PALE,HexColor("#CDE8E3"),11)
    label(c,"PONTOS DE CONTROLE METODOLÓGICO",57,225,TEAL,8.8)
    cautions=[
        "O ENEM não cobre automaticamente toda a população da rede pública.",
        "Questionários e notas do ENEM não foram unidos sem chave individual validada.",
        "IDEB 2025 e Censo 2024 não devem ser tratados como o mesmo período.",
        "Os dados permitem diagnósticos descritivos, não inferências causais imediatas."
    ]
    y=200
    for s in cautions:
        c.setFillColor(TEAL);c.circle(61,y+3,2.5,fill=1,stroke=0)
        wrap(c,s,73,y,W-132,8.6,14,INK)
        y-=27
    link(c,"Acessar o repositório e a documentação",GITHUB,42,68,8.2)
    c.showPage()


def main():
    c=canvas.Canvas(str(OUTPUT),pagesize=A4,pageCompression=1,
                    invariant=1)
    c.setTitle("Projeto INEP — Overview executivo da análise de dados da Paraíba")
    c.setAuthor("Projeto INEP — Análise de Dados")
    c.setSubject("Status, resultados, dashboards e próximos passos — novembro de 2026")
    p1(c);p2(c);p3(c);p4(c);p5(c)
    c.save()
    print("Gerado:",OUTPUT)
    print("Bytes:",OUTPUT.stat().st_size)


if __name__=="__main__":
    main()
