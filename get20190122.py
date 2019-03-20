import pandas as pd
import datetime
scalar=154.0/158.0
df = pd.read_csv("Metro_train/record_2019-01-22.csv")
dfres=pd.read_csv("Metro_testA/testA_submit_2019-01-29.csv")
print(df.head(5))
print(df.columns)
print(df.index)
#gbdfandstatus=df.groupby(['stationID','status'])
print(df.shape)
#print(gbdfandstatus.size())
#print(gbdfandstatus.describe().reset_index().head(3))
#print(gbdfandstatus.count().reset_index().head(3))
#print(gbdfandstatus.get_group((25,0)).shape)
#print(len(gbdfandstatus))
#for eachdf in gbdfandstatus:
  #print(type(eachdf))
df['time'] = pd.to_datetime(df['time']) 
print(df[(df["stationID"]==55) & (df["status"]==0) &(df["time"]>datetime.datetime(2019, 1, 22, 20, 20) )\
 &(df["time"]<datetime.datetime(2019, 1, 22, 20, 30) )].count()['time'])
total=df.shape[0]
print('total:',total)
for indexstationID in range(81):
  print('stationID:',indexstationID)
  for indexstatus in range(2):
    for indexhour in range(24):
      for indexminite in range(0,60,10):
        basestartTime=datetime.datetime(2019,1,22,indexhour,indexminite)
        restime=str(basestartTime+datetime.timedelta(days=7))
        
        baseendTime=datetime.datetime(2019,1,22,indexhour,indexminite)+datetime.timedelta(minutes=10)
        #value=total-(((df["stationID"]==indexstationID) & (df["status"]==indexstatus) \
        #&(df["time"]>basestartTime )&(df["time"]<baseendTime )).value_counts()[False])
        value=df[(df["stationID"]==indexstationID) & (df["status"]==indexstatus) \
        &(df["time"]>basestartTime )&(df["time"]<baseendTime )].shape[0]
        #print(value)
        resvalue=float(value)*scalar
        if indexstatus==1:
          dfres.loc[((dfres.stationID == indexstationID) & (dfres.startTime==restime)),'inNums']=resvalue
          
        else:  
          dfres.loc[((dfres.stationID == indexstationID) & (dfres.startTime==restime)),'outNums']=resvalue
  #print(dfres)
print(dfres)
dfres.to_csv('Result1.csv',index=0)
print(str(datetime.datetime(2019, 1, 22, 20, 50)+datetime.timedelta(minutes=10)))
#154/158
now=datetime.datetime.now()
#print(type(df['time'][0]))
print(type(now-df['time'][0]))
#print(df['2019'].head[5])
