import Config
import pandas as pd
import numpy as np
from scipy.spatial import KDTree
import ecdf



daily_barra = pd.read_csv(Config.dir_gauge_info + 'daily_barra_id.csv', index_col=0, parse_dates=True)


def sel_ref(zz_90, xx, yy, z_90, x, y, n):
    assert len(zz_90) == len(xx)
    assert len(xx) == len(yy)
    assert len(z_90) == len(x)
    assert len(x) == len(y)
    T = KDTree(np.c_[xx, yy])
    ind = []
    for x_i, y_i, z_90_i in zip(x, y, z_90):
        dd, ii_xy = T.query([x_i, y_i], k=n+1)
        diff = abs(z_90_i - zz_90[ii_xy[1:]])
        i_ii_xy = np.argmin(diff)
        ind.append(ii_xy[i_ii_xy+1])
        #print(dd, diff, i_ii_xy+1)
    return np.array(ind, dtype=np.int32)

ref = []
for mm in range(1, 13):
    gauge = pd.read_csv(Config.dir_gauge_info + 'lonlat_obs_' + Config.months[mm - 1] + '.csv') # the id in gauge is sorted

    barra_mm_ref_all = daily_barra[daily_barra.index.month==mm].filter(["%.1f" % id_i for id_i in gauge.id])

    barra_mm_95 = []
    for i in range(barra_mm_ref_all.shape[1]):
        x = barra_mm_ref_all.values[:,i]
        barra_mm_95.append(ecdf.run(x[x>=0]).ppf(0.95)[0])

    barra_mm_95 = np.array(barra_mm_95)
    barra_mm_95_id = barra_mm_95[gauge.id.isin(Config.ids)]

    #check if the order of barra_mm_90 is consistent with the order of gauge.id
    #np.all([barra_mm_90.index[i] == str(gauge.id[i]) for i in range(len(gauge))])
    ii = sel_ref(barra_mm_95, gauge.longitude.values, gauge.latitude.values,
                 barra_mm_95_id, gauge.longitude[gauge.id.isin(Config.ids)].values, gauge.latitude[gauge.id.isin(Config.ids)].values, 3)


    for i, id in enumerate(np.sort(Config.ids)):
        print(Config.months[mm - 1], '%06d' % id)
        ref_id = gauge.id[ii[i]]
        ref.append([mm, id, int(ref_id)])


pd.DataFrame(ref, columns=['month', 'id', 'ref_id']).to_csv(Config.dir_results + 'reference95_id.csv', index=None)