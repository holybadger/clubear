import pandas as pd
import glob,os,time,IPython,random
import numpy as np

class manager(object):
    
    def demo(nfiles=9,ss=100000):
        '''demo is used to demonstrate typical examples about this class.'''
        
        greeting='''
To demonstrate the data manager method, we need to creat a folder
named 'demodata' in your current directory. In the directory, we should 
simulate a number of CSV datasets, named: CluBearDemoData.X.csv. For 
each CSV file there contains a number of variables and the 'logsales' 
one can be treated for response for regression.

**WARNING**: 'demodata' is a folder created for clubear demo only. As
a result, please do *NOT* place any personal file in this 'demodadta' 
folder for they are to be *DELETED* completely. Once your files are 
deleted, they can NEVER be recovered! By answering 'YES', any files
in the demodata folder (if exists) will be completely removed.
'''
        print(greeting);print('')
        userinput=input('Do you want to proceed [YES/No]:')
        if userinput != 'YES': return('manager.demo: demo data cannot be generated without user permission.')
        
        print('')
        if not os.path.exists('demodata'): os.makedirs('demodata')
        files=os.listdir('demodata')
        [os.remove('demodata/'+each) for each in files]

        heads=['gender','age','height','weight','region','company','brand','price','logsales']
        headline=','.join(heads)+'\n'
        ncov=len(heads);random.seed(0)
        for j in range(nfiles):
            filename='CluBearDemoData.'+str(j)+'.csv'
            gender=(np.random.uniform(0,1,ss)>0.5)
            gender=['Male'*each+'Female'*(not each) for each in gender]
            age=np.round(20+50*np.random.uniform(0,1,ss))
            height=np.round(150+50*np.random.uniform(0,1,ss))
            weight=np.round(100+100*np.random.uniform(0,1,ss),1)
            price=np.round(np.random.uniform(0,1,ss)*100,1)
            
            region=65+25*np.random.uniform(0,1,ss)
            region=[chr(int(each)) for each in region]
            
            com1=70+5*np.random.uniform(0,1,ss);
            com1=[chr(int(each)) for each in com1]
            com2=70+5*np.random.uniform(0,1,ss);
            com2=[chr(int(each)) for each in com2]
            company=[com1[each]+com2[each] for each in range(ss)]
            
            br1=75+10*np.random.uniform(0,1,ss)
            br1=[chr(int(each)) for each in br1]
            br2=75+10*np.random.uniform(0,1,ss)
            br2=[chr(int(each)) for each in br2]
            brand=[br1[each]+br2[each] for each in range(ss)]
            
            logsales=np.round(0.1*np.random.uniform(0,1,ss)+0.5*np.sqrt(age-20)-0.01*(price-50),2)
            
            output=pd.DataFrame(list(zip(gender,age,height,weight,region,company,brand,price,logsales)))
            output.columns=['gender','age','height','weight','region','company','brand','price','logsales']
            output.to_csv('demodata/'+filename,index=False,encoding='iso8859-1')
            
            IPython.display.clear_output(wait=True)
            print('Demo datasets generated [',j+1,'/',nfiles,'] :',filename)
        

        demostr='''
import clubear as cb
dm=cb.manager("demodata/") #initiate a dm object. 
dm.files #the file names without path.
dm.sizes #the file sizes in bytes.
dm.nr #the number of rows in each file.
dm.nc #the number of columns in each file.
dm.heads #the columns contained in each file.
dm.Heads #the columns contained in EVERY file.
dm.write() #do a test run for write
dm.write("clubear.csv") #do a full run with headers
'''
        IPython.display.clear_output(wait=True)
        print(demostr)
    
    
    def __init__(self,path):
        '''Initialization: check whether pm is a PUMP!.'''
        
        if not os.path.exists(path): print('manager: The directory dose not exists!'); return
        if not os.path.isdir(path): print('manager: This is not a director at all!'); return
        
        '''List all the CSV files under the director'''
        csvfiles = glob.glob(path+"*csv")
        csvfiles = sorted(csvfiles)
        isfiles=list(map(os.path.isfile,csvfiles))
        csvfiles = [csvfiles[each] for each in range(len(csvfiles)) if isfiles[each] == True] 
        if len(csvfiles)==0: print('manager: No CSV file found in the director!'); return
        
        '''short file names without path information'''
        shortfiles=[each[len(path):] for each in csvfiles]

        
        '''Count the number of lines in each file'''
        IPython.display.clear_output(wait=True)
        print('Total',len(csvfiles),'files found in path=',path)
        print('')
        nr = np.array([0 for each in csvfiles])
        for kk in range(len(csvfiles)):
            for line in open(csvfiles[kk],encoding='iso8859-1'):
                nr[kk]=nr[kk]+1
                if nr[kk]%1.0e+5==0: 
                    IPython.display.clear_output(wait=True)
                    print('Step (',kk+1,'/',len(csvfiles),')',('%.1f'%(nr[kk]/1.0e+6)),
                          '*10**6 lines found in',csvfiles[kk])
            nr[kk]=nr[kk]-1 #eliminate the header line
        mlines=np.round(nr/10**3,2)

        '''Open each CSV file and get its first row and assume they are headers'''
        openfiles=[open(each,encoding='iso8859-1') for each in csvfiles]
        heads = [each.readline().replace("\n","").replace('\"','').replace("\'","").split(',') for each in openfiles]
        
        '''eliminate the redundante spaces befor and after heads'''
        for k in range(len(heads)): heads[k]=list(map(str.strip,heads[k]))
            
        
        '''The number of columns in each CSV file'''
        nc = [len(each) for each in heads]
        
        '''Output at most 3 column headers for inspection. The number of characters'''
        '''contained in each header is constrainted to be no more than maxstrlen.'''
        maxstrlen=10
        maxm=np.min([np.min(nc),3])
        topheads=[each[0:maxm] for each in heads]
        for i in range(len(topheads)):
            for j in range(maxm):
                topheads[i][j]=topheads[i][j][:maxstrlen]
                
        '''Heads contains those columns commonly shared by EVERY file'''
        Heads = sorted(list(set.intersection(*map(set,heads))))
        '''some times we have empty header, they are eliminated'''
        Heads = [each for each in Heads if len(each)>0]
        
        '''each file sizes in G bytes'''
        filesizes=np.round(np.array(list(map(os.path.getsize,csvfiles)))/(2.0**20),3)
        
        '''output to screen for user inspection'''
        output=pd.DataFrame(list(zip(shortfiles,filesizes,mlines,nc,topheads)))
        output.columns=['files','sizes','nr','nc','heads']
        IPython.display.clear_output(wait=True)
        print('Total',len(csvfiles),'files found with ',len(Heads),'common columns and ',np.sum(nr),'lines.')
        print('')
        print(output)
        print('')
        print('* files: a list of csvfile names without path information')
        print('* sizes: the sizes of the files in M bytes')
        print('* nr: the number of rows contained in the file in 10**3' )
        print('* nc: the number of columns contained in the file')
        print('');
        print('The following',len(Heads),'Heads are found in EVERY file and can be used for output:')
        print('\n',Heads)
        print('')
        
        '''global variables shared by the class'''
        self.csvfiles = csvfiles
        self.totlines=np.sum(nr)        
        self.path = path
        
        self.nc = np.array(nc)
        self.nr = np.array(nr)
        self.heads = heads
        self.files = shortfiles
        self.sizes = list(map(os.path.getsize,csvfiles))
        self.Heads = Heads
    
    def write(self,pathfile='_CluBearTest_.csv'):
        '''write is used to merge CSV files **with** headers'''
        
        if len(self.Heads)==0: print('manager.write: No common column can be writen out!'); return
        
        '''Always remove the target file so that a new file can be created'''
        if os.path.exists(pathfile): os.remove(pathfile)
        
        '''If no filename given by user then do a test run write() get from each file '''
        '''its 1st observation (not header) line and then output them to a target file.'''
        if pathfile=='_CluBearTest_.csv':
            is_first_file = True       
            for each in self.csvfiles:
                reader=pd.read_csv(each,iterator=True,encoding='iso8859-1')
                chunk=reader.get_chunk(1)
                heads=chunk.columns
                heads=[each.strip() for each in heads]
                chunk.columns=heads
                chunk=chunk[self.Heads]
                chunk.to_csv(pathfile,mode='a',index=0,header=is_first_file)
                is_first_file=False

        '''If filename is given by user then do full run write() to output the file '''
        if pathfile!='_CluBearTest_.csv':
            
            if self.path+pathfile in self.csvfiles: print('manager.write: Cannot write to the source file.'); return
            
            '''This is the file for output'''
            f=open(pathfile,'w',encoding='iso8859-1')
            
            '''output the header line'''
            f.write(','.join(self.Heads)+'\n')
            
            '''oklines counts how many lines have been ouputed'''
            oklines=0
            
            '''output each CSV file'''
            start_time=time.time()
            for each in self.csvfiles:
                reader=open(each,encoding='iso8859-1')
                
                '''read in the line and this is the headerline'''
                firstline=next(reader).replace('\n','').replace('\"','').replace("\'","").split(',')
                firstline=[each.strip() for each in firstline]
                                
                '''find the column positions of those variables in Heads'''
                pos=[firstline.index(each) for each in self.Heads]
                maxpos=np.max(pos)
                
                '''remember oklines should add one'''
                oklines=oklines+1
                
                '''start to read and write data lines'''
                for line in reader:
                    
                    '''read in data line and keep those columns in Heads'''
                    newline=line.replace('\n','').replace('\"','').replace("\'","").split(',')
                    newline=[each.strip() for each in newline]
                    if len(newline)< maxpos+1: continue
                    data=[newline[each] for each in pos]
                    
                    '''output to the target file'''
                    data=','.join(data)+'\n'
                    f.write(data)
                    oklines=oklines+1
                    
                    '''for every 10**5 lines the progress % is updated'''
                    if (oklines%10**5==0)|(oklines==self.totlines):
                        end_time=time.time();elapsed_time=end_time-start_time
                        progress=100*oklines/self.totlines
                        IPython.display.clear_output(wait=True)
                        print('Time elapsed:',('%.1f'%elapsed_time),'second and',end=' ')
                        print("mission accomplished: ", ('%.1f'%progress),'% for a total of ',self.totlines,'lines.' )                    
            f.close()
            
        '''data target data is created. we sould read its top 10 lines and '''
        '''output them to the screen for user inspection'''
        df=pd.read_csv(pathfile,iterator=True,encoding='iso8859-1')
        df=df.get_chunk(10)
        if os.path.exists('_CluBearTest_.csv'): os.remove(pathfile)
        return df

    
    def dump(self,pathfile='_CluBearTest_.csv'):
        '''dump is used to merge CSV files **without** headers'''
        
        '''Always remove the target file so that a new file can be created'''
        if os.path.exists(pathfile): os.remove(pathfile)
        
        '''This is the target file for output'''
        f=open(pathfile,'w',encoding='iso8859-1')
        
        '''Since those files have no headers, we are going to create headers for'''
        '''them. How many headers are needed? This is determined by the minimum '''
        '''number of columns contained in each CSV file.'''
        min_num_columns=np.min(self.nc)
        column_names=",".join(["V"+str(i) for i in range(min_num_columns)])+'\n'
        f.write(column_names)
        
        '''If no user input is given then do a test run'''
        if pathfile=='_CluBearTest_.csv': [f.write(next(open(each,encoding='iso8859-1'))) for each in self.csvfiles]
            
        '''If user input is given, we then do a full size run'''
        if pathfile!='_CluBearTest_.csv':
            if self.path+pathfile in self.csvfiles: print('manager.write: Cannot write to the source file.'); return
            
            '''start to record how many lines outputed'''
            oklines=0
            
            '''do for each CSV file'''
            start_time=time.time()
            for each in self.csvfiles:
                
                '''do for each line'''
                for line in open(each,encoding='iso8859-1'):
                    
                    newline=line.replace('\n','').replace('\"','').replace("\'","").split(',')
                    if len(newline)< min_num_columns: continue
                    data=[newline[each] for each in list(range(min_num_columns))]
                    data=[each.strip() for each in data]
                    
                    '''output to the target file'''
                    data=','.join(data)+'\n'
                    
                    '''write to the target file'''
                    f.write(data)
                    
                    '''update how many lines outputed'''
                    oklines=oklines+1
                    
                    '''update the progress % for every 10**5 lines'''
                    if (oklines%10**5==0)|(oklines==self.totlines):
                        end_time=time.time();elapsed_time=end_time-start_time
                        progress=100*oklines/self.totlines
                        IPython.display.clear_output(wait=True)
                        print('Time elapsed:',('%.1f'%elapsed_time),'second and',end=' ')
                        print("mission accomplished: ", ('%.1f'%progress),'% for a total of ',self.totlines,'lines.' )                    
        f.close()

        '''data target data is created. we sould read its top 10 lines and '''
        '''output them to the screen for user inspection'''
        df=pd.read_csv(pathfile,iterator=True,encoding='iso8859-1')
        df=df.get_chunk(10)
        if os.path.exists('_CluBearTest_.csv'): os.remove(pathfile)
        return df
    
