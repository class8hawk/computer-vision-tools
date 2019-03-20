import pandas as pd
from datetime import datetime
df = pd.read_csv("Metro_train/record_2019-01-22.csv")
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
print(df[(df["stationID"]==25) & (df["status"]==0) &(df["time"]>datetime(2019, 1, 22, 20, 20) )\
 &(df["time"]<datetime(2019, 1, 22, 20, 30) )])
 
print(str(datetime(2019, 1, 22, 20, 30)))

now=datetime.now()
#print(type(df['time'][0]))
print(type(now-df['time'][0]))
#print(df['2019'].head[5])
