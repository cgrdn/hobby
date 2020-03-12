#!/usr/bin/python

import numpy as np
import pylab as pl
import pandas as pd

from scipy.interpolate import interp1d

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.offsetbox import AnchoredText
import matplotlib.dates as mdates

import seaborn as sns
sns.set(style='ticks',palette='colorblind',context='paper')

corona_data = '../data/external/total-cases-covid-19-who.csv'
search_data = '../data/external/corona-search-trend.csv'

cf = pd.read_csv(corona_data)
cf = cf.drop(cf.index[cf.Entity != 'Worldwide'])
cf['Date'] = np.arange(pl.datestr2num('01-21-2020'), pl.datestr2num('03-12-2020'), 1)

sf = pd.read_csv(search_data, skiprows=1)
sf['Date'] = pl.datestr2num(sf.Day)
sf = sf.drop(sf.index[sf.Date < pl.datestr2num('01-21-2020')])
sf['Coronavirus: (Worldwide)'][sf['Coronavirus: (Worldwide)'] == '<1'] = 0
sf['Search Rate'] = sf['Coronavirus: (Worldwide)'].astype(int)

# gs = GridSpec(1,3)
# fig = plt.figure()
# axes = [fig.add_subplot(gs[:2]), fig.add_subplot(gs[2])]

fig,ax = plt.subplots()
axes = [ax]

axes[0].plot(cf.Date, cf['Total confirmed cases of COVID-19']/1000, '-o', linewidth=1.5, markersize=3, label='Total Cases')
axes[0].plot(np.nan, np.nan, '-s', linewidth=2, label='Search Rate', color=sns.color_palette('colorblind')[1])
axes[0].legend(loc=4, fontsize=8)
axes[0].set_ylabel('Global confirmed cases of COVID-19 (1000\'s)')

at = AnchoredText('@gordonchris19\n\nSources:\nhttps://ourworldindata.org/coronavirus\nhttps://trends.google.com',frameon=False,loc=2,prop={'size':8,'color':'black'})
axes[0].add_artist(at)

twax = axes[0].twinx()
twax.plot(sf.Date, sf['Search Rate'], '-s', linewidth=1.5, markersize=3, label='Search Rate', color=sns.color_palette('colorblind')[1])
twax.set_ylabel('Google Trends Search Index')

mihr = mdates.DayLocator(interval=2)
mhr  = mdates.WeekdayLocator(mdates.MO, interval=2)
fmt  = mdates.DateFormatter('%b-%d')
axes[0].xaxis.set_major_locator(mhr)
axes[0].xaxis.set_major_formatter(fmt)
axes[0].xaxis.set_minor_locator(mihr)

# f = interp1d(sf.Date, sf['Search Rate'],bounds_error=False)
# interp_search = f(cf.Date)

# axes[1].plot(cf['Total confirmed cases of COVID-19']/1000, interp_search, 'o')
# axes[1].set_xlabel(axes[0].get_ylabel())
# axes[1].set_ylabel('Google Trends Search Index')

w, h = fig.get_figwidth(), fig.get_figheight()
fig.set_size_inches(w, h/1.5)
fig.tight_layout()

fig.savefig('../reports/figures/covid_cases_and_search.png',bbox_inches='tight',dpi=350)
plt.close(fig)
