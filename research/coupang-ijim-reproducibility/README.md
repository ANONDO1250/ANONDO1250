# Coupang breach event-study reproducibility supplement

This supplement accompanies the manuscript **Control-Assurance Decoupling and Information-State Transitions in a Digital-Platform Breach: Evidence from Coupang**.

## Contents
- `Coupang_IJIM_Event_Calendar.csv`: focal event calendar and analytical status.
- `Coupang_IJIM_Reproducibility_Template.py`: rerun template for licensed daily market data.

## Data availability
The repository does **not** redistribute licensed CPNG, SPY, EWY, XRT, USD/KRW, or volume observations. To rerun the analysis, supply a CSV with the columns documented at the top of the Python file.

## Primary specification
- Estimation returns: 28 Oct 2024 through 14 Nov 2025, N=264 matched observations.
- Primary factor: SPY close-to-close arithmetic return.
- Primary event: E1, 1 Dec 2025, the first U.S. trading session after the 29 Nov scale revision.
- E2, S1, S2, E3 and E4 are exploratory.
- E4 is treated as a two-session 10-11 Jun 2026 window.

## Interpretation
The script reproduces the market-model workflow when the licensed input series are supplied. The manuscript treats market evidence as secondary to the regulator-led process reconstruction.

## License
Code and event definitions may be reused with attribution. Source documents and market data remain subject to their original terms.
