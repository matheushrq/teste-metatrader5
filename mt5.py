import MetaTrader5 as mt5
from datetime import datetime
import pandas as pd

login, password = open('credentials.txt').read().splitlines()

mt5.initialize(login=int(login), password=password, server="mt5.xpi.com.br:443")

ativos = ['BBDC3', 'ITUB4', 'PETR4', 'VALE3']

dataframes = {}

for ativo in ativos:
    ticks = mt5.copy_ticks_range(
        ativo,
        datetime(2026, 6, 1),
        datetime(2026, 6, 3),
        mt5.COPY_TICKS_ALL
    )
    print(f"Fetched {len(ticks) if ticks is not None else 0} ticks for {ativo}")
    df_ticks = pd.DataFrame(ticks)
    df_ticks['time'] = pd.to_datetime(df_ticks['time'], unit='s')
    df_ticks['time_msc'] = pd.to_datetime(df_ticks['time_msc'], unit='ms')

    # armazenar DataFrame por ativo
    dataframes[ativo] = df_ticks


if __name__ == "__main__":
    # exemplo: mostrar as últimas 10 linhas filtradas por mês/ano para cada ativo
    for ativo, df in dataframes.items():
        print(f"--- {ativo} ---")
        print(df[(df['time'].dt.year == 2026) & (df['time'].dt.month == 6)].tail(10))

    # opcional: salvar cada DataFrame em CSV
    for ativo, df in dataframes.items():
        df.to_csv(f"{ativo}.csv", index=False)

'''
# candle
candle = mt5.copy_rates_range(
    'PETR4',
    mt5.TIMEFRAME_D1,
    datetime(2026, 6, 1),
    datetime(2026, 6, 3),
)

df_candle = pd.DataFrame(candle)

df_candle['time'] = pd.to_datetime(df_candle['time'], unit='s')

df_candle[(df_candle['time'].dt.year == 2026) & (df_candle['time'].dt.month == 6)].head()
'''