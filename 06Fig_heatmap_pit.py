import Config
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

gauge_info = pd.read_csv(Config.dir_gauge_info + 'test_50gauges_info.csv', index_col=0)
gauge_info1 = gauge_info.sort_values(by=['id'])
ks = pd.read_csv(Config.dir_results + 'verf_pit.csv')

raw_ks = ks.pivot(index='id', columns='month', values='raw')
raw_ks1 = raw_ks.sort_index()
raw_ks1['koppen'] = gauge_info1['koppen'].values
raw_ks2 = raw_ks1.sort_values(by=['koppen'])

cali_ks = ks.pivot(index='id', columns='month', values='cali_Q95')
cali_ks1 = cali_ks.sort_index()
cali_ks1['koppen'] = gauge_info1['koppen'].values
cali_ks2 = cali_ks1.sort_values(by=['koppen'])

#raw_ks2.max()
cm = 1/2.54
f = plt.figure(figsize=(14.5*cm, 11.5*cm))
gs = f.add_gridspec(60, 3)
ax1 = f.add_subplot(gs[:-7, 0])
ax2 = f.add_subplot(gs[:-7, 1])
ax3 = f.add_subplot(gs[:-7, 2])
cbar_ax1 = f.add_subplot(gs[-1, 0:2])
cbar_ax2 = f.add_subplot(gs[-1, 2])

sns.heatmap(raw_ks2.iloc[:, 0:12], vmin=0.5, vmax=1, cmap='Blues',
            cbar=True, cbar_kws=dict(label='Consistency index',
                                     ticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1],
                                     orientation='horizontal',
                                     extend='neither'),
            cbar_ax=cbar_ax1,
            xticklabels=Config.m_abr,
            yticklabels=Config.koppen,
            ax=ax1)

sns.heatmap(cali_ks2.iloc[:, 0:12].values, vmin=0.5, vmax=1, cmap='Blues',
            cbar=False,
            xticklabels=Config.m_abr,
            yticklabels=[],
            ax=ax2)

r = cali_ks2.iloc[:, 0:12]-raw_ks2.iloc[:, 0:12]
sns.heatmap(r, vmin=-0.5, vmax=0.5, center=0, cmap='RdBu',
           cbar=True, cbar_kws=dict(label='Consistency index difference',
                                    ticks=[-0.5, 0, 0.5],
                                    orientation='horizontal',
                                    extend='neither'),
           cbar_ax=cbar_ax2,
           xticklabels=Config.m_abr,
           yticklabels=np.arange(1,51),
           ax=ax3)

ax1.set_ylabel('Climate zone', fontsize=6)
ax1.set_xlabel('')
ax1.set_title('Raw reanalysis', fontsize=6)
ax1.set_yticklabels(ax1.get_yticklabels(), rotation = 'horizontal', fontsize=5)
ax1.set_xticklabels(ax1.get_xticklabels(), fontsize=6)
ax2.set_title('Post-processed reanalysis', fontsize=6)
ax2.set_xticklabels(ax2.get_xticklabels(), fontsize=6)
ax3.set_ylabel('Site', fontsize=6)
ax3.set_xlabel('')
ax3.set_xticklabels(ax3.get_xticklabels(), fontsize=6)
ax3.set_title('Post-processed reanalysis - Raw reanalysis', fontsize=6)
ax3.yaxis.tick_right()
ax3.yaxis.set_label_position("right")
#tick_params(axis='y', which='both', labelleft=False, labelright=True, ticksleft=False)
ax3.set_yticklabels(ax3.get_yticklabels(), rotation = 'horizontal', fontsize=5)
#ax3.set_xticklabels(ax3.get_xticklabels(), rotation = 'horizontal')
cbar_ax1.tick_params(labelsize=6)
cbar_ax1.set_xlabel(cbar_ax1.get_xlabel(), fontsize=6)
cbar_ax2.tick_params(labelsize=6)
cbar_ax2.set_xlabel(cbar_ax2.get_xlabel(), fontsize=6)
f.text(0.5, 0.12, 'Month',
       fontsize=6, rotation='horizontal',
       verticalalignment='center',horizontalalignment='center')

plt.subplots_adjust(top=0.95, bottom=0.08,
                    left=0.085, right=0.935,
                    hspace=0.2, wspace=0.25)
f.savefig(Config.dir_fig + '06Fig_heatmap_pit1.png')
