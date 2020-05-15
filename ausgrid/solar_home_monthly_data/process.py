import pandas as pd
import numpy as np
import datetime

FILE="data/2012-2013 Solar home electricity data v2.csv"
OUT="out/home_data_2012-13.csv"

raw = pd.read_csv(FILE, skiprows=1)

raw = raw.drop(['Generator Capacity', 'Postcode', 'Row Quality'], axis=1)

tmp = pd.melt(raw, id_vars=['Customer', 'Consumption Category', 'date'])

tmp =  pd.pivot_table(tmp, index=['Customer', 'date', 'variable'],
                      columns='Consumption Category', values='value')

tmp['net'] = tmp['GC'] - tmp['GG'] + tmp['CL']
datetimes = [datetime.datetime.strptime(x[1] + x[2], '%d/%m/%Y%H:%M') for x in
             tmp.index]

tmp['datetime'] = datetimes

final = tmp.reset_index()[['Customer', 'datetime', 'net']].copy()
final.columns = ['customer', 'date', 'power']

final = final.dropna(axis=0)
final = final.sort_values(['customer', 'date'])

final = pd.pivot_table(
        index='date',
        columns='customer',
        values='power',
        data=final
        )
final = final.dropna(axis=1)
final.columns = np.arange(final.columns.shape[0])

final.to_csv(OUT)
