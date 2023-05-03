import sys
import datetime
import pandas as pd
import matplotlib as mpl


dir_map = 'C:\\Users\\YILIANGD\OneDrive - The University of Melbourne\\code\\02_4\\data\\Maps\\'
dir_gauge_info = 'C:\\Users\\YILIANGD\OneDrive - The University of Melbourne\\code\\02_4\\data\\'
#dir_obs_csv = 'E:\\Data\\Point_Obs\\csv\\'
dir_obs_csv = 'C:\\Users\\YILIANGD\OneDrive - The University of Melbourne\\code\\02_6\\data\\'
dir_fig = 'C:\\Users\\YILIANGD\OneDrive - The University of Melbourne\\code\\02_6\\figs\\'
dir_results = 'C:\\Users\\YILIANGD\OneDrive - The University of Melbourne\\code\\02_6\\results\\'
dir_stn_classified_clim = 'C:\\Users\\YILIANGD\OneDrive - The University of Melbourne\\code\\02_1\\ock\\data\\'
x_m = 3
x_o = 1
x_cl = 2
x_cr = 4
obs_p = 0.3
obs_uniform = 0.75
lmbda = 0.6

x_c = 0.01
y_c = 0.2
wetday_c = 0.2#1

n_rnd = 500
p_extreme = 1 - 1 / (1000 * 30)

missing_value = -9999

start = datetime.date(1990, 3, 1)
end = datetime.date(2019, 2, 28)

period = pd.date_range(
    start=start,
    end=end,
    freq='D')

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
m_abr = ['J', 'F','M', 'A', 'M','J', 'J', 'A', 'S', 'O', 'N', 'D']

ids = [1013, 5061, 6070, 7083, 7193,
      9257, 10045, 10878, 12176, 14015,
       15602, 29065, 10647, 11019, 12077,
       13017, 18104, 18166, 19042, 21106,
       24572, 25039, 26086, 27044, 29030,
       31062, 32040, 33076, 36143, 37104,
       38016, 39142, 40138, 41510, 44026,
       44070, 47016, 48034, 56055, 55006,
       62014, 66037, 77040, 73025, 84093,
      87043, 88023, 91262, 92019, 97054]

ids_sorted_koppen = [31062, 32040, 27044, 14015,
                     1013, 48034, 44070, 44026, 39142,
                     37104, 36143, 29030, 29065, 10045,
                     77040, 18166, 47016, 21106, 24572,
                     25039, 12077, 11019, 10878,
                     12176, 5061, 6070, 7083, 13017,
                     38016, 7193, 15602,
                     33076, 73025, 66037, 55006, 56055,
                     41510, 40138,
                     92019, 62014, 84093, 87043, 88023,
                     91262, 97054,
                     19042, 9257, 10647,
                     18104, 26086]

koppen = ['Am', 'Aw', 'Aw', 'Aw',
          'BSh', 'BSh', 'BSh', 'BSh', 'BSh',
          'BSh', 'BSh', 'BSh', 'BSh', 'BSh',
          'BSk', 'BSk', 'BSk', 'BSk', 'BSk',
          'BSk','BSk', 'BSk', 'BSk',
          'BWh', 'BWh', 'BWh', 'BWh', 'BWh',
          'BWh', 'BWh','BWh',
          'Cfa', 'Cfa', 'Cfa', 'Cfa', 'Cfa',
          'Cfa', 'Cfa',
          'Cfb', 'Cfb', 'Cfb', 'Cfb', 'Cfb',
          'Cfb', 'Cfb',
          'Csa', 'Csa', 'Csa',
          'Csb', 'Csb']



mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.weight"] = "normal"
mpl.rcParams["font.size"]= 8

mpl.rcParams['axes.titlesize'] = 8
mpl.rcParams['axes.linewidth'] = 0.8
mpl.rcParams['axes.labelsize'] = 8


mpl.rcParams['lines.linewidth'] = 0.8
mpl.rcParams['lines.markersize'] = 2.5


mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8

mpl.rcParams['legend.frameon'] = False
mpl.rcParams['legend.fontsize'] = 8


mpl.rcParams['savefig.dpi'] = 1000 #300

mpl.rcParams['boxplot.boxprops.linewidth'] = 0.8
mpl.rcParams['boxplot.capprops.linewidth'] = 0.8
mpl.rcParams['boxplot.whiskerprops.linewidth'] = 0.8
mpl.rcParams['boxplot.meanprops.linewidth'] = 0.8
mpl.rcParams['boxplot.medianprops.linewidth'] = 0.8
mpl.rcParams['boxplot.flierprops.linewidth'] = 0.8


#more detail how to
# derive barra data from NCI,
# screen observation,
# select test locations
# please refer to 02_4 file.
