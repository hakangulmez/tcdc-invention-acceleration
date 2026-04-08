#!/usr/bin/env python3
"""Add Sections 13-16 to the notebook with correct source formatting."""
import json
import os

os.chdir('/Users/hakanzekigulmez/Desktop/tcdc-invention-acceleration')

nb = json.load(open('main_analysis.ipynb'))

def make_source_lines(text):
    """Convert text to proper nbformat source: list of lines each ending with \\n except last."""
    lines = text.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            result.append(line + '\n')
        else:
            result.append(line)
    return result

def md_cell(source):
    return {"cell_type": "markdown", "metadata": {}, "source": make_source_lines(source)}

def code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": make_source_lines(source)
    }

new_cells = []

# === SECTION 13 ===
new_cells.append(md_cell("""---

## 13. Extended GPT Dataset — Rönesans & Banking Era

This section documents the expansion of the GPT dataset from 24 to 30 technologies,
adding Renaissance and pre-industrial innovations that were missing from the original Lipsey et al. framework."""))

new_cells.append(code_cell("""# === Section 13: Extended GPT Dataset ===
import pandas as pd
import numpy as np

gpt_df = pd.read_csv('data/processed/gpt_dataset.csv')
print(f"Updated GPT count: {len(gpt_df)}")
print(f"\\nNew GPTs added (IDs 25-30):")

new_gpts = gpt_df[gpt_df['id'].isin([25, 26, 27, 28, 29, 30])]
for _, row in new_gpts.iterrows():
    print(f"  ID {int(row['id'])}: {row['name']} ({int(row['year'])})")
    print(f"    Omega-shift: {row['omega_shift_description']}")
    print(f"    Source: {row['source']}")
    print()

print("=" * 70)
print("Updated Interval Calculations (sorted by year):")
print("=" * 70)
display_cols = ['name', 'year', 'interval_years', 'log_interval']
print(gpt_df[display_cols].to_string(index=False))

print(f"\\nKey interval changes due to new GPTs:")
print(f"  - Printing Press: 1750 -> 110 years (Mechanical Clock now precedes it)")
print(f"  - Steam Engine: 319 -> 69 years (Crop Rotation fills the gap)")
print(f"  - Steel Production: 31 -> 19 years (Telegraph inserted before)")"""))

# === SECTION 14 ===
new_cells.append(md_cell("""---

## 14. Real Maddison Data Integration

We integrate real GDP per capita data for Western Europe from the Maddison Project Database,
using published estimates from Maddison (2007) *Contours of the World Economy 1-2030 AD*
and Bolt & van Zanden (2024) *Journal of Economic Surveys*.

This replaces the approximate GDP values in the original dataset with historically consistent estimates."""))

new_cells.append(code_cell("""# === Section 14: Real Maddison Data Integration ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

maddison_df = pd.read_csv('data/raw/maddison_western_europe.csv')
gpt_df = pd.read_csv('data/processed/gpt_dataset.csv')

print("Maddison Project Database -- Western Europe GDP per capita (2011 US$)")
print(f"Observations: {len(maddison_df)}, Period: {maddison_df['year'].min()}-{maddison_df['year'].max()}")
print(f"Source: Maddison (2007) + Bolt & van Zanden (2024)\\n")
print(maddison_df.to_string(index=False))

gpt_post1000 = gpt_df[gpt_df['year'] >= 1000].copy()
interp_func = interp1d(maddison_df['year'], maddison_df['gdppc_2011usd'],
                        kind='linear', fill_value='extrapolate')

print("\\n" + "=" * 70)
print("GDP Context Around Each GPT Arrival (post-1000 CE)")
print("=" * 70)
for _, gpt in gpt_post1000.iterrows():
    y = gpt['year']
    gdp_at = float(interp_func(y))
    gdp_before = float(interp_func(max(1, y - 50)))
    growth = (gdp_at - gdp_before) / gdp_before * 100
    print(f"  {gpt['name']:45s} ({int(y)}): GDP=${gdp_at:,.0f}, 50yr growth={growth:+.1f}%")"""))

new_cells.append(code_cell("""# === Figure 6: GDP Trajectory with GPT Markers ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

maddison_df = pd.read_csv('data/raw/maddison_western_europe.csv')
gpt_df = pd.read_csv('data/processed/gpt_dataset.csv')

years_fine = np.arange(1000, 2018)
interp_func = interp1d(maddison_df['year'], maddison_df['gdppc_2011usd'],
                        kind='linear', fill_value='extrapolate')
gdp_fine = interp_func(years_fine)

gpt_post1000 = gpt_df[(gpt_df['year'] >= 1000) & (gpt_df['year'] <= 2017)].copy()
gpt_post1000 = gpt_post1000.drop_duplicates(subset='year')
gpt_post1000['gdp_at_arrival'] = gpt_post1000['year'].apply(lambda y: float(interp_func(y)))

def era_color(year):
    if year < 1450: return '#8B4513'
    elif year < 1769: return '#DAA520'
    elif year < 1882: return '#FF6347'
    elif year < 1971: return '#4169E1'
    else: return '#9370DB'

era_labels = {
    'Medieval (pre-1450)': '#8B4513',
    'Renaissance (1450-1769)': '#DAA520',
    'Steam (1769-1882)': '#FF6347',
    'Electric (1882-1971)': '#4169E1',
    'Digital (1971+)': '#9370DB'
}

fig, ax = plt.subplots(figsize=(22, 10))
ax.semilogy(years_fine, gdp_fine, 'k-', lw=2.5, alpha=0.8, label='Western Europe GDP/capita')

gpt_years_sorted = sorted(gpt_post1000['year'].unique())
for i in range(len(gpt_years_sorted) - 1):
    y1, y2 = gpt_years_sorted[i], gpt_years_sorted[i + 1]
    color = era_color(y1)
    ax.axvspan(y1, y2, alpha=0.06, color=color)

for _, gpt in gpt_post1000.iterrows():
    color = era_color(gpt['year'])
    ax.axvline(gpt['year'], color=color, lw=1.2, ls='--', alpha=0.6)
    ax.scatter(gpt['year'], gpt['gdp_at_arrival'], color=color, s=80, zorder=5,
               edgecolors='black', lw=0.5)
    name_short = gpt['name'].split('(')[0].strip()[:25]
    ax.annotate(name_short, (gpt['year'], gpt['gdp_at_arrival']),
                xytext=(5, 15), textcoords='offset points',
                fontsize=7, rotation=45, color=color, fontweight='bold',
                arrowprops=dict(arrowstyle='-', color=color, alpha=0.3))

for label, color in era_labels.items():
    ax.plot([], [], color=color, lw=3, label=label)

ax.set_xlabel('Year', fontsize=13)
ax.set_ylabel('GDP per capita (2011 US$, log scale)', fontsize=13)
ax.set_title('Figure 6: Western Europe GDP Trajectory with GPT Arrivals\\n'
             'Maddison Project Database -- Each vertical line marks a General Purpose Technology',
             fontsize=14, fontweight='bold')
ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
ax.set_xlim(1000, 2030)
ax.grid(True, alpha=0.3)
ax.text(0.02, 0.02,
        'Data: Maddison (2007), Bolt & van Zanden (2024)\\n'
        'Note: Shaded regions show within-Omega periods;\\n'
        'GPT arrivals shift the technological frontier',
        transform=ax.transAxes, fontsize=9, verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('figures/fig6_maddison_gdp_trajectory.png', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig6_maddison_gdp_trajectory.pdf', bbox_inches='tight')
plt.close()
print("Saved: figures/fig6_maddison_gdp_trajectory.png/.pdf")"""))

# === SECTION 15 ===
new_cells.append(md_cell("""---

## 15. GDP Growth Event Study: Do GPTs Create Growth Boosts?

This is the core new empirical contribution. We conduct an event study around GPT arrivals
to test whether General Purpose Technologies generate measurable GDP growth accelerations.

**Method**: For each post-1500 GPT (where Maddison data has adequate coverage):
- Extract GDP growth rates for +/-50 years around the GPT arrival
- Calculate the average growth *boost* = mean(post) - mean(pre)
- Aggregate across all GPTs to identify systematic patterns

**Key prediction (TCDC theory)**: GPT arrivals should produce positive growth boosts,
as they shift the technological frontier Omega and open new combinatorial possibilities."""))

new_cells.append(code_cell("""# === Section 15A: Event Study Setup ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy import stats

maddison_df = pd.read_csv('data/raw/maddison_western_europe.csv')
gpt_df = pd.read_csv('data/processed/gpt_dataset.csv')

interp_func = interp1d(maddison_df['year'], maddison_df['gdppc_2011usd'],
                        kind='linear', fill_value='extrapolate')

event_windows = []
gpt_post1500 = gpt_df[(gpt_df['year'] >= 1500) & (gpt_df['year'] <= 2000)].copy()
gpt_post1500 = gpt_post1500.drop_duplicates(subset='year')

print(f"GPTs included in event study (post-1500, N={len(gpt_post1500)}):")
for _, gpt in gpt_post1500.iterrows():
    print(f"  {gpt['name']} ({int(gpt['year'])})")

for _, gpt in gpt_post1500.iterrows():
    gpt_year = gpt['year']
    window = []
    for rel_year in range(-50, 51):
        abs_year = gpt_year + rel_year
        if abs_year >= maddison_df['year'].min() and abs_year <= maddison_df['year'].max():
            gdp = float(interp_func(abs_year))
            window.append({'gpt': gpt['name'], 'gpt_year': gpt_year,
                          'rel_year': rel_year, 'abs_year': abs_year, 'gdppc': gdp})
    if len(window) > 50:
        event_windows.append(pd.DataFrame(window))

event_df = pd.concat(event_windows, ignore_index=True)
event_df = event_df.sort_values(['gpt', 'rel_year'])
event_df['gdp_growth'] = event_df.groupby('gpt')['gdppc'].pct_change() * 100

print(f"\\nEvent windows constructed: {len(event_windows)} GPTs")
print(f"Total observations: {len(event_df)}")

print("\\n" + "=" * 70)
print("Individual GPT Growth Boosts:")
print("=" * 70)
boosts = []
for gpt_name in event_df['gpt'].unique():
    gpt_data = event_df[event_df['gpt'] == gpt_name].dropna(subset=['gdp_growth'])
    pre = gpt_data[gpt_data['rel_year'] < 0]['gdp_growth'].mean()
    post = gpt_data[gpt_data['rel_year'] > 0]['gdp_growth'].mean()
    boost = post - pre
    boosts.append({'gpt': gpt_name, 'pre_growth': pre, 'post_growth': post, 'boost': boost})
    print(f"  {gpt_name:45s}: pre={pre:.3f}%, post={post:.3f}%, boost={boost:+.3f} pp")

boosts_df = pd.DataFrame(boosts)
avg_boost = boosts_df['boost'].mean()
print(f"\\n  Average GPT growth boost: {avg_boost:+.3f} pp")
print(f"  Median GPT growth boost: {boosts_df['boost'].median():+.3f} pp")
print(f"  Std dev: {boosts_df['boost'].std():.3f} pp")

t_stat, p_val = stats.ttest_1samp(boosts_df['boost'], 0)
print(f"\\n  T-test (H0: boost=0): t={t_stat:.3f}, p={p_val:.4f}")
if p_val < 0.05:
    print(f"  -> Statistically significant at 5% level")
else:
    print(f"  -> Not significant at 5% level (small sample)")"""))

new_cells.append(code_cell("""# === Figure 7: Event Study Plot ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

maddison_df = pd.read_csv('data/raw/maddison_western_europe.csv')
gpt_df = pd.read_csv('data/processed/gpt_dataset.csv')

interp_func = interp1d(maddison_df['year'], maddison_df['gdppc_2011usd'],
                        kind='linear', fill_value='extrapolate')

event_windows = []
gpt_post1500 = gpt_df[(gpt_df['year'] >= 1500) & (gpt_df['year'] <= 2000)].copy()
gpt_post1500 = gpt_post1500.drop_duplicates(subset='year')

for _, gpt in gpt_post1500.iterrows():
    gpt_year = gpt['year']
    window = []
    for rel_year in range(-50, 51):
        abs_year = gpt_year + rel_year
        if abs_year >= maddison_df['year'].min() and abs_year <= maddison_df['year'].max():
            gdp = float(interp_func(abs_year))
            window.append({'gpt': gpt['name'], 'rel_year': rel_year, 'gdppc': gdp})
    if len(window) > 50:
        event_windows.append(pd.DataFrame(window))

event_df = pd.concat(event_windows, ignore_index=True)
event_df = event_df.sort_values(['gpt', 'rel_year'])
event_df['gdp_growth'] = event_df.groupby('gpt')['gdppc'].pct_change() * 100

avg_path = event_df.groupby('rel_year')['gdp_growth'].agg(['mean', 'sem']).reset_index()
avg_path['ci_lo'] = avg_path['mean'] - 1.96 * avg_path['sem']
avg_path['ci_hi'] = avg_path['mean'] + 1.96 * avg_path['sem']

pre_mean = avg_path[avg_path['rel_year'] < 0]['mean'].mean()
post_mean = avg_path[avg_path['rel_year'] > 0]['mean'].mean()
boost = post_mean - pre_mean

print(f"Average pre-GPT growth rate: {pre_mean:.3f}%")
print(f"Average post-GPT growth rate: {post_mean:.3f}%")
print(f"Average GPT growth boost: {boost:.3f} pp")

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle('Figure 7: GDP Growth Around GPT Arrivals -- Event Study',
             fontsize=14, fontweight='bold')

ax = axes[0]
ax.fill_between(avg_path['rel_year'], avg_path['ci_lo'], avg_path['ci_hi'],
                alpha=0.3, color='steelblue')
ax.plot(avg_path['rel_year'], avg_path['mean'], 'b-', lw=2.5)
ax.axvline(0, color='red', lw=2, ls='--', label='GPT Arrival')
ax.axhline(0, color='black', lw=0.5)
ax.axvspan(-50, 0, alpha=0.05, color='red')
ax.axvspan(0, 50, alpha=0.05, color='green')
ax.set_xlabel('Years Relative to GPT Arrival', fontsize=11)
ax.set_ylabel('GDP Growth Rate (%)', fontsize=11)
ax.set_title('Average GDP Growth Path Around GPT Arrivals')
ax.legend(fontsize=10)
ylim = ax.get_ylim()
ax.text(5, ylim[1]*0.85, f'Post-GPT boost:\\n+{boost:.2f} pp', fontsize=11,
        color='darkgreen',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

ax2 = axes[1]
colors2 = plt.cm.tab10(np.linspace(0, 1, len(gpt_post1500)))
for i, (_, gpt) in enumerate(gpt_post1500.iterrows()):
    gpt_data = event_df[event_df['gpt'] == gpt['name']]
    if len(gpt_data) > 20:
        path = gpt_data.groupby('rel_year')['gdp_growth'].mean()
        ax2.plot(path.index, path.values, alpha=0.5, lw=1.5, color=colors2[i],
                 label=gpt['name'][:25])
ax2.axvline(0, color='red', lw=2, ls='--')
ax2.axhline(0, color='black', lw=0.5)
ax2.set_xlabel('Years Relative to GPT Arrival', fontsize=11)
ax2.set_ylabel('GDP Growth Rate (%)', fontsize=11)
ax2.set_title('Individual GPT Growth Paths')
ax2.legend(fontsize=7, loc='upper left')

plt.tight_layout()
plt.savefig('figures/fig7_event_study.png', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig7_event_study.pdf', bbox_inches='tight')
plt.close()
print("Saved: figures/fig7_event_study.png/.pdf")"""))

new_cells.append(code_cell("""# === Figure 8: Schumpeterian S-Curve -- Diminishing Returns Within Omega ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

maddison_df = pd.read_csv('data/raw/maddison_western_europe.csv')

interp_func = interp1d(maddison_df['year'], maddison_df['gdppc_2011usd'],
                        kind='linear', fill_value='extrapolate')

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Figure 8: Schumpeterian Dynamics -- Diminishing Returns Within Each Omega',
             fontsize=13, fontweight='bold')

eras = [
    ('Steam Era', 1769, 1882, 'orangered'),
    ('Electricity Era', 1882, 1971, 'royalblue'),
    ('Digital Era', 1971, 2017, 'purple')
]

for ax, (era_name, t_start, t_end, color) in zip(axes, eras):
    years = np.arange(t_start, t_end + 1)
    gdp_vals = np.array([float(interp_func(y)) for y in years])
    growth_rates = np.diff(gdp_vals) / gdp_vals[:-1] * 100
    years_growth = years[1:]
    t_rel = years_growth - t_start

    window = min(10, len(growth_rates) // 3)
    if window > 1:
        growth_smooth = pd.Series(growth_rates).rolling(window, center=True).mean().values
    else:
        growth_smooth = growth_rates

    ax.scatter(t_rel, growth_rates, color=color, s=15, alpha=0.3, zorder=2)
    valid = ~np.isnan(growth_smooth)
    ax.plot(t_rel[valid], growth_smooth[valid], color=color, lw=2.5, alpha=0.8,
            zorder=3, label='10yr MA')

    valid_mask = ~np.isnan(growth_rates)
    if valid_mask.sum() > 3:
        z = np.polyfit(t_rel[valid_mask], growth_rates[valid_mask], 1)
        t_fit = np.linspace(0, t_end - t_start, 100)
        ax.plot(t_fit, np.poly1d(z)(t_fit), color='black', lw=1.5, ls='--', alpha=0.6,
                label=f'Trend: {z[0]:+.4f}/yr')

    ax.set_title(f'{era_name}\\n({t_start}-{t_end})', fontweight='bold', fontsize=12)
    ax.set_xlabel('Years since GPT arrival', fontsize=10)
    ax.set_ylabel('GDP growth rate (%)', fontsize=10)
    ax.axhline(0, color='black', lw=0.5)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('figures/fig8_schumpeterian_scurve.png', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig8_schumpeterian_scurve.pdf', bbox_inches='tight')
plt.close()
print("Saved: figures/fig8_schumpeterian_scurve.png/.pdf")"""))

# === SECTION 16 ===
new_cells.append(md_cell("""---

## 16. Does the GDP Boost Predict the Next Interval?

This tests the full TCDC causal chain:
**GPT_m -> GDP boost -> Technology stock T_t increases -> Interval_{m+1} shorter**

If the theory is correct, GPTs that produce larger GDP growth boosts should be followed
by shorter intervals to the next GPT, because the growth boost reflects a larger expansion
of the combinatorial frontier."""))

new_cells.append(code_cell("""# === Section 16A-B: Boost Variable + OLS Regressions ===
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy import stats
import statsmodels.api as sm

maddison_df = pd.read_csv('data/raw/maddison_western_europe.csv')
gpt_df = pd.read_csv('data/processed/gpt_dataset.csv')

interp_func = interp1d(maddison_df['year'], maddison_df['gdppc_2011usd'],
                        kind='linear', fill_value='extrapolate')

gpt_post1500 = gpt_df[(gpt_df['year'] >= 1500) & (gpt_df['year'] <= 2000)].copy()
gpt_post1500 = gpt_post1500.sort_values('year').reset_index(drop=True)

results = []
for idx in range(len(gpt_post1500)):
    gpt = gpt_post1500.iloc[idx]
    y = gpt['year']

    pre_years = np.arange(max(1, y - 30), y)
    pre_gdp = np.array([float(interp_func(yr)) for yr in pre_years])
    pre_growth = np.mean(np.diff(pre_gdp) / pre_gdp[:-1] * 100) if len(pre_gdp) > 1 else np.nan

    post_years = np.arange(y, min(2017, y + 30) + 1)
    post_gdp = np.array([float(interp_func(yr)) for yr in post_years])
    post_growth = np.mean(np.diff(post_gdp) / post_gdp[:-1] * 100) if len(post_gdp) > 1 else np.nan

    boost = post_growth - pre_growth if (pd.notna(pre_growth) and pd.notna(post_growth)) else np.nan
    gdp_level = float(interp_func(y))

    if idx < len(gpt_post1500) - 1:
        next_gpt = gpt_post1500.iloc[idx + 1]
        next_interval = next_gpt['year'] - y
    else:
        next_interval = np.nan

    results.append({
        'gpt': gpt['name'], 'year': y,
        'pre_growth': pre_growth, 'post_growth': post_growth,
        'boost': boost, 'gdp_level': gdp_level,
        'log_gdp_level': np.log(gdp_level),
        'next_interval': next_interval,
        'log_next_interval': np.log(next_interval) if pd.notna(next_interval) and next_interval > 0 else np.nan
    })

reg_df = pd.DataFrame(results).dropna(subset=['boost', 'log_next_interval'])
print("Regression Dataset:")
print(reg_df[['gpt', 'year', 'boost', 'gdp_level', 'next_interval']].to_string(index=False))

# Spec A
print("\\n" + "=" * 70)
print("OLS Regressions: log(next_interval) ~ GDP boost")
print("=" * 70)

X_a = sm.add_constant(reg_df['boost'])
y = reg_df['log_next_interval']
model_a = sm.OLS(y, X_a).fit()
print("\\n--- Spec A: log(interval_next) ~ boost ---")
print(model_a.summary())

# Spec B
X_b = sm.add_constant(reg_df[['boost', 'log_gdp_level']])
model_b = sm.OLS(y, X_b).fit()
print("\\n--- Spec B: log(interval_next) ~ boost + log(gdp_level) ---")
print(model_b.summary())

print("\\n" + "=" * 70)
print("INTERPRETATION:")
print("=" * 70)
beta_boost = model_a.params.iloc[1] if len(model_a.params) > 1 else model_a.params[0]
print(f"  Spec A: A 1 pp increase in GDP boost is associated with")
print(f"          a {beta_boost:.3f} change in log(next interval)")
if beta_boost < 0:
    print(f"          -> Larger GDP boosts predict SHORTER intervals to next GPT")
    print(f"          -> Consistent with TCDC theory!")
else:
    print(f"          -> Positive coefficient (may reflect increasing complexity of later GPTs)")
print(f"  Spec A R-squared: {model_a.rsquared:.3f}")
print(f"  Spec B R-squared: {model_b.rsquared:.3f}")"""))

new_cells.append(code_cell("""# === Figure 9: Scatter -- GDP Boost vs Next Interval ===
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import statsmodels.api as sm

maddison_df = pd.read_csv('data/raw/maddison_western_europe.csv')
gpt_df = pd.read_csv('data/processed/gpt_dataset.csv')

interp_func = interp1d(maddison_df['year'], maddison_df['gdppc_2011usd'],
                        kind='linear', fill_value='extrapolate')

gpt_post1500 = gpt_df[(gpt_df['year'] >= 1500) & (gpt_df['year'] <= 2000)].copy()
gpt_post1500 = gpt_post1500.sort_values('year').reset_index(drop=True)

results = []
for idx in range(len(gpt_post1500)):
    gpt = gpt_post1500.iloc[idx]
    y = gpt['year']
    pre_years = np.arange(max(1, y - 30), y)
    pre_gdp = np.array([float(interp_func(yr)) for yr in pre_years])
    pre_growth = np.mean(np.diff(pre_gdp) / pre_gdp[:-1] * 100) if len(pre_gdp) > 1 else np.nan
    post_years = np.arange(y, min(2017, y + 30) + 1)
    post_gdp = np.array([float(interp_func(yr)) for yr in post_years])
    post_growth = np.mean(np.diff(post_gdp) / post_gdp[:-1] * 100) if len(post_gdp) > 1 else np.nan
    boost = post_growth - pre_growth if (pd.notna(pre_growth) and pd.notna(post_growth)) else np.nan
    if idx < len(gpt_post1500) - 1:
        next_interval = gpt_post1500.iloc[idx + 1]['year'] - y
    else:
        next_interval = np.nan
    results.append({'gpt': gpt['name'], 'year': y, 'boost': boost,
                    'next_interval': next_interval,
                    'log_next_interval': np.log(next_interval) if pd.notna(next_interval) and next_interval > 0 else np.nan})

reg_df = pd.DataFrame(results).dropna(subset=['boost', 'log_next_interval'])

X = sm.add_constant(reg_df['boost'])
model = sm.OLS(reg_df['log_next_interval'], X).fit()
x_range = np.linspace(reg_df['boost'].min() - 0.05, reg_df['boost'].max() + 0.05, 100)
X_pred = sm.add_constant(x_range)
y_pred = model.predict(X_pred)
pred = model.get_prediction(X_pred)
ci = pred.conf_int(alpha=0.05)

fig, ax = plt.subplots(figsize=(12, 8))

ax.scatter(reg_df['boost'], reg_df['log_next_interval'], s=100, c='steelblue',
           edgecolors='navy', lw=1.5, zorder=5)

for _, row in reg_df.iterrows():
    name_short = row['gpt'].split('(')[0].strip()[:20]
    ax.annotate(f"{name_short}\\n({int(row['year'])})",
                (row['boost'], row['log_next_interval']),
                xytext=(8, 5), textcoords='offset points', fontsize=8,
                fontweight='bold', color='navy')

ax.plot(x_range, y_pred, 'r-', lw=2,
        label=f'OLS: beta={model.params.iloc[1]:.3f} (p={model.pvalues.iloc[1]:.3f})')
ax.fill_between(x_range, ci[:, 0], ci[:, 1], alpha=0.15, color='red')

ax.set_xlabel('GDP Growth Boost (pp): post-GPT minus pre-GPT', fontsize=12)
ax.set_ylabel('log(Interval to Next GPT)', fontsize=12)
ax.set_title('Figure 9: GDP Boost -> Next GPT Interval\\n'
             'Testing the TCDC Channel: GPT -> Growth -> Faster Innovation',
             fontsize=13, fontweight='bold')
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)

r2 = model.rsquared
ax.text(0.02, 0.98, f'R-squared = {r2:.3f}\\nN = {len(reg_df)}\\n'
        f'beta(boost) = {model.params.iloc[1]:.3f}',
        transform=ax.transAxes, fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
plt.savefig('figures/fig9_boost_vs_interval.png', dpi=300, bbox_inches='tight')
plt.savefig('figures/fig9_boost_vs_interval.pdf', bbox_inches='tight')
plt.close()
print("Saved: figures/fig9_boost_vs_interval.png/.pdf")"""))

# Append all new cells
nb['cells'].extend(new_cells)

with open('main_analysis.ipynb', 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Added {len(new_cells)} new cells to notebook (Sections 13-16)")
print(f"Total cells now: {len(nb['cells'])}")
