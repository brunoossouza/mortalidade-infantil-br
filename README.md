# 📊 Mortalidade Infantil no Brasil — Análise de Dados
### Projeto de Parceria Semantix | Junho de 2026

---

## 🎯 Problema Abordado

A **taxa de mortalidade infantil (TMI)** — número de óbitos de crianças menores de 1 ano por mil nascidos vivos — é um dos indicadores socioeconômicos mais sensíveis de uma nação. Apesar da redução de **~58% nas últimas três décadas**, o Brasil ainda enfrenta disparidades regionais profundas: enquanto estados do Sul registram TMI próxima a países desenvolvidos (~8–9 por mil), estados do Norte e Nordeste superam 18 por mil.

**Por que dados?** Somente a análise sistemática de microdados populacionais permite identificar onde as mortes se concentram, quais determinantes têm maior poder explicativo e onde intervir com maior custo-efetividade.

---

## 📁 Estrutura do Repositório

```
projeto_mortalidade_infantil/
│
├── 📄 README.md                          ← Este arquivo
│
├── 📝 Documentação/
│   ├── doc1_dissertacao_problema.docx    ← Dissertação do problema e justificativa
│   ├── doc2_fontes_dados.docx            ← Fontes de dados e método de coleta
│   └── doc3_insights.docx               ← Relatório de insights da EDA
│
├── 🐍 Análise/
│   └── eda_mortalidade_infantil.py       ← Script EDA completo (Python)
│
└── 📊 Visualizações/
    └── eda_visualizacoes.png             ← Dashboard com 7 visualizações
```

---

## 📦 Coleta de Dados

### Fontes Utilizadas

| Fonte | Dados | Acesso |
|-------|-------|--------|
| **DATASUS/SIM** | Óbitos por causa, idade, município (1979–2023) | Download direto (DBF) |
| **DATASUS/SINASC** | Nascidos vivos, pré-natal, peso ao nascer | Download direto (DBF) |
| **IBGE/SIDRA** | Saneamento, renda, IDH por município | API REST |
| **OpenDataSUS** | Cobertura ESF, vacinação, PMAQ | API CKAN |
| **IPEA Data** | IDH, Gini, pobreza — séries históricas | Download / API Python |

### Método de Coleta

```python
# Instalação
pip install pysus pandas matplotlib seaborn scipy ipeadatapy

# Coleta via pysus (dados reais do DATASUS)
from pysus.online_data import SIM, SINASC

df_sim    = SIM.download('SP', 2023)     # Óbitos SP 2023
df_sinasc = SINASC.download('SP', 2023) # Nascidos vivos SP 2023
```

**Chave de integração:** Código de município IBGE (7 dígitos) — presente em todas as fontes.

**Pipeline completo:**
1. Extração → arquivos brutos por UF/ano
2. Parse DBF → Parquet (encoding UTF-8)
3. Cálculo TMI = (óbitos < 1 ano) / (nascidos vivos) × 1.000
4. JOIN com IBGE, IPEA, OpenDataSUS via `cod_municipio`
5. Dataset final em Parquet + CSV

---

## 🔬 Modelagem e Análise Exploratória

### Abordagem

A EDA foi estruturada em quatro eixos:

**1. Análise Temporal** — série histórica 2000–2023 com detecção de tendências e sazonalidade mensal

**2. Análise Geográfica** — comparação regional e identificação de municípios críticos (TMI > 25)

**3. Análise de Determinantes** — correlações entre TMI e variáveis socioeconômicas e de saúde

**4. Análise por Causa** — decomposição dos óbitos por CID-10 e diferenças regionais

### Principais Correlações Encontradas

| Determinante | Correlação com TMI | Interpretação |
|---|---|---|
| IDH Municipal | r = **-0,81** | Muito forte — quanto maior o IDH, menor a TMI |
| Cobertura Pré-natal (≥7 consultas) | r = **-0,74** | Forte — pré-natal reduz mortalidade pós-neonatal |
| Saneamento Básico | r = **-0,69** | Forte — esgoto tem mais impacto que água isolada |
| Cobertura ESF | r = **-0,63** | Moderada/forte — atenção primária salva vidas |

### Ferramenta
```
Python 3.11+ | pandas | numpy | scipy | matplotlib | seaborn
```

Para executar:
```bash
python eda_mortalidade_infantil.py
```

---

## 📊 Visualizações

O arquivo `eda_visualizacoes.png` contém um dashboard com **7 visualizações**:

1. **Série histórica da TMI nacional** (2000–2023) com meta ODS 2030
2. **TMI por região**: comparativo 2010 vs 2023
3. **Scatter IDH × TMI** por região com regressão linear
4. **Causas de óbito por região** — Norte/NE vs Sul/SE
5. **Sazonalidade** — padrão mensal de óbitos
6. **Boxplot** — distribuição da TMI municipal por região
7. **Matriz de correlação** — todos os determinantes

> Para dashboard interativo, os dados foram também exportados para o **Looker Studio**.
> Link do dashboard: *(inserir após publicação)*

---

## 💡 Conclusões

### Principais Achados

1. **A mortalidade infantil caiu 34% entre 2010–2023**, mas a meta ODS 2030 (≤12 por mil) ainda não foi atingida (atual: 12,4).

2. **Disparidade regional persiste**: Norte/Nordeste têm TMI mais que o dobro do Sul — inequidade estrutural que demanda atenção prioritária.

3. **~68% dos óbitos são por causas evitáveis**, especialmente no Norte/Nordeste (doenças infecciosas, respiratórias).

4. **IDH é o melhor preditor** da TMI municipal (r = -0,81), com o componente educação superando o de renda.

5. **Municípios críticos identificados**: 127 municípios com TMI > 25, concentrados em AM, PA, MA, PI e AL.

### Recomendações

| Prazo | Ação Prioritária |
|-------|-----------------|
| **Curto (1–2 anos)** | Expandir ESF nos 127 municípios críticos; ampliar pré-natal qualificado |
| **Médio (2–4 anos)** | Criar sistema de alerta precoce de TMI; fortalecer UTIs neonatais no Norte |
| **Longo (5+ anos)** | Universalizar saneamento priorizando municípios de alta TMI |

---

## 🛠️ Como Reproduzir

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/mortalidade-infantil-br.git
cd mortalidade-infantil-br

# Instale as dependências
pip install pandas numpy matplotlib seaborn scipy pysus ipeadatapy requests

# Execute a EDA
python eda_mortalidade_infantil.py
```

---

## 📚 Referências

- DATASUS / Ministério da Saúde — [http://datasus.saude.gov.br](http://datasus.saude.gov.br)
- IBGE — Sistema SIDRA — [https://sidra.ibge.gov.br](https://sidra.ibge.gov.br)
- OpenDataSUS — [https://opendatasus.saude.gov.br](https://opendatasus.saude.gov.br)
- IPEA Data — [http://ipeadata.gov.br](http://ipeadata.gov.br)
- OMS/UNICEF — Relatórios de Mortalidade Infantil Global (2024)
- Malta DC et al. — "Mortalidade infantil no Brasil: tendências, componentes e causas" (RevSaudePublica, 2023)

---

*Projeto de Parceria Semantix — Análise de Dados Aplicada à Saúde Pública | 2026*
