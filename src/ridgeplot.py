#!/usr/bin/python

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

stats = pd.read_hdf('../data/interim/NBA_stats_perGame_qualified_players_2000-2020.h5')

var = 'Age'
stats = stats.drop(stats.index[stats[var] == ''])
sns.set(style='white', rc={'axes.facecolor': (0, 0, 0, 0)})

# Initialize the FacetGrid object
pal = sns.cubehelix_palette(20, rot=-.25, light=.7)
g = sns.FacetGrid(stats, row='Season', row_order=stats.Season.unique()[::-1], hue='Season', aspect=15, height=.5, palette=pal)

# Draw the densities in a few steps
g.map(sns.kdeplot, var, clip_on=False, shade=True, alpha=1, lw=1.5, bw=.2)
g.map(sns.kdeplot, var, clip_on=False, color='w', lw=2, bw=.2)
g.map(plt.axhline, y=0, lw=2, clip_on=False)


# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight='bold', color=color,
            ha='left', va='center', transform=ax.transAxes)

g.map(label, var)

# g.set(xlim=(0,1))

# Set the subplots to overlap
g.fig.subplots_adjust(hspace=-.6)

# Remove axes details that don't play well with overlap
g.set_titles('')
g.set(yticks=[])
g.despine(bottom=True, left=True)

w,h = g.fig.get_figwidth(),g.fig.get_figheight()
g.fig.set_size_inches(w*1.4,h)

plt.savefig('../reports/figures/{}_rigdeplot.pdf'.format(var),bbox_inches='tight')
plt.close()
