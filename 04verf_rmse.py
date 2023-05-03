import pandas as pd
import numpy as np
import Config

dir_obs = 'C:\\Users\\YILIANGD\OneDrive - The University of Melbourne\\code\\02_6\\data\\'
def rmse(x, y):
    return np.sqrt(np.mean((x - y) ** 2))

rmse_old = np.zeros([50, 12])
rmse_new = np.zeros([50, 12])

barra_old = pd.read_csv(Config.dir_gauge_info + 'daily_barra_id.csv', index_col=0, parse_dates=True)
for i, id in enumerate(Config.ids_sorted_koppen):
    obs = pd.read_csv(dir_obs + '%06d' % id + '.csv', index_col=0, parse_dates=True)

    for j in range(12):
        obs_mm = obs[Config.period.month == j+1].values.flatten()
        old_mm = barra_old["%.1f" % id][Config.period.month == j+1].values.flatten()
        cali_mm = pd.read_csv(Config.dir_results + '%06d' % id + '_' + Config.months[j] + '_fitted.csv', usecols=[1]).values.flatten()
        rmse_old[i, j] = rmse(old_mm[obs_mm >=0], obs_mm[obs_mm >=0])
        rmse_new[i, j] = rmse(cali_mm[obs_mm >= 0], obs_mm[obs_mm >= 0])

pd.DataFrame(rmse_old, columns=np.arange(1, 13), index=Config.ids_sorted_koppen
             ).to_csv(Config.dir_results + 'verf_rmse_raw.csv')
pd.DataFrame(rmse_new, columns=np.arange(1, 13), index=Config.ids_sorted_koppen
             ).to_csv(Config.dir_results + 'verf_rmse_cali.csv')