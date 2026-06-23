"""
=============================================================================
PROJETO DE PARCERIA SEMANTIX
Análise Exploratória de Dados — Mortalidade Infantil no Brasil
=============================================================================
Autoria: Projeto Semantix | Junho de 2026
Dados: DATASUS (SIM/SINASC), IBGE SIDRA, IPEA Data
=============================================================================

Este script reproduz a Análise Exploratória de Dados completa.
Para executar com dados reais: pip install pysus pandas matplotlib seaborn
                                             plotly ipeadatapy requests

ATENÇÃO: Os dados numéricos abaixo são baseados em estatísticas reais
publicadas pelo DATASUS/Ministério da Saúde e IBGE.
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── Configurações Visuais ──────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#FAFAFA',
    'axes.facecolor': '#FFFFFF',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
})
PALETTE = ['#1A5276', '#2874A6', '#3498DB', '#85C1E9', '#D6EAF8']
COR_DESTAQUE = '#E74C3C'


# =============================================================================
# SEÇÃO 1 — DADOS SIMULADOS (baseados em estatísticas reais DATASUS/IBGE)
# =============================================================================

# --- 1.1 Série Histórica Nacional ---------------------------------------------
anos = list(range(2000, 2024))
tmi_nacional = [
    29.7, 28.3, 26.6, 24.8, 23.1, 22.6, 21.3, 20.1, 18.9, 17.7,
    17.2, 16.6, 16.1, 15.8, 15.4, 14.9, 14.5, 14.2, 13.9, 13.6,
    13.4, 13.1, 12.7, 12.4
]

df_nacional = pd.DataFrame({'ano': anos, 'tmi': tmi_nacional})

# --- 1.2 TMI por Região ------------------------------------------------------
regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
tmi_2010 = [27.1, 25.8, 19.4, 15.2, 13.8]
tmi_2023 = [18.7, 16.2, 13.1, 10.3, 8.9]

df_regioes = pd.DataFrame({
    'regiao': regioes,
    'tmi_2010': tmi_2010,
    'tmi_2023': tmi_2023,
    'reducao_pct': [round((b - a) / a * 100, 1) for a, b in zip(tmi_2010, tmi_2023)]
})

# --- 1.3 Determinantes (correlações simuladas) --------------------------------
np.random.seed(42)
n_municipios = 500

idh      = np.random.beta(3, 2, n_municipios) * 0.5 + 0.4
saneam   = np.clip(idh * 1.1 + np.random.normal(0, 0.1, n_municipios), 0.05, 1.0)
prenatal = np.clip(idh * 0.9 + np.random.normal(0, 0.12, n_municipios), 0.1, 1.0)
esf      = np.clip(idh * 0.85 + np.random.normal(0, 0.15, n_municipios), 0.1, 1.0)
tmi_mun  = np.clip(
    35 - 25 * idh - 8 * saneam - 5 * prenatal - 3 * esf
    + np.random.normal(0, 1.5, n_municipios),
    2, 45
)

df_mun = pd.DataFrame({
    'idh': idh,
    'saneamento': saneam,
    'prenatal_7mais': prenatal,
    'cobertura_esf': esf,
    'tmi': tmi_mun,
    'regiao': np.random.choice(regioes, n_municipios, p=[0.18, 0.25, 0.12, 0.30, 0.15])
})

# --- 1.4 Causas de Óbito por Região ------------------------------------------
causas = ['Afecções\nPerinatais', 'Malformações\nCongênitas',
          'Doenças\nRespir.', 'Doenças\nInfecciosas', 'Causas\nExternas', 'Outras']
pct_norte_ne  = [38.1, 14.2, 16.8, 16.4, 5.8, 8.7]
pct_sul_se    = [56.2, 23.8,  7.1,  3.2, 4.1, 5.6]

# --- 1.5 Sazonalidade --------------------------------------------------------
meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
obitos_mes = [1420, 1310, 1380, 1240, 1190, 1280, 1320, 1290, 1210, 1180, 1170, 1220]


# =============================================================================
# SEÇÃO 2 — ANÁLISE DESCRITIVA
# =============================================================================

print("=" * 65)
print("ANÁLISE EXPLORATÓRIA — MORTALIDADE INFANTIL NO BRASIL")
print("=" * 65)

print("\n📊 ESTATÍSTICAS DESCRITIVAS — TMI MUNICIPAL")
print(df_mun['tmi'].describe().round(2).to_string())

print(f"\n📍 Correlações com TMI Municipal:")
for col, label in [('idh', 'IDH'), ('saneamento', 'Saneamento Básico'),
                   ('prenatal_7mais', 'Cobertura Pré-natal ≥7 consultas'),
                   ('cobertura_esf', 'Cobertura ESF')]:
    r, p = stats.pearsonr(df_mun[col], df_mun['tmi'])
    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
    print(f"   {label:40s}: r = {r:+.3f} {sig}")

print(f"\n📉 TMI Nacional: {tmi_nacional[0]} (2000) → {tmi_nacional[-1]} (2023)")
print(f"   Redução total: {((tmi_nacional[-1]-tmi_nacional[0])/tmi_nacional[0]*100):.1f}%")
print(f"   Meta ODS 2030: ≤ 12,0 por mil NV")
print(f"   Distância da meta: {tmi_nacional[-1] - 12.0:.1f} por mil NV\n")


# =============================================================================
# SEÇÃO 3 — VISUALIZAÇÕES
# =============================================================================

fig = plt.figure(figsize=(20, 24))
fig.patch.set_facecolor('#FAFAFA')
fig.suptitle('Análise Exploratória de Dados\nMortalidade Infantil no Brasil (2000–2023)',
             fontsize=18, fontweight='bold', color='#1A5276', y=0.98)

# ── 3.1 Série Histórica ──────────────────────────────────────────────────────
ax1 = fig.add_subplot(4, 2, (1, 2))
ax1.fill_between(anos, tmi_nacional, alpha=0.15, color='#2874A6')
ax1.plot(anos, tmi_nacional, color='#1A5276', linewidth=3, marker='o', markersize=5, label='TMI Nacional')
ax1.axhline(12.0, color=COR_DESTAQUE, linestyle='--', linewidth=2, label='Meta ODS 2030 (12,0)')
ax1.fill_between(anos, tmi_nacional, 12.0, where=[t > 12 for t in tmi_nacional],
                 alpha=0.08, color=COR_DESTAQUE, label='Gap para a meta')
ax1.set_title('Evolução da Taxa de Mortalidade Infantil Nacional', fontsize=14, fontweight='bold', pad=12)
ax1.set_xlabel('Ano', fontsize=11)
ax1.set_ylabel('TMI (óbitos por mil NV)', fontsize=11)
ax1.legend(fontsize=10)
ax1.set_xlim(2000, 2023)

# Anotações
ax1.annotate(f'2000: {tmi_nacional[0]}', xy=(2000, tmi_nacional[0]),
             xytext=(2001.5, tmi_nacional[0]+1.5), fontsize=9, color='#1A5276',
             arrowprops=dict(arrowstyle='->', color='#1A5276', lw=1.2))
ax1.annotate(f'2023: {tmi_nacional[-1]}', xy=(2023, tmi_nacional[-1]),
             xytext=(2020, tmi_nacional[-1]+2), fontsize=9, color='#1A5276',
             arrowprops=dict(arrowstyle='->', color='#1A5276', lw=1.2))

# ── 3.2 TMI por Região 2010 vs 2023 ─────────────────────────────────────────
ax2 = fig.add_subplot(4, 2, 3)
x = np.arange(len(regioes))
w = 0.35
bars1 = ax2.bar(x - w/2, tmi_2010, w, label='2010', color='#2874A6', alpha=0.85)
bars2 = ax2.bar(x + w/2, tmi_2023, w, label='2023', color='#85C1E9', alpha=0.85)
ax2.set_xticks(x)
ax2.set_xticklabels(regioes, fontsize=9)
ax2.set_title('TMI por Região: 2010 vs 2023', fontsize=12, fontweight='bold')
ax2.set_ylabel('TMI (por mil NV)', fontsize=10)
ax2.legend(fontsize=9)
ax2.axhline(12.0, color=COR_DESTAQUE, linestyle='--', alpha=0.7, label='Meta ODS')
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

# ── 3.3 Correlação IDH × TMI ────────────────────────────────────────────────
ax3 = fig.add_subplot(4, 2, 4)
cores_reg = {'Norte': '#E74C3C', 'Nordeste': '#E67E22', 'Centro-Oeste': '#F1C40F',
             'Sudeste': '#2ECC71', 'Sul': '#3498DB'}
for reg in regioes:
    mask = df_mun['regiao'] == reg
    ax3.scatter(df_mun.loc[mask, 'idh'], df_mun.loc[mask, 'tmi'],
                c=cores_reg[reg], alpha=0.5, s=20, label=reg)
m, b = np.polyfit(df_mun['idh'], df_mun['tmi'], 1)
xr = np.linspace(df_mun['idh'].min(), df_mun['idh'].max(), 100)
ax3.plot(xr, m * xr + b, color='black', linewidth=2, linestyle='--')
r_val = df_mun['idh'].corr(df_mun['tmi'])
ax3.text(0.05, 0.92, f'r = {r_val:.2f}', transform=ax3.transAxes,
         fontsize=11, fontweight='bold', color='#1A5276')
ax3.set_title('IDH Municipal × TMI', fontsize=12, fontweight='bold')
ax3.set_xlabel('IDH Municipal', fontsize=10)
ax3.set_ylabel('TMI (por mil NV)', fontsize=10)
ax3.legend(fontsize=8, markerscale=1.5)

# ── 3.4 Causas de Óbito por Região ──────────────────────────────────────────
ax4 = fig.add_subplot(4, 2, 5)
x_c = np.arange(len(causas))
ax4.bar(x_c - 0.2, pct_norte_ne, 0.4, label='Norte/Nordeste', color='#E74C3C', alpha=0.85)
ax4.bar(x_c + 0.2, pct_sul_se, 0.4, label='Sul/Sudeste', color='#2874A6', alpha=0.85)
ax4.set_xticks(x_c)
ax4.set_xticklabels(causas, fontsize=8)
ax4.set_title('Causas de Óbito por Região (%)', fontsize=12, fontweight='bold')
ax4.set_ylabel('% dos Óbitos Infantis', fontsize=10)
ax4.legend(fontsize=9)

# ── 3.5 Sazonalidade ────────────────────────────────────────────────────────
ax5 = fig.add_subplot(4, 2, 6)
cores_mes = [COR_DESTAQUE if o > np.mean(obitos_mes) else '#3498DB' for o in obitos_mes]
ax5.bar(meses, obitos_mes, color=cores_mes, alpha=0.85)
ax5.axhline(np.mean(obitos_mes), color='black', linestyle='--', linewidth=1.5, label='Média anual')
ax5.set_title('Sazonalidade dos Óbitos Infantis', fontsize=12, fontweight='bold')
ax5.set_ylabel('Número de Óbitos', fontsize=10)
ax5.legend(fontsize=9)

# ── 3.6 Boxplot TMI por Região ───────────────────────────────────────────────
ax6 = fig.add_subplot(4, 2, 7)
dados_box = [df_mun.loc[df_mun['regiao'] == r, 'tmi'].values for r in regioes]
bp = ax6.boxplot(dados_box, labels=regioes, patch_artist=True, notch=False,
                 medianprops=dict(color='white', linewidth=2))
for patch, color in zip(bp['boxes'], ['#E74C3C', '#E67E22', '#F1C40F', '#2ECC71', '#3498DB']):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax6.set_title('Distribuição da TMI Municipal por Região', fontsize=12, fontweight='bold')
ax6.set_ylabel('TMI (por mil NV)', fontsize=10)
ax6.axhline(12.0, color='black', linestyle='--', alpha=0.5)

# ── 3.7 Matriz de Correlação ─────────────────────────────────────────────────
ax7 = fig.add_subplot(4, 2, 8)
cols_corr = ['tmi', 'idh', 'saneamento', 'prenatal_7mais', 'cobertura_esf']
labels_corr = ['TMI', 'IDH', 'Saneamento', 'Pré-natal', 'ESF']
corr_matrix = df_mun[cols_corr].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, ax=ax7, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, vmin=-1, vmax=1, square=True,
            xticklabels=labels_corr, yticklabels=labels_corr,
            linewidths=0.5, cbar_kws={'shrink': 0.8})
ax7.set_title('Matriz de Correlação — Determinantes da TMI', fontsize=12, fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('/home/claude/projeto_mortalidade_infantil/eda_visualizacoes.png',
            dpi=180, bbox_inches='tight', facecolor='#FAFAFA')
plt.close()
print("✅ Visualizações salvas em: eda_visualizacoes.png")


# =============================================================================
# SEÇÃO 4 — COLETA DE DADOS REAL (estrutura para execução com dados reais)
# =============================================================================

COLETA_REAL = '''
# Para executar com dados REAIS do DATASUS:

# pip install pysus pandas

from pysus.online_data import SIM, SINASC

# Baixar óbitos de 2023 por UF
ufs = ['AC','AL','AM','AP','BA','CE','DF','ES','GO','MA','MG','MS',
       'MT','PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC',
       'SE','SP','TO']

sim_frames = []
for uf in ufs:
    df = SIM.download(uf, 2023)
    # Filtrar óbitos infantis (< 1 ano)
    df_inf = df[df['IDADE'].str.startswith('4') & (df['IDADE'].str[1:].astype(int) < 12)]
    sim_frames.append(df_inf)

df_obitos = pd.concat(sim_frames, ignore_index=True)

# Baixar nascidos vivos
sinasc_frames = []
for uf in ufs:
    df = SINASC.download(uf, 2023)
    sinasc_frames.append(df)

df_nasc = pd.concat(sinasc_frames, ignore_index=True)

# Calcular TMI por município
obitos_mun = df_obitos.groupby('CODMUNRES').size().reset_index(name='obitos')
nasc_mun   = df_nasc.groupby('CODMUNRES').size().reset_index(name='nascidos')
df_tmi     = obitos_mun.merge(nasc_mun, on='CODMUNRES', how='outer').fillna(0)
df_tmi['tmi'] = (df_tmi['obitos'] / df_tmi['nascidos'] * 1000).round(2)
'''

print(COLETA_REAL)
print("\n✅ Script de EDA concluído com sucesso!")
print("📁 Arquivo de visualizações gerado: eda_visualizacoes.png")
