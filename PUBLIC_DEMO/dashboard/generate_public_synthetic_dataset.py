"""Generate an entirely synthetic, reproducible 96-month dashboard demonstration CSV.
No external market datasets or EEX observations are read.
Run from the ENERGY PROJECT root: python3 generate_public_synthetic_dataset.py
"""
from pathlib import Path
import calendar
import numpy as np
import pandas as pd

OUTPUT = Path('PUBLIC_DEMO/german_energy_market_eex_2018_2026.csv')
SEED = 20261112
rng = np.random.default_rng(SEED)
months = pd.date_range('2018-11-01', periods=96, freq='MS')
rows = []
for t, date in enumerate(months):
    month = date.month
    hours = calendar.monthrange(date.year, month)[1] * 24
    trading_days = int(np.busday_count(date.date(), (date + pd.offsets.MonthBegin(1)).date()))
    seasonal = np.cos(2 * np.pi * (month - 1) / 12)
    load = max(24e6, (39e6 + 3.2e6 * seasonal + 0.5e6 * np.sin(t / 8) + rng.normal(0, 1.4e6)) * hours / 730)
    wind = np.clip(12e6 + 3.3e6 * seasonal + 0.7e6 * np.sin(t / 9) + rng.normal(0, 1.9e6), 3e6, load * 0.56)
    solar = np.clip(5.5e6 - 3.1e6 * seasonal + 0.5e6 * np.sin(t / 11) + rng.normal(0, 0.65e6), 0.4e6, load * 0.30)
    renewables = wind + solar
    residual = max(load - renewables, 1e6)
    gas_gen = max(0.7e6, 4.6e6 + 0.10 * (residual - 20e6) + rng.normal(0, 0.65e6))
    lignite = max(0.6e6, 6.2e6 - 0.035e6 * t + rng.normal(0, 0.45e6))
    coal = max(0.4e6, 3.3e6 - 0.017e6 * t + rng.normal(0, 0.35e6))
    gas_price = max(1.5, 7.5 + 2.1 * np.sin(t / 7.5) + 0.018 * t + rng.normal(0, 1.0))
    carbon = max(5, 22 + 0.43 * t + 4.0 * np.sin(t / 13) + rng.normal(0, 3.0))
    residual_avg_mw = residual / hours
    electricity = max(-15, 19 + 3.1 * gas_price + 0.27 * carbon + 0.00035 * residual_avg_mw + rng.normal(0, 10))
    rows.append({
        'Month': date.strftime('%Y-%m-%d'),
        'Electricity_Price_EUR_MWh': electricity,
        'Wind_Generation_MWh': wind,
        'Solar_Generation_MWh': solar,
        'Gas_Generation_MWh': gas_gen,
        'Lignite_Generation_MWh': lignite,
        'Hard_Coal_Generation_MWh': coal,
        'Grid_Load_MWh': load,
        'Average_Residual_Load_MWh': residual_avg_mw,
        'Hours_Observed': hours,
        'Gas_Price_USD_MMBtu': gas_price,
        'Trading_Days': trading_days,
        'Wind_Solar_Generation_MWh': renewables,
        'Wind_Solar_to_Load_Pct': 100 * renewables / load,
        'Residual_Load_GWh': residual_avg_mw / 1000,
        'Carbon_Auction_Price_EUR_tCO2': carbon,
    })

df = pd.DataFrame(rows)
assert df.shape == (96, 16)
assert df.notna().all().all()
assert np.allclose(df['Wind_Solar_Generation_MWh'], df['Wind_Generation_MWh'] + df['Solar_Generation_MWh'])
assert np.allclose(df['Average_Residual_Load_MWh'] * df['Hours_Observed'], df['Grid_Load_MWh'] - df['Wind_Solar_Generation_MWh'])
assert (df['Wind_Solar_to_Load_Pct'].between(0, 100)).all()
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
if OUTPUT.exists():
    backup = OUTPUT.with_name('german_energy_market_eex_2018_2026_PREVIOUS_DO_NOT_PUBLISH.csv')
    if backup.exists():
        raise FileExistsError(f'Backup already exists: {backup}; move it before running again.')
    OUTPUT.rename(backup)
    print(f'Previous CSV backed up locally: {backup}')
df.to_csv(OUTPUT, index=False, float_format='%.8f')
print(f'Created {OUTPUT}: {len(df)} rows, {len(df.columns)} columns')
print(f'Synthetic generation only; random seed: {SEED}; no external datasets read.')
