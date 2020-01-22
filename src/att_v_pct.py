#!/usr/bin/python

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import seaborn as sns

from tools import *

sns.set(style='darkgrid',context='paper',palette='colorblind')

stats = pd.read_hdf('../data/interim/NBA_stats_perGame_qualified_players_2000-2020.h5')

stats = stats.drop(stats.index[stats['2PA'] == ''])
stats = stats.drop(stats.index[stats['3PA'] == ''])
stats = stats.drop(stats.index[stats['FGA'] == ''])
stats = stats.drop(stats.index[stats['2P%'] == ''])
stats = stats.drop(stats.index[stats['3P%'] == ''])
stats = stats.drop(stats.index[stats['FG%'] == ''])

stats['2PA'] = stats['2PA'].astype(float)
stats['3PA'] = stats['3PA'].astype(float)
stats['FGA'] = stats['FGA'].astype(float)
stats['2P%'] = stats['2P%'].astype(float)
stats['3P%'] = stats['3P%'].astype(float)
stats['FG%'] = stats['FG%'].astype(float)

stats = stats.drop(stats.index[stats['FGA'] < 100/82])
stats = stats.drop(stats.index[stats['2P%'] < 0.005])

fig,axes = plt.subplots(1,3)

sns.scatterplot(x='2PA',y='2P%',data=stats,ax=axes[0])
sns.scatterplot(x='3PA',y='3P%',data=stats,ax=axes[1])
sns.scatterplot(x='FGA',y='FG%',data=stats,ax=axes[2])

ix1 = np.logical_and(stats['2PA'] > 13.5, stats['2P%'] > 0.6)
ix2 = np.logical_or(np.logical_and(stats['3PA'] > 10.5, stats['3P%'] > 0.4),stats['3PA'] > 13)
ix3 = np.logical_and(stats['FGA'] > 20.0, stats['FG%'] > 0.5)

stype = ['2P','3P','FG']

offsets = [[(-20,100),(-130,60),(20,10),(-140,50),(-100,-150),(-20,-120)],
[(-100,-80),(-100,70),(-140,-50),(-150,50)],
[(-50,35),(-120,75),(-90,-140),(-10,10),(-10,-100)]]

for ix,ax,s,off in zip([ix1,ix2,ix3],axes,stype,offsets):
    instances = stats.drop(stats.index[~ix])
    for n,i in enumerate(instances.index):
        ax.annotate('{}, {}'.format(instances.Player[i],instances.Season[i]),
        xy=(instances['{}A'.format(s)][i],instances['{}%'.format(s)][i]),
        xytext=off[n],xycoords='data',textcoords='offset points',
        arrowprops=dict(arrowstyle='->',color='k'))

at = AnchoredText('@gordonchris19',loc=1,
            prop={'size':12,'color':'black'},frameon=True)
axes[2].add_artist(at)

at = AnchoredText('data via basketball-reference.com',loc=4,
            prop={'size':8,'color':'black'},frameon=True)
axes[2].add_artist(at)

axes[1].set_title('Attempts per game vs. Shooting Percentage',loc='center',fontweight='bold')

w,h = fig.get_figheight(),fig.get_figwidth()
fig.set_size_inches(w*4,h)

fig.savefig('../reports/figures/att_pct.png',bbox_inches='tight',dpi=350)
plt.close(fig)

fig1,ax1 = plt.subplots()
sns.scatterplot(x='2PA',y='2P%',data=stats,ax=ax1)

fig2,ax2 = plt.subplots()
sns.scatterplot(x='3PA',y='3P%',data=stats,ax=ax2)

fig3,ax3 = plt.subplots()
sns.scatterplot(x='FGA',y='FG%',data=stats,ax=ax3)

offsets = [[(-20,35),(-130,60),(25,10),(-130,30),(-100,-100),(-20,-70)],
[(-100,-80),(-100,70),(-140,-50),(-150,50)],
[(-20,35),(-120,75),(-30,-120),(-90,-100),(-10,-100)]]

for ix,ax,s,off in zip([ix1,ix2,ix3],[ax1,ax2,ax3],stype,offsets):
    instances = stats.drop(stats.index[~ix])
    for n,i in enumerate(instances.index):
        ax.annotate('{}, {}'.format(instances.Player[i],instances.Season[i]),
        xy=(instances['{}A'.format(s)][i],instances['{}%'.format(s)][i]),
        xytext=off[n],xycoords='data',textcoords='offset points',
        arrowprops=dict(arrowstyle='->',color='k'))

for ax in [ax1,ax2,ax3]:
    at1 = AnchoredText('@gordonchris19',loc=1,
                prop={'size':12,'color':'black'},frameon=True)
    at2 = AnchoredText('data via basketball-reference.com',loc=4,
                prop={'size':8,'color':'black'},frameon=True)
    ax.add_artist(at1)
    ax.add_artist(at2)
    ax.set_title('Attempts per game vs. Shooting Percentage',loc='center',fontweight='bold')

fig1.savefig('../reports/figures/att_pct_2P.png',bbox_inches='tight',dpi=350)
fig2.savefig('../reports/figures/att_pct_3P.png',bbox_inches='tight',dpi=350)
fig3.savefig('../reports/figures/att_pct_FG.png',bbox_inches='tight',dpi=350)
plt.close('all')
