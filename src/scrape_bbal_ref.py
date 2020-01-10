#!/usr/bin/python

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

accum_stats = []
for offset in range(0,9400,100):

    # per 100 pos.
    # url = 'https://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=per_poss&per_minute_base=36&per_poss_base=100&lg_id=NBA&is_playoffs=N&year_min=2001&year_max=&franch_id=&season_start=1&season_end=-1&age_min=0&age_max=99&shoot_hand=&height_min=0&height_max=99&birth_country_is=Y&birth_country=&birth_state=&college_id=&draft_year=&is_active=&debut_yr_nba_start=&debut_yr_nba_end=&is_hof=&is_as=&as_comp=gt&as_val=0&award=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&qual=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&c5stat=&c5comp=&c6mult=&c6stat=&order_by=season&order_by_asc=&offset={}'.format(offset)
    # per game
    url = 'https://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&match=single&type=per_game&per_minute_base=36&per_poss_base=100&lg_id=NBA&is_playoffs=N&year_min=2001&year_max=&franch_id=&season_start=1&season_end=-1&age_min=0&age_max=99&shoot_hand=&height_min=0&height_max=99&birth_country_is=Y&birth_country=&birth_state=&college_id=&draft_year=&is_active=&debut_yr_nba_start=&debut_yr_nba_end=&is_hof=&is_as=&as_comp=gt&as_val=0&award=&pos_is_g=Y&pos_is_gf=Y&pos_is_f=Y&pos_is_fg=Y&pos_is_fc=Y&pos_is_c=Y&pos_is_cf=Y&qual=&c1stat=&c1comp=&c1val=&c2stat=&c2comp=&c2val=&c3stat=&c3comp=&c3val=&c4stat=&c4comp=&c4val=&c5stat=&c5comp=&c6mult=&c6stat=&order_by=season&order_by_asc=&offset={}'.format(offset)
    html = urlopen(url)
    soup = BeautifulSoup(html)

    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)
    # use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
    # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]

    # avoid the first header row
    rows = soup.findAll('tr')[2:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')]
                for i in range(len(rows))]
    accum_stats = accum_stats + player_stats

stats = pd.DataFrame(accum_stats, columns = headers)
stats = stats.drop(stats.index[stats.Player.values == None])

# create an HDF store (note the *.h5 suffix)
store = pd.HDFStore('../data/interim/NBA_stats_perGame_qualified_players_2000-2020.h5')
store.put('stats', stats, data_columns=stats.columns)
store.close()
