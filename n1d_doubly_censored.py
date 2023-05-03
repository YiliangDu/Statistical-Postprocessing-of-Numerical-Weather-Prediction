import pandas as pd
import numpy as np
from scipy.optimize import differential_evolution
import sys
import math
from scipy.stats import norm
from scipy.optimize import minimize

#mark == 4: right censored
#mark == 2: left censored
#mark == 1: observed
#mark == 3: missing

#p0 = mu/stdev
#p1 = log(stdv)

def map_p1(p, a, b):
    if a == -np.inf:
        if b == np.inf:
            m = p
        else:
            m = b - abs(p - b)
    else:
        if b == np.inf:
            m = a + abs(p - a)
        else:
            if p < a:
                m = 2 * a - p
            else:
                m = p
            m = m - 2 * (b - a) * int((m - a) / (2 * (b - a)))
            if m > b:
                m = 2 * b - m
    return m

def map_params(reparams, bounds):
    p0, p1 = reparams
    p01 = map_p1(p0, bounds[0][0], bounds[0][1])
    p11 = map_p1(p1, bounds[1][0], bounds[1][1])
    return p01, p11

def loglik(reparams, bounds, xs, xm):
    p0, p1 = map_params(reparams, bounds)
    std = math.exp(p1)
    mu = std * p0
    N = norm(loc=mu, scale=std)
    lmbda = 0.6
    p_extreme = 1 - 1 / (1000 * 30)
    log_prob = 0
    for i in range(len(xs)):
        if xm[i] == 1:#observed
            xb = xs[i] ** lmbda
            temp_xs = xs[i]
            log_prob = log_prob + N.logpdf(xb) + math.log(lmbda * (temp_xs ** (lmbda - 1)))
        elif xm[i] == 2:#left-censored
            xb = xs[i] ** lmbda
            log_prob = log_prob + N.logcdf(xb)
        elif xm[i] == 4:#right-censored
            xb = xs[i] ** lmbda
            if N.cdf(xb) >= p_extreme:
                new_cdf = p_extreme
            else:
                new_cdf = N.cdf(xb)
            log_prob = log_prob + math.log(1 - new_cdf)
        else:
            log_prob = log_prob + 0.0

    return -log_prob

def fit(xs, xm):
    bounds = [(-3, 1.5), (0.1, 2)]
    args = (bounds, xs, xm)
    res_p = differential_evolution(loglik, bounds, args=args)
    if res_p.success:
        params = res_p.x
        params1 = map_params(params, bounds)
        res2 = minimize(loglik, np.array(params1), args=args, method='nelder-mead')
        params2 = res2.x
        p03, p13 = map_params(params2, bounds)
        std = math.exp(p13)
        mu = std * p03
    else:
        print(res_p.message)
        mu = -9999
        std = -9999
    return mu, std
