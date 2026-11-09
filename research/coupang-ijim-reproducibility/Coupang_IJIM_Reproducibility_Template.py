"""Reproducibility template for the Coupang event-study manuscript.

Expected CSV columns:
Date, CPNG, SPY, EWY, XRT, USDKRW, Volume
where price/index columns are adjusted closing levels and Volume is CPNG daily volume.
The script does not redistribute licensed market data.
"""
import math
import numpy as np
import pandas as pd

EST_START = pd.Timestamp('2024-10-28')
EST_END = pd.Timestamp('2025-11-14')
EVENTS = {
    'E1': ['2025-12-01'],
    'E2': ['2025-12-10'],
    'S1': ['2025-12-29'],
    'S2': ['2026-02-05'],
    'E3': ['2026-02-10'],
    'E4': ['2026-06-10', '2026-06-11'],
}

def load_data(path):
    df = pd.read_csv(path, parse_dates=['Date']).sort_values('Date').set_index('Date')
    for c in ['CPNG','SPY','EWY','XRT','USDKRW']:
        if c in df:
            df[c+'_r'] = df[c].pct_change()
    if 'Volume' in df:
        df['log_volume'] = np.log(df['Volume'])
    return df

def ols(y, X):
    X = np.column_stack([np.ones(len(X)), X])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    resid = y - X @ b
    return b, resid

def primary_model(df):
    est = df.loc[EST_START:EST_END, ['CPNG_r','SPY_r']].dropna()
    b, resid = ols(est['CPNG_r'].to_numpy(), est[['SPY_r']].to_numpy())
    alpha, beta = b
    sigma = math.sqrt(np.sum(resid**2)/(len(resid)-2))
    out = df[['CPNG_r','SPY_r']].dropna().copy()
    out['AR'] = out['CPNG_r'] - (alpha + beta*out['SPY_r'])
    return out, est, alpha, beta, sigma, resid

def empirical_tail(event_ar, residuals):
    return (np.sum(np.abs(residuals) >= abs(event_ar)) + 1) / (len(residuals) + 1)

def car_forecast_se(est_market_returns, event_market_returns, sigma):
    L = len(event_market_returns)
    N = len(est_market_returns)
    mean_m = est_market_returns.mean()
    sxx = np.sum((est_market_returns - mean_m)**2)
    term = L + L*L/N + ((event_market_returns.sum() - L*mean_m)**2)/sxx
    return sigma * math.sqrt(term)

def report(path):
    df = load_data(path)
    ar, est, alpha, beta, sigma, residuals = primary_model(df)
    print(f'N={len(est)} alpha={alpha:.8f} beta={beta:.4f} sigma={sigma:.6f}')
    for name, dates in EVENTS.items():
        idx = [pd.Timestamp(d) for d in dates]
        block = ar.loc[idx]
        if len(idx)==1:
            x = block['AR'].iloc[0]
            print(name, 'AR=', x, 't=', x/sigma, 'emp_tail=', empirical_tail(x,residuals))
        else:
            car = block['AR'].sum()
            se = car_forecast_se(est['SPY_r'].to_numpy(), block['SPY_r'].to_numpy(), sigma)
            print(name, 'CAR=', car, 'SE=', se, 't=', car/se,
                  'CI=', (car-1.96*se, car+1.96*se))

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('csv', help='Licensed daily market-data CSV; see module docstring.')
    args = ap.parse_args()
    report(args.csv)
