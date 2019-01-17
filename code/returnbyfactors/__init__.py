# -*- coding: utf-8 -*-
"""

@author: @ibrahimk07
"""

import pandas as pd
import numpy as np

def analyze_by_score(pivotdata,factor_score):
           
    scores = factor_score
    grouplabeled = scores
   
    #grouping companies in pivot table every day based on their factor_scores
    count=0
    for i in grouplabeled.values:   
        k = pd.qcut(i,5,labels=[1,2,3,4,5],duplicates='drop')
        grouplabeled.values[count] = k
        count=count+1
    #calculating returns by given day range
    odayreturns = pivotdata.pct_change(periods=1) 
    odayreturns = odayreturns.shift(periods=-1)

    threedayreturns = pivotdata.pct_change(periods=3)
    threedayreturns = threedayreturns.shift(periods=-3)
    
    fivedayreturns = pivotdata.pct_change(periods=5)
    fivedayreturns = fivedayreturns.shift(periods=-5)
    
    #grouping companies titles into multidimensional-arrays
    #indexes is like [day][comp_indx]
    groups=[]
    #day,comp_indx
    def groupper(t): 
        subgroup=[]
        dailygroup=[]
        for i in grouplabeled.values:
            count=0
            for j in i:
                if j==t:
                    dailygroup.append(grouplabeled.columns[count])
                count=count+1
            subgroup.append(dailygroup)
            dailygroup=[]
        return subgroup
    for i in range(1,6):
        groups.append(groupper(i*1.0))
    #calculate every groups mean daily , by day-ranged returns
    groupsper1day=[]
    for g in range(5):
        gd1 =[]
        for i in range(len(odayreturns.index)):
            #for each group,calculate every day's mean and store in dg1
            gd1.append(odayreturns[groups[g][i]].iloc[i].mean())
        #calculate mean for all dates for each group
        meanofgroup = np.nanmean(gd1)
        groupsper1day.append(meanofgroup)
    
    groupsper3day=[]
    for g in range(5):
        gd3 =[]
        for i in range(len(threedayreturns.index)):
            gd3.append(threedayreturns[groups[g][i]].iloc[i].mean())
        meanofgroup = np.nanmean(gd3)
        groupsper3day.append(meanofgroup)
    
    groupsper5day=[]
    for g in range(5):
        gd5 =[]
        for i in range(len(fivedayreturns.index)):
            gd5.append(fivedayreturns[groups[g][i]].iloc[i].mean())
        meanofgroup = np.nanmean(gd5)
        groupsper5day.append(meanofgroup)    
    
    fres = {'1dayreturn':groupsper1day   , '3dayreturn':groupsper3day , '5dayreturn':groupsper5day, 'index':['Group1','Group2','Group3','Group4','Group5']}
    finalresult =pd.DataFrame(data=fres)
    finalpivot = finalresult.set_index('index')
  
    
    finalpivot['1dayreturn'] = finalpivot['1dayreturn'] - finalpivot['1dayreturn'].mean()
    finalpivot['3dayreturn'] = finalpivot['3dayreturn'] - finalpivot['3dayreturn'].mean()
    finalpivot['5dayreturn'] = finalpivot['5dayreturn'] - finalpivot['5dayreturn'].mean()
    
    return finalpivot