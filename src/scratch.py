#!/usr/bin/python

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredText
import seaborn as sns

from tools import *

sns.set(style='darkgrid',context='paper',palette='colorblind')

stats = pd.read_hdf('../data/interim/NBA_stats_perGame_qualified_players_2000-2020.h5')

var = ['PF','PTS']
df = clean(stats,var)
df = convert(df,var)
df = qualify(df)

fig,ax = plt.subplots()
sns.scatterplot(x=var[0],y=var[1],data=df,color=sns.color_palette('Reds')[5],ax=ax)

ix = np.logical_or(np.logical_and(df[var[0]] > 3.5, df[var[1]] > 25),np.logical_and(df[var[0]] >= 4, df[var[1]] > 20),)

instances = df.drop(df.index[~ix])
print(instances)

ax.set_xlim((0,5))
ax.set_ylim(bottom=0)

off = [(-50,55),(-180,55),(-60,-165),(-260,45),(-100,50)]

for n,i in enumerate(instances.index):
    ax.annotate('{}, {}'.format(instances.Player[i],instances.Season[i]),
    xy=(instances[var[0]][i],instances[var[1]][i]),
    xytext=off[n],xycoords='data',textcoords='offset points',
    arrowprops=dict(arrowstyle='->',color='k'))



at = AnchoredText('@gordonchris19\n\ndata via basketball-reference.com',loc=3,
            prop={'size':8,'color':'black'},frameon=True)
ax.add_artist(at)
ax.set_title('Who is mean, but scores a lot?',loc='left',fontweight='bold')

fig.savefig('../reports/figures/pf_vs_pts.png',bbox_inches='tight',dpi=350)
