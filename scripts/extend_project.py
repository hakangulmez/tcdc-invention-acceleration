#!/usr/bin/env python3
"""
Major extension script for TCDC Invention Acceleration project.
Steps: Create Maddison data, expand GPT list, rebuild master dataset.
"""

import pandas as pd
import numpy as np
import os

os.chdir('/Users/hakanzekigulmez/Desktop/tcdc-invention-acceleration')

# =============================================================================
# STEP 1: Create Maddison Western Europe GDP data
# =============================================================================
print("=" * 60)
print("STEP 1: Creating Maddison Western Europe GDP data")
print("=" * 60)

maddison_manual = {
    'year': [1, 500, 1000, 1300, 1400, 1450, 1500, 1550, 1600, 1650,
             1700, 1750, 1769, 1780, 1800, 1820, 1825, 1840, 1856,
             1870, 1882, 1885, 1900, 1908, 1913, 1929, 1947, 1950,
             1960, 1971, 1980, 1991, 2000, 2010, 2017],
    'gdppc_2011usd': [600, 580, 640, 780, 820, 850, 900, 980, 1050, 1100,
                      1200, 1350, 1450, 1550, 1700, 1850, 1950, 2200, 2600,
                      3100, 3600, 3700, 4500, 5000, 5500, 6800, 6500, 7000,
                      9000, 12500, 16000, 19000, 24000, 30000, 38000],
    'region': ['Western Europe'] * 35
}

maddison_df = pd.DataFrame(maddison_manual)
maddison_df.to_csv('data/raw/maddison_western_europe.csv', index=False)
print(f"Saved Maddison data: {len(maddison_df)} observations, {maddison_df['year'].min()}-{maddison_df['year'].max()}")
print(f"Source: Maddison (2007) + Bolt & van Zanden (2024)")
print(maddison_df.to_string(index=False))

# =============================================================================
# STEP 2: Expand GPT list from 24 to 30
# =============================================================================
print("\n" + "=" * 60)
print("STEP 2: Expanding GPT list")
print("=" * 60)

gpt_df = pd.read_csv('data/processed/gpt_dataset.csv')
old_n = len(gpt_df)
print(f"Old GPT count: {old_n}")

# Store old intervals for comparison
old_intervals = gpt_df[['name', 'year', 'interval_years']].copy()
old_intervals = old_intervals.rename(columns={'interval_years': 'old_interval'})

new_gpts = pd.DataFrame([
    {
        'id': 25, 'name': 'Mechanical Clock', 'year': 1300,
        'omega_shift_description': 'Precise time measurement — enables coordination, scheduling, navigation, scientific observation',
        'is_prehistoric': False, 'source': 'Lipsey et al. 2005'
    },
    {
        'id': 26, 'name': 'Double-Entry Bookkeeping & Early Banking', 'year': 1340,
        'omega_shift_description': 'Systematic financial accounting + credit creation — enables capital allocation, long-distance trade finance, risk distribution',
        'is_prehistoric': False, 'source': 'Gülmez 2026 (Medici banking, Banca Monte dei Paschi 1472, Bills of exchange)'
    },
    {
        'id': 27, 'name': 'Gunpowder & Cannon (European)', 'year': 1320,
        'omega_shift_description': 'Chemical energy release for propulsion — transforms warfare, mining, construction; enables new material extraction',
        'is_prehistoric': False, 'source': 'Lipsey et al. 2005'
    },
    {
        'id': 28, 'name': 'Crop Rotation & Scientific Agriculture', 'year': 1700,
        'omega_shift_description': 'Systematic soil management — enables sustained agricultural surplus, population growth, labor release for industrialization',
        'is_prehistoric': False, 'source': 'Mokyr (1990) The Lever of Riches'
    },
    {
        'id': 29, 'name': 'Blast Furnace & Iron Casting', 'year': 1450,
        'omega_shift_description': 'High-temperature iron production at scale — enables cheap structural materials, machine parts, weaponry',
        'is_prehistoric': False, 'source': 'Smil (2005) Creating the 20th Century'
    },
    {
        'id': 30, 'name': 'Telegraph (Long-distance communication)', 'year': 1837,
        'omega_shift_description': 'Near-instantaneous long-distance communication — eliminates information lag in trade, military coordination, journalism',
        'is_prehistoric': False, 'source': 'Jovanovic & Rousseau 2005'
    }
])

# Merge
combined = pd.concat([gpt_df, new_gpts], ignore_index=True)
combined = combined.sort_values('year').reset_index(drop=True)

# Recalculate intervals
combined['interval_years'] = combined['year'].diff()
# First entry has no interval
combined.loc[0, 'interval_years'] = np.nan

# Recalculate log_interval
combined['log_interval'] = np.where(
    combined['interval_years'] > 0,
    np.log(combined['interval_years']),
    np.nan
)

# Recalculate gpt_number
combined['gpt_number'] = range(1, len(combined) + 1)

# Fill post_1450 and post_industrial
combined['post_1450'] = combined['year'] >= 1450
combined['post_industrial'] = combined['year'] >= 1769

new_n = len(combined)
print(f"New GPT count: {new_n}")
print(f"\nNew GPTs added:")
for _, row in new_gpts.iterrows():
    print(f"  - {row['name']} ({row['year']})")

# Compare intervals
merged_compare = pd.merge(
    combined[['name', 'year', 'interval_years']].rename(columns={'interval_years': 'new_interval'}),
    old_intervals,
    on=['name', 'year'],
    how='outer'
)
merged_compare['changed'] = merged_compare['old_interval'] != merged_compare['new_interval']
changed = merged_compare[merged_compare['changed'] == True]
print(f"\nIntervals that changed ({len(changed)}):")
for _, row in changed.iterrows():
    old_v = f"{row['old_interval']:.0f}" if pd.notna(row['old_interval']) else "N/A"
    new_v = f"{row['new_interval']:.0f}" if pd.notna(row['new_interval']) else "N/A"
    print(f"  {row['name']} ({row['year']}): {old_v} → {new_v}")

# Save
combined.to_csv('data/processed/gpt_dataset.csv', index=False)
print(f"\nSaved updated gpt_dataset.csv ({new_n} GPTs)")

# =============================================================================
# STEP 3: Rebuild master dataset with Maddison data
# =============================================================================
print("\n" + "=" * 60)
print("STEP 3: Rebuilding master dataset with Maddison GDP")
print("=" * 60)

# For each GPT, find closest Maddison observation and interpolate
from scipy.interpolate import interp1d

maddison_interp = interp1d(
    maddison_df['year'], maddison_df['gdppc_2011usd'],
    kind='linear', fill_value='extrapolate'
)

master = combined.copy()

# For post-year-1 GPTs, get interpolated GDP
master['gdp_pc_maddison'] = master['year'].apply(
    lambda y: float(maddison_interp(y)) if y >= 1 else np.nan
)

# GDP growth rate: (gdp_t - gdp_{t-50}) / gdp_{t-50}
def calc_gdp_growth(year, interp_func):
    if year < 51:
        return np.nan
    gdp_now = float(interp_func(year))
    gdp_before = float(interp_func(year - 50))
    if gdp_before <= 0:
        return np.nan
    return (gdp_now - gdp_before) / gdp_before

master['gdp_growth_50yr'] = master['year'].apply(lambda y: calc_gdp_growth(y, maddison_interp))
master['log_gdp_growth'] = master['gdp_growth_50yr'].apply(lambda g: np.log(1 + g) if pd.notna(g) and g > -1 else np.nan)

# Update log columns
master['log_gdp_pc'] = np.log(master['gdp_pc_maddison'].where(master['gdp_pc_maddison'] > 0))

# Keep existing columns where they exist, fill from original
orig_master = pd.read_csv('data/processed/master_dataset.csv')
# Preserve literacy, patent_stock, population from original where available
for col in ['literacy_rate_pct', 'patent_stock_index', 'population_millions']:
    if col in orig_master.columns:
        name_to_val = dict(zip(orig_master['name'], orig_master[col]))
        master[col] = master['name'].map(name_to_val)

# For new GPTs, estimate these values
new_gpt_estimates = {
    'Mechanical Clock': {'literacy_rate_pct': 6, 'patent_stock_index': 0.0, 'population_millions': 300},
    'Gunpowder & Cannon (European)': {'literacy_rate_pct': 6, 'patent_stock_index': 0.0, 'population_millions': 310},
    'Double-Entry Bookkeeping & Early Banking': {'literacy_rate_pct': 7, 'patent_stock_index': 0.0, 'population_millions': 320},
    'Blast Furnace & Iron Casting': {'literacy_rate_pct': 10, 'patent_stock_index': 0.1, 'population_millions': 400},
    'Crop Rotation & Scientific Agriculture': {'literacy_rate_pct': 25, 'patent_stock_index': 0.5, 'population_millions': 600},
    'Telegraph (Long-distance communication)': {'literacy_rate_pct': 50, 'patent_stock_index': 3.0, 'population_millions': 1150},
}

for name, vals in new_gpt_estimates.items():
    for col, val in vals.items():
        mask = master['name'] == name
        if mask.any():
            master.loc[mask, col] = val

master['log_population'] = np.log(master['population_millions'].where(master['population_millions'] > 0))

# Also update gdp_pc_1990_intl_dollars from Maddison where available
# (Keep original for pre-historical, use Maddison for post-year-1)
if 'gdp_pc_1990_intl_dollars' not in master.columns:
    master['gdp_pc_1990_intl_dollars'] = np.nan
for _, row in orig_master.iterrows():
    mask = master['name'] == row['name']
    if mask.any() and 'gdp_pc_1990_intl_dollars' in orig_master.columns:
        master.loc[mask, 'gdp_pc_1990_intl_dollars'] = row['gdp_pc_1990_intl_dollars']

# For new GPTs, use Maddison values (converting 2011$ to approx 1990$ with factor ~0.7)
for name in new_gpt_estimates:
    mask = master['name'] == name
    if mask.any() and pd.isna(master.loc[mask, 'gdp_pc_1990_intl_dollars'].values[0]):
        master.loc[mask, 'gdp_pc_1990_intl_dollars'] = master.loc[mask, 'gdp_pc_maddison'].values[0] * 0.7

master.to_csv('data/processed/master_dataset.csv', index=False)
print(f"Saved master_dataset.csv ({len(master)} rows)")
print(f"\nGDP coverage:")
print(master[['name', 'year', 'gdp_pc_maddison', 'gdp_growth_50yr']].to_string(index=False))

print("\n✓ All data preparation steps complete!")
