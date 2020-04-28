import pandas as pd
import urllib.request
df=pd.read_excel('利水湾1#开票室车牌.xlsx')
index=0
total=len(df['车牌'])
for i in range(len(df['车牌'])):
    if(i%20==0):
        print('total:',total,'  cur:',i)
    item=df['车牌'][i]
    if type(item) is str:
        if(len(item)==7 ):
            index+=1
            print(df['车牌.1'][i])
            try:
                urllib.request.urlretrieve(df['车牌.1'][i], filename=
            './利水湾1#开票室车牌/'+str(i)+'_'+item+'.jpg')
            except Exception as e:
                print("出现异常:"+str(e))


#print(len(df['车牌'])