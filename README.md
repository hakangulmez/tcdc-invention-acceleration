# Inter-Invention Interval & Technology Stock

[![TCDC Framework](https://img.shields.io/badge/TCDC-G%C3%BClmez%202026-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

## Research Question
Does accumulated technology stock (T_{t-1}) accelerate the arrival of new General Purpose Technologies?

## Hypothesis
Inter-invention intervals between GPTs decline as technology stock accumulates — consistent with the feedback mechanism phi_6 * sum_m(omega_m * a_{m,t-1}) in the TCDC framework (Gulmez 2026).

## Key Theoretical Contribution
Each GPT represents a discrete shift in production function space (Omega_t -> Omega_{t+1}). Higher T_{t-1} enables faster Omega transitions — formally distinct from the Jones-Bloom (2020) per-researcher productivity channel.

## Data
| Source | Variable | Coverage |
|--------|----------|----------|
| Lipsey, Carlaw & Bekar (2005) | GPT list & dates | 10,000 BCE - 2017 |
| Bolt & van Zanden (2020) | GDP per capita | 1 CE - 2018 |
| Van Zanden et al. (2011) | Literacy rates | 1820 - 2010 |
| Bergeaud et al. (2016) | Patent stock index | 1820 - 2015 |
| McEvedy & Jones (1978) | Population | 400 BCE - 1975 |

## Main Finding
Technology stock (proxied by GDP per capita, literacy, and patent stock) significantly predicts shorter inter-invention intervals, independent of researcher count. This supports the TCDC feedback mechanism and is compatible with — but distinct from — the Jones-Bloom (2020) finding of declining per-researcher productivity.

## Repository Structure
```
tcdc-invention-acceleration/
├── data/
│   ├── raw/                    # Downloaded/manually entered raw data
│   └── processed/              # Cleaned, merged datasets
│       ├── gpt_dataset.csv
│       ├── master_dataset.csv
│       └── regression_table.csv
├── figures/                    # All output figures (PDF + PNG)
│   ├── fig1_timeline.*
│   ├── fig2_intervals.*
│   ├── fig3_stock_vs_interval.*
│   ├── fig4_omega_transitions.*
│   └── fig5_coefficient_plot.*
├── paper/                      # LaTeX paper draft
├── main_analysis.ipynb         # SINGLE MASTER NOTEBOOK
├── README.md
└── requirements.txt
```

## How to Run
```bash
git clone https://github.com/hakangulmez/tcdc-invention-acceleration
cd tcdc-invention-acceleration
pip install -r requirements.txt
jupyter notebook main_analysis.ipynb
```

## Related Work
- [Thesis: AI as a Task Shock](https://github.com/hakangulmez/thesis-ai-task-shock)
- [Replicability Explorer](https://github.com/hakangulmez/ai-task-replicability-explorer)
- TCDC Working Paper (forthcoming)

## Citation
Gulmez, H.Z. (2026). Does the Existing Technology Stock Accelerate New Invention? Evidence from 10,000 Years of General Purpose Technologies. Working Paper, TU Munich.
