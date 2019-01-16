# -*- coding: utf-8 -*-
"""

@author: @ibrahimk07
"""

import pandas as pd
import numpy as np

def analyze_by_score(price_data,factor_score):
    pivotdata = price_data.pivot_table(values='adjusted_close',index='date',columns='symbol')

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
    t=len(returns.index)
    for k in range(t):
        farray.append(dailygroupreturns(k))
    
    #creating dataframes for each group, includes 1day,3day,5day returns columns
    group1returnby1 =[]
    for i in farray:
        group1returnby1.append(np.mean(i[0][0]))
    group1returnby3 =[]
    for i in farray:
        group1returnby3.append(np.mean(i[0][1]))
    group1returnby5 =[]
    for i in farray:
        group1returnby5.append(np.mean(i[0][2]))
        
    f = {'1dayreturn': group1returnby1  , '3dayreturn':group1returnby3 , '5dayreturn':group1returnby5 ,'index' :returns.index}
    finaldfg1 =pd.DataFrame(data=f)
    finaldfg1['group_title'] = 'Group1'
    
    group2returnby1 =[]
    for i in farray:
        group2returnby1.append(np.mean(i[1][0]))
    group2returnby3 =[]
    for i in farray:
        group2returnby3.append(np.mean(i[1][1]))
    group2returnby5 =[]
    for i in farray:
        group2returnby5.append(np.mean(i[1][2]))    
    f = {'1dayreturn': group2returnby1  , '3dayreturn':group2returnby3 , '5dayreturn':group2returnby5 ,'index' :returns.index}
    finaldfg2 =pd.DataFrame(data=f)
    finaldfg2['group_title'] = 'Group2'
   
    
    group3returnby1 =[]
    for i in farray:
        group3returnby1.append(np.mean(i[2][0]))
    group3returnby3 =[]
    for i in farray:
        group3returnby3.append(np.mean(i[2][1]))
    group3returnby5 =[]
    for i in farray:
        group3returnby5.append(np.mean(i[2][2]))  
    f = {'1dayreturn': group3returnby1  , '3dayreturn':group3returnby3 , '5dayreturn':group3returnby5 ,'index' :returns.index}
    finaldfg3 =pd.DataFrame(data=f)
    finaldfg3['group_title'] = 'Group3'
    
    
    group4returnby1 =[]
    for i in farray:
        group4returnby1.append(np.mean(i[3][0]))
    group4returnby3 =[]
    for i in farray:
        group4returnby3.append(np.mean(i[3][1]))
    group4returnby5 =[]
    for i in farray:
        group4returnby5.append(np.mean(i[3][2]))  
    f = {'1dayreturn': group4returnby1  , '3dayreturn':group4returnby3 , '5dayreturn':group4returnby5 ,'index' :returns.index}
    finaldfg4 =pd.DataFrame(data=f)
    finaldfg4['group_title'] = 'Group4'
  
    
    group5returnby1 =[]
    for i in farray:
        group5returnby1.append(np.mean(i[4][0]))
    group5returnby3 =[]
    for i in farray:
        group5returnby3.append(np.mean(i[4][1]))
    group5returnby5 =[]
    for i in farray:
        group5returnby5.append(np.mean(i[4][2]))    
    f = {'1dayreturn': group5returnby1  , '3dayreturn':group5returnby3 , '5dayreturn':group5returnby5 ,'index' :returns.index}
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
    
   
          