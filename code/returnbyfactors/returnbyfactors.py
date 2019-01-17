# -*- coding: utf-8 -*-
"""

@author: @ibrahimk07
"""

import pandas as pd
import numpy as np

def calc_daybased_return(pivotdata):
    odayreturns = pivotdata.pct_change(periods=1) 
    odayreturns = odayreturns.shift(periods=-1)

    threedayreturns = pivotdata.pct_change(periods=3)
    threedayreturns = threedayreturns.shift(periods=-3)
    
    fivedayreturns = pivotdata.pct_change(periods=5)
    fivedayreturns = fivedayreturns.shift(periods=-5)

    return odayreturns,threedayreturns,fivedayreturns

def prepare_for_join(firstpivot,secondpivot,thirdpivot):
    dfodayreturns = firstpivot.unstack()
    dfodayreturns = dfodayreturns.reset_index(level=[0,1])
    dfodayreturns.columns = ['symbol', 'date', '1dayreturns']
    dfodayreturns = dfodayreturns.set_index(['date','symbol'])
        
    dfthreedayreturns = secondpivot.unstack()
    dfthreedayreturns = dfthreedayreturns.reset_index(level=[0,1])
    dfthreedayreturns.columns = ['symbol', 'date', '3dayreturns']
    dfthreedayreturns = dfthreedayreturns.set_index(['date','symbol'])
        
    dffivedayreturns = thirdpivot.unstack()
    dffivedayreturns = dffivedayreturns.reset_index(level=[0,1])
    dffivedayreturns.columns = ['symbol', 'date', '5dayreturns']
    dffivedayreturns = dffivedayreturns.set_index(['date','symbol'])
    
    return dfodayreturns,dfthreedayreturns,dffivedayreturns

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
    groupdf = grouplabeled.unstack()
    groupdf = groupdf.reset_index(level=[0,1])
    groupdf.columns = ['symbol', 'date', 'group number']  
    groupdf = groupdf.set_index(['date','symbol'])
    
    odayreturns,threedayreturns,fivedayreturns = calc_daybased_return(pivotdata) 
    
    first_df,third_df,fifth_df = prepare_for_join(odayreturns,threedayreturns,fivedayreturns) 
    
    totaldata= groupdf.join(first_df)
    totaldata= totaldata.join(third_df)
    totaldata = totaldata.join(fifth_df)

    onedayreturns = []
    threedayreturns = []
    fivedayreturns = []
    for i in range(1,6):
        onedayreturns.append(totaldata.loc[totaldata['group number'] == i*1.0]['1dayreturns'].mean())
        threedayreturns.append(totaldata.loc[totaldata['group number'] == i*1.0]['3dayreturns'].mean())
        fivedayreturns.append(totaldata.loc[totaldata['group number'] == i*1.0]['5dayreturns'].mean())
    
    fres = {'1dayreturn':onedayreturns  , '3dayreturn':threedayreturns , '5dayreturn':fivedayreturns, 'index':['Group1','Group2','Group3','Group4','Group5']}
    finalresult =pd.DataFrame(data=fres)
    finalpivot = finalresult.set_index('index')
  
    
    finalpivot['1dayreturn'] = finalpivot['1dayreturn'] - finalpivot['1dayreturn'].mean()
    finalpivot['3dayreturn'] = finalpivot['3dayreturn'] - finalpivot['3dayreturn'].mean()
    finalpivot['5dayreturn'] = finalpivot['5dayreturn'] - finalpivot['5dayreturn'].mean()
    
    return finalpivot