import pandas as pd
import numpy as np

r = np.random.RandomState(13122210)

BASE = "out/home_data_2012-13"
RAND = "out/home_data_2012-13_rand_03"
U_MIN = - 0.3

### Creation of the dataset with additional random noise
base = pd.read_csv(BASE + ".csv", index_col='date', parse_dates=True)

val = base.values
D = val.shape[0] // 48
randomness = r.uniform(U_MIN, 0, size=val.shape)

mask = np.zeros((48, val.shape[1]))
mask[24: 36, :] = 1
mask = np.tile(mask, (D, 1))

randomness = randomness * mask
val += randomness

base.to_csv(RAND + ".csv")

### Creation of datasets with AvgPast forecasts
week = 48 * 7
datasets = [BASE, RAND]

for dat in datasets:
   
    df = pd.read_csv(dat + ".csv", index_col='date', parse_dates=True)

    offset = df.shape[0] % week

    for i, c in enumerate(df.columns):
        col = df.iloc[:, i]
        val = col[offset: ].values.reshape(-1, week)
        means = np.vstack([val[:j, :].mean(axis=0) for j in range(1, val.shape[0])])
        new_vals = np.zeros_like(col.values)
        new_vals[week + offset:] = means.flatten()
        df[c] = new_vals
    df.to_csv(dat + "_forcast.csv")



