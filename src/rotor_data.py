#!/usr/bin/python

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='ticks',palette='colorblind',context='paper')

datafile = '../data/external/200324 - GJ Data for Figures.csv'
df = pd.read_csv(datafile)

df['Op'] = df['Pre or Post Op?']
df['Par'] = df['Atrophy or Fatty Infiltration']

df = df.drop('Pre or Post Op?',axis=1)
df = df.drop('Atrophy or Fatty Infiltration',axis=1)

g = sns.FacetGrid(df, col='Par', row='Op', despine=False)

g = g.map(sns.barplot, 'Muscle', 'Percentage', 'Grade', palette='colorblind')

# nlabels = [l.get_text() for l in g.axes[1,1].get_xticklabels()]
for ax in g.axes.flatten():
    ax.set_ylim((0,100))
    ax.set_ylabel('')
    ax.set_xlabel('')
    # ax.set_xticklabels(nlabels)

for ax in g.axes[:,0]:
    labels = ax.get_yticklabels()
    nlabels = ['{}%'.format(l.get_text()) for l in labels]
    ax.set_yticklabels(nlabels)

g.axes[0,1].legend(title='Grade', bbox_to_anchor=(1.3,1.0), loc=1)

g.fig.savefig('../reports/figures/rotor_figure.pdf', bbox_inches='tight', dpi=350)
plt.close(g.fig)
