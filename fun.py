import pandas as pd
import numpy as np
import os,glob

        
def ispump(pp):
    '''is pump is used to check whether the input is a pump'''

    try:
        df=pp.go()
    except:
        return False
    if not isinstance(df, pd.DataFrame): return False
    if df.shape[0]==0: return False
    
    return True

def demo():
    '''demo is used to demonstrate the whole clubear class'''
    
    mylist=['manager','pump','check','plot','model','tank']
    mylist=sorted(mylist)
    
    greeting='''
Welcome to CluBear!

This is a package designed for *Interactive* statistical analysis for massive 
datasets. The key idea used here is subsampling. The package is developed by 
CluBear Research Group. You are welcome to visit our official website at 
www.xiong99.com.cn. You are also welcome to follow us at our official WeChat 
account (ID: CluBear). Enjoy!
'''
    print(greeting)
    print('\n',mylist,'\n')
    
    return

def require():
    '''require is used to list all required package'''
    pyfiles = glob.glob("../src/*.py")
    
    reqlist=[]
    for each in pyfiles:
        f=open(each,encoding='iso8859-1')
        for eachline in f:
            if not 'import' in eachline: continue
            if 'from .' in eachline: continue
            if '"' in eachline: continue
            if "'" in eachline: continue
            eachlist=eachline.replace('\n','').split(' ')
            if eachlist[0] not in ['import','from']: continue
            eachlist=eachlist[1].split('.')[0]
            reqlist.append(eachlist)
        f.close()
    reqlist=','.join(reqlist)
    reqlist=reqlist.split(',')
    reqlist=set(reqlist)
    reqlist=sorted(list(reqlist))
    
    rmlist=['clubear','copy','glob','os','inspect','random','time','warnings','multiprocessing']
    [reqlist.remove(each) for each in rmlist]
    
    f=open('../pub/requirements.txt','w')
    for each in reqlist: f.write(each+'\n');
    f.close()
    return


