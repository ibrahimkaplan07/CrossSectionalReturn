# -*- coding: utf-8 -*-
"""

@author: @ibrahimk07
"""

import pandas as pd
import numpy as np

def analyze_by_score(pivotdata,factor_score):
   
    returns = pivotdata.pct_change()
           
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
    odayreturns
    # group every companies values by day
    # [group_no][1,3,5][comp_pos]
    def dailygroupreturns(day):  
        resultarray=[]
        diffreturns=[]
        returnsarray1=[]
        returnsarray3=[]
        returnsarray5=[]
        for k in groups:
            for i in k[day]:
                count=0
                #if a title of a company from group array is equal to 
                #odayreturns tables columns, add the value of this companies return into returnsarray'day_range'
                
                
                for j in odayreturns.columns:
                    if j==i:
                        returnsarray1.append(odayreturns.values[day][count])
                    count=count+1
                count=0
                for j in threedayreturns.columns:
                    if j==i:
                        returnsarray3.append(threedayreturns.values[day][count])
                    count=count+1
                count=0
                for j in fivedayreturns.columns:
                    if j==i:
                        returnsarray5.append(fivedayreturns.values[day][count])
                    count=count+1   
            diffreturns.append(returnsarray1)
            diffreturns.append(returnsarray3)
            diffreturns.append(returnsarray5)
            
            resultarray.append(diffreturns)
            
            returnsarray1 = []
            returnsarray3 = []
            returnsarray5 = []
            diffreturns = []
        return resultarray
    #final array which includes all data generated from parameters.
    #final array has indexes such as [day][group_ind][returnbyday][comp_index]
    farray = []
    #day,group_ind,[1,3,5],comp_ind
    #t=len(returns.index)
    t=len(groups[0])
    for k in range(t):
    	farray.append(dailygroupreturns(k))
    
    #creating dataframes for each group, includes 1day,3day,5day returns columns
  
   #[groupno][1_3_5]
    grouped_returns=[]
    for j in range(5):
        returnby1 = []
        returnby3 = []
        returnby5 = []
        for i in farray:
            returnby1.append(np.mean(i[j][0]))
            returnby3.append(np.mean(i[j][1]))
            returnby5.append(np.mean(i[j][2]))
        greturns = [returnby1,returnby3,returnby5]   
        grouped_returns.append(greturns)

    f = {'1dayreturn': grouped_returns[0][0] , '3dayreturn':grouped_returns[0][1] , '5dayreturn':grouped_returns[0][2] ,'index' :len(groups[0])}
    finaldfg1 =pd.DataFrame(data=f)
    finaldfg1['group_title'] = 'Group1'

    f = {'1dayreturn': grouped_returns[1][0] , '3dayreturn':grouped_returns[1][1] , '5dayreturn':grouped_returns[1][2] ,'index' :len(groups[1])}
    finaldfg2 =pd.DataFrame(data=f)
    finaldfg2['group_title'] = 'Group2'
  
    f = {'1dayreturn': grouped_returns[2][0] , '3dayreturn':grouped_returns[2][1] , '5dayreturn':grouped_returns[2][2] ,'index' :len(groups[2])}
    finaldfg3 =pd.DataFrame(data=f)
    finaldfg3['group_title'] = 'Group3'

    f = {'1dayreturn': grouped_returns[3][0] , '3dayreturn':grouped_returns[3][1] , '5dayreturn':grouped_returns[3][2] ,'index' :len(groups[3])}
    finaldfg4 =pd.DataFrame(data=f)
    finaldfg4['group_title'] = 'Group4'

    f = {'1dayreturn': grouped_returns[4][0] , '3dayreturn':grouped_returns[4][1] , '5dayreturn':grouped_returns[4][2] ,'index' :len(groups[4])}
    finaldfg5 =pd.DataFrame(data=f)
    finaldfg5['group_title'] = 'Group5'

    #merging all grouping into one dataframe
    frames = [finaldfg1,finaldfg2,finaldfg3,finaldfg4,finaldfg5]
    result = pd.concat(frames)
    resultreverseindexed = result.set_index(['group_title','index'])

    #creating day-ranged returns for final dataframe for each group
    count=0
    d1=[]
    while(count<5):
      groupno= 'Group'+ str(count+1)  
      d1.append(resultreverseindexed['1dayreturn'][groupno].mean())  
      count=count+1
    
    count=0
    d3=[]
    while(count<5):
      groupno= 'Group'+ str(count+1)  
      d3.append(resultreverseindexed['3dayreturn'][groupno].mean())  
      count=count+1
    
    count=0
    d5=[]
    while(count<5):
      groupno= 'Group'+ str(count+1)  
      d5.append(resultreverseindexed['5dayreturn'][groupno].mean())  
      count=count+1
    
    fres = {'1dayreturn':d1   , '3dayreturn':d3 , '5dayreturn':d5, 'index':['Group1','Group2','Group3','Group4','Group5']}
    finalresult =pd.DataFrame(data=fres)
    finalpivot = finalresult.set_index('index')
    
    finalpivot['1dayreturn'] = finalpivot['1dayreturn'] - finalpivot['1dayreturn'].mean()
    finalpivot['3dayreturn'] = finalpivot['3dayreturn'] - finalpivot['3dayreturn'].mean()
    finalpivot['5dayreturn'] = finalpivot['5dayreturn'] - finalpivot['5dayreturn'].mean()
    
    return finalpivot