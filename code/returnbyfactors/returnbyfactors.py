# -*- coding: utf-8 -*-
"""

@author: @ibrahimk07
"""

import pandas as pd
import numpy as np

def calc_daybased_return(pivotdata,day,filter_by_zscore):

    dayrangedreturns = pivotdata.pct_change(periods=day).shift(periods=day*-1)
    
    if filter_by_zscore is not None:
        filtered_returns = abs(dayrangedreturns - dayrangedreturns.mean()) > filter_by_zscore * dayrangedreturns.std()
        dayrangedreturns[filtered_returns] = np.nan

    return dayrangedreturns

def prepare_for_join(pivot,day_range):
    
    df_dayranged_returns = pivot.unstack()
    df_dayranged_returns = df_dayranged_returns.reset_index(level=[0,1])
    df_dayranged_returns.columns = ['symbol', 'date', str(day_range)+'dayreturn']
    df_dayranged_returns = df_dayranged_returns.set_index(['date','symbol'])
    
    return df_dayranged_returns

def analyze_by_score(pivotdata,factor_score,nofgroups=5,return_range=[1,5,10],filter_by_zscore = None):
    
    grouplabeled = factor_score
   
    count=0
    for i in grouplabeled.values:   
        k = pd.qcut(i,nofgroups,labels=list(range(1,nofgroups+1)),duplicates='raise')
        grouplabeled.values[count] = k
        count=count+1
    
    groupdf = grouplabeled.unstack()
    groupdf = groupdf.reset_index(level=[0,1])
    groupdf.columns = ['symbol', 'date', 'group number']  
    groupdf = groupdf.set_index(['date','symbol'])
    
    day_ranged_returns_pivot = []
    for i in return_range:
        day_ranged_returns_pivot.append(calc_daybased_return(pivotdata,i,filter_by_zscore))

    day_ranged_returns_df = []
    for i in return_range:
        day_ranged_returns_df.append(prepare_for_join
                                     (day_ranged_returns_pivot[return_range.index(i)],i))
                            
    
    total_df = groupdf.join(day_ranged_returns_df)   
    
    day_ranged_returns_results = []                                    
    
    for j in return_range:
        for i in range(1,nofgroups+1):
            day_ranged_returns_results.append(total_df.loc
                                                          [total_df['group number'] == i*1.0]
                                                                                             [str(j)+'dayreturn'].mean())
            
    result_dict={}
    keys = [ str(j)+'dayreturn' for j in return_range ]
    
    for i in keys:
        result_dict.update({i:day_ranged_returns_results[:nofgroups]})
        day_ranged_returns_results = day_ranged_returns_results[nofgroups:]
    index_list= [ 'Group'+str(j) for j in range(1,nofgroups+1)] 
    result_dict.update({'index': index_list})
    factor_scores = pd.DataFrame(data=result_dict).set_index('index')
   
    for q in return_range:
        factor_scores[str(q)+'dayreturn'] = factor_scores[str(q)+'dayreturn'] * 15/q
        factor_scores[str(q)+'dayreturn'] = factor_scores[str(q)+'dayreturn'] - factor_scores[str(q)+'dayreturn'].mean()

    return factor_scores
