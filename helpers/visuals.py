import os 
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm, patches



def add_cabinet_periods(ax,cab_df=None,min_time=1946,max_time=1967,color='salmon',alpha=.5,linestyle='--',text=True):
  cbp = cab_df
  cbp['startdate'] = pd.to_datetime(cbp.startdate,format='%d-%M-%Y')
  cbp['enddate'] = pd.to_datetime(cbp.enddate,format='%d-%M-%Y')
  ymin,ymax = ax.get_ylim()

  for i,r in cbp.iterrows():
      sd = r['startdate']
      if sd.year >= min_time and sd.year <= max_time and r['cabinet'] != 'Van Agt III':
          ax.vlines(x=sd,ymin=ymin,ymax=ymax,color=color,linestyle=linestyle,alpha=alpha,linewidth=1)
          if text == True:
            ax.text(x=sd,y=ymin,s=r['cabinet'],rotation=90)

def add_year_lines(ax,month="01",min_time=1946,max_time=1967,color='gray',alpha=.5,linestyle='--'):
    ymin,ymax = ax.get_ylim()
    ax.vlines(x=[f'{y}-{month}-01' for y in range(min_time,max_time)], ymin=ymin, ymax=ymin, color=color, ls=linestyle,alpha=alpha, lw=.75)
