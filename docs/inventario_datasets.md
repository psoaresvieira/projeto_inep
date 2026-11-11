# Inventário inicial dos datasets — Paraíba

**Status:** coleta parcial e inspeção interna pendente (11/11/2026).

## Arquivos recebidos nesta conversa

| Pacote | Tamanho do arquivo recebido | Origem declarada | Validação interna |
|---|---:|---|---|
| `microdados_enem_2024.zip` | 526.073.856 bytes | Microdados ENEM 2024 (INEP) | Pendente |
| `microdados_censo_escolar_2024.zip` | 33.829.396 bytes | Microdados Censo Escolar 2024 (INEP) | Pendente |
| `divulgacao_ensino_medio_escolas_2025(1).zip` | 18.989.748 bytes | Resultados IDEB 2025 — ensino médio, escolas (INEP) | Pendente |

**Importante:** os tamanhos acima são metadados dos anexos recebidos, e não resultados de processamento dos conteúdos. Não foram verificados quantidade de registros, campos, ZIP íntegro ou chaves.

## Arquivos ainda previstos
- ENEM 2025;
- Censo Escolar 2025;
- Taxas de rendimento escolar 2024/2025 (complementares);
- SAEB (opcional, para complementar diagnóstico de aprendizagem).

## Procedimento de inspeção

Execute o script do repositório em um computador com acesso aos ZIPs:

```bash
python src/01_inspecao.py --arquivos "dados_brutos/microdados_enem_2024.zip" "dados_brutos/microdados_censo_escolar_2024.zip" "dados_brutos/divulgacao_ensino_medio_escolas_2025(1).zip"
```

O script gera `reports/inspecao/inventario.md` e `reports/inspecao/inventario.json`, contendo nomes de arquivos internos, tamanhos e amostras de cabeçalhos tabulares.

O script **não** calcula contagem completa de linhas, registros nulos ou chaves. A análise detalhada ocorrerá somente após verificar os dicionários.

## Pontos a validar após execução
1. Colunas adequadas para delimitar o ENEM à população da Paraíba, distinguindo escola, residência e local de prova;
2. Campos do Censo para escola, município, dependência administrativa e oferta de ensino médio;
3. Granularidade efetiva do arquivo IDEB 2025;
4. Capacidade de união temporal e junção por chaves comuns, sem multiplicação artificial de registros;
5. Contagens reais por UF, escola, rede e ano;
6. Definições oficiais e unidades de observação de cada base.

**Não publicar microdados nacionais ou arquivos ZIP de centenas de MB neste repositório.** Preserve-os localmente e versionem-se scripts e relatórios de inspeção sem dados pessoais.