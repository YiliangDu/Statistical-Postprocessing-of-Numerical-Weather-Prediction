import pandas as pd
import Config
import numpy as np
import eQM
from scipy.stats import norm
#when doing parametric quantile mapping, the raw reanalysis distribution is based on 0.2 power transformation.
def fQM(x, params_y):
    N = Est_Powertrans.fit_trans(x, Config.x_c, 0.2, False)
    N_xb = norm(loc=N.mean, scale=N.stdev)
    N_yb = norm(loc=params_y[0], scale=params_y[1])
    xb_c_cdf = N_xb.cdf(Config.x_c ** 0.2)
    yb = []
    for x_i in x:
        if x_i < 0:
            rnd = N_yb.rvs(size=Config.n_rnd)
            yb.append(rnd.mean())
        elif (x_i >= 0) & (x_i <= Config.x_c):
            rnd = []
            for ii in range(Config.n_rnd):
                cdf_c = xb_c_cdf * np.random.rand()
                rnd.append(N_yb.ppf(cdf_c))
            rnd = np.array(rnd)
            yb.append(rnd.mean())
        elif x_i > Config.x_c:
            cdf_xb = N_xb.cdf(x_i ** 0.2)
            if cdf_xb > Config.p_extreme:
                yb.append(N_yb.ppf(Config.p_extreme))
            else:
                yb.append(N_yb.ppf(cdf_xb))

    #back transform
    y = []
    for yb_i in yb:
        if yb_i > 0:
            y.append(yb_i ** (1/Config.lmbda))
        else:
            y.append(0)
    return np.array(y)

raw_barra = pd.read_csv(Config.dir_gauge_info + 'daily_barra_id.csv', index_col=0, parse_dates=True)
params1 = pd.read_csv(Config.dir_results + 'fit_eQM_params.csv')
## the results need to be updated/
for i, id_i in enumerate(Config.ids):
    raw = raw_barra["%.1f" % id_i]
    for mm in range(1, 13):
        raw_mm = raw[Config.period.month == mm].values.flatten()
        cali = fQM(raw_mm,
                       params1[['cali_mu', 'cali_sigma']][(params1.id==id_i) & (params1.month==mm)].values.flatten())
        pd.DataFrame({'cali': cali},
                     index=Config.period[Config.period.month == mm]).to_csv(
            Config.dir_results + '%06d' % id_i + '_' + Config.months[mm - 1] + '_fitted.csv', index_label='time')
