import numpy as np
import pandas as pd
import Est_trans
import Est_Powertrans

#for X[i,j], determine a regionally optimised value for power transformation

#use two c++ code Est_trans and Est_Powertrans.
#Est_trans include
    # power transformation and log-sinh transformation.
    # simplex numerical search method, to transformation parameters and normal distribution parameters.

#Est_Powertrans
    # given a certain power, estimate normal distribution parameters, using simplex.


n, m = data.shape
x_c = 0.1 # censoring threshold


#1. determine the serach range
# calculte optimal power for X[i,:] or X[:, j], i = 1,2,..n; j = 1, 2, ..m
loc_power = []
for i in range(n):
    N = Est_trans.fit_trans(data[i,:], x_c, 20, 30, False) #20 means rainfall, 30 means power transform.
    loc_power.append(N.lmbda)

min = np.min(np.array(loc_power))
max = np.max(np.array(loc_power))


#2. search regional power within the range.
lmbda = np.linspace(min, max, 10) #10 -- depend on the resolution you want
loglik = []
for lmbda_i in lmbda:
    loglik_s = 0
    for i in range(n):
        N = Est_Powertrans.fit_trans(data[i,:], x_c, lmbda_i, False)
        loglik_s = loglik_s + N.loglik_opt
    loglik.append(loglik_s)
loglik = np.array(loglik)
i = np.argmax(loglik)
reg_power = lmbda[i]


#3. the reg_power should be similar with median/mean of local powers.
reg_power = lmbda[i]
median =np.median(np.array(loc_power))
mean = np.mean(np.array(loc_power))
