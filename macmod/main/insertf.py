
import pandas as pd
import json

sheets = list(map(str,range(1,174)))
tables1 = pd.read_excel('All Phase Pages - Update 2.xlsx',sheet_name=sheets,nrows=1)
tables2 = pd.read_excel('All Phase Pages - Update 2.xlsx',sheet_name=sheets,header=3,nrows=1)

df = pd.DataFrame()
for i in sheets:
    df1 = tables1[i].dropna(axis=1)
    df2 = tables2[i].dropna(axis=1)
    t12 = pd.concat([df1,df2],axis=1)
    df = pd.concat([df,t12],axis=0)

df['Phase Number'] = sheets
df['Carbon Load (%)'] = df['Carbon Load \n(%)']
df['Surface Area (m2/g)'] = df['Surface Area\n (m2/g)']
df['Pore Size (A)'] = df['Pore Size\n(Å)']

df.head(2)

df['Particle Size (µm)'].fillna(df['Particle Size\n (µm)'],inplace=True)
df['Carbon Load (%)'].fillna(df['Carbon Load \n(%)'],inplace=True)
df['Carbon Load (%)'].fillna(df['Carbon Load\n (%)'],inplace=True)
df['Surface Area (m2/g)'].fillna(df['Surface Area\n (m2/g)'],inplace=True)
df['LC-Mode'].fillna(df['LC Mode'],inplace=True)
df.drop(['Particle Size\n (µm)','Carbon Load \n(%)','Surface Area\n (m2/g)','Carbon Load\n (%)','LC Mode','Pore Size\n(Å)'],axis=1,inplace=True)

sheets_all2 = json.loads(df.to_json(orient='records'))

with open('test2.json','w') as data:
    json.dump(sheets_all2,data)