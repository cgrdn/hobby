#!/usr/bin/python

import numpy as np
import pandas as pd
import pylab as pl

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.offsetbox import AnchoredText
import seaborn as sns

sns.set(palette='colorblind', context='paper', style='ticks')

breakdown = True
pct = True

fn = '../data/external/covid19.csv'
df = pd.read_csv(fn)

df.date = np.array(['{}-{}-{}'.format(datestr.split('-')[2], datestr.split('-')[1], datestr.split('-')[0]) for datestr in df.date])

df['date_number'] = pl.datestr2num(df.date)
prov = 'Nova Scotia'
ns = df.drop(df.index[df.prname != prov])
ix = np.where(ns.numconf == 0)[0]
if len(ix) > 0:
    ix = ix[-1] - 1
    ns = ns.drop(ns.index[:ix])

ix = np.where(~np.isnan(ns.numrecover))[0]
ns.numrecover.iloc[:ix[0]] = 0
for i in range(len(ix)-1):
    ns.numrecover.iloc[ix[i]:ix[i+1]] = ns.numrecover.iloc[ix[i]]

if breakdown:
    fig, ax = plt.subplots()

    ax.fill_between(ns.date_number, ns.numdeaths, color='k', label='Deaths')
    ax.fill_between(ns.date_number, ns.numrecover+ns.numdeaths, y2=ns.numdeaths, label='Recoveries')
    ax.fill_between(ns.date_number, ns.numconf, y2=ns.numdeaths+ns.numrecover, label='Active')

    ax.plot(ns.date_number, ns.numconf - ns.numdeaths - ns.numrecover, linewidth=2, label='Total Active', color='k')

    ax.legend(loc=2, ncol=4, bbox_to_anchor=(0.0, 1.1))

    ax.set_ylabel('# Cases')

    mihr = mdates.DayLocator()
    mhr  = mdates.WeekdayLocator(mdates.MO, interval=2)
    fmt  = mdates.DateFormatter('%d %b')

    ax.xaxis.set_major_locator(mhr)
    ax.xaxis.set_major_formatter(fmt)
    ax.xaxis.set_minor_locator(mihr)

    ax.set_xlim(ns.date_number.min(), ns.date_number.max())
    ax.set_ylim(bottom=0)

    w, h = fig.get_figwidth(), fig.get_figheight()
    # fig.set_size_inches(w*1.5, h)

    at = AnchoredText('data via https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html',loc=2,
                prop={'size':6,'color':'black'},frameon=True)
    ax.add_artist(at)

    fig.savefig('../reports/figures/{}_covid_breakdown.png'.format(prov), dpi=350, bbox_inches='tight')

    plt.close(fig)

if pct:

    pr = df.drop(df.index[df.prname == 'Canada'])
    pr = pr.drop(pr.index[pr.prname == 'Repatriated travellers'])
    pr = pr.drop(pr.index[pr.prname == 'Nunavut'])
    pr = pr.drop(pr.index[pr.prname == 'Yukon'])
    pr = pr.drop(pr.index[pr.prname == 'Northwest Territories'])

    pr['pct_positive'] = df.numconf/df.numtested*100
    pr['Province'] = df.prname
    pr = pr.drop(pr.index[np.isnan(pr.numtested)])

    for p in pr.Province.unique():
        N = pr['numtested'][pr.index[pr.Province == p]].max()
        pr['date_number'][pr.index[pr.Province == p]] = pr['date_number'][pr.index[pr.Province == p]] - np.nanmin(pr['date_number'][pr.index[pr.Province == p]])
        pr['Province'][pr.index[pr.Province == p]] = '{} ($N={:d}$)'.format(p, int(N))

    g = sns.lineplot('date_number', 'pct_positive', hue='Province', data=pr, palette='colorblind')

    ax = g.axes

    ax.axhline(0,color='k',zorder=-1)

    ax.set_xlim(left=0)
    ax.set_xlim(right=pr.date_number.max()+1)
    ax.set_ylim((-0.5,12.5))

    leg = g.axes.get_legend()
    # leg.set_frame_on(False)
    leg.set_bbox_to_anchor((1.02, 1.0))

    ax.set_ylabel('% Tested Positive')
    ax.set_xlabel('Days Since Initial Testing')

    at = AnchoredText('data via https://www.canada.ca/en/public-health/services/diseases/2019-novel-coronavirus-infection.html',loc=2,
                prop={'size':6,'color':'black'},frameon=True)
    ax.add_artist(at)

    plt.savefig('../reports/figures/positive_test_rate_by_province.png', dpi=350, bbox_inches='tight')
    plt.close()
