# SME Incentive Allocation Engine

A multi-objective optimization system for informal sector business incentive distribution, built on evolutionary algorithms and World Bank enterprise survey data.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://sme-incentive-engine.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python)](https://python.org)

## Problem

Informal SME incentive programmes in developing economies typically operate on first-come-first-served or single-objective prioritisation. Policymakers face an impossible choice:

- **Efficiency** — allocate to high-growth, high-revenue firms
- **Equity** — prioritise vulnerable micro-enterprises and female-owned businesses
- **Sustainability** — favour technology-ready, ESG-aligned firms

No current framework handles all three simultaneously under real budget constraints across thousands of heterogeneous businesses.

## Approach

Multi-Objective Evolutionary Algorithm (MOEA) with adaptive operators to generate Pareto-optimal allocation sets — giving policymakers a structured view of real trade-offs rather than forcing a single answer.

**Key components:**
- Constrained MOEA with adaptive crossover and mutation operators
- Three-objective scoring framework (Efficiency, Equity, Sustainability)
- Interactive Pareto trade-off explorer
- Policy scenario simulation

## Live Dashboard

[→ sme-incentive-engine.streamlit.app](https://sme-incentive-engine.streamlit.app/)

Explore business rankings, score distributions, and Pareto trade-offs interactively.

> Dashboard uses synthetic data generated to mirror the statistical properties of World Bank ISES 2023. Research conducted on licensed dataset (5,352 enterprises, 191 variables).

## Stack

| Layer | Tools |
|---|---|
| Optimisation | Python, NumPy, SciPy |
| Data | Pandas, World Bank ISES 2023 |
| Dashboard | Streamlit, Plotly |
| Deployment | Streamlit Community Cloud |

## Repository Structure

incentive-allocation-engine/

├── app/
│   └── dashboard.py        # Streamlit dashboard
├── data/
│   └── processed/
│       ├── scored_dataset.csv        # Synthetic demo data
│       └── generate_synthetic.py     # Synthetic data generator
├── requirements.txt
└── README.md


## Research Context

This project operationalises findings from PhD research in Artificial Intelligence at Universiti Kebangsaan Malaysia, focusing on multi-objective evolutionary algorithms with adaptive operators for informal business incentive distribution modelling.

## License

MIT
