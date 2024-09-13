import pandas as pd
# LOAD CSV
df = pd.read_csv('atp.csv'); 
#
df['Start_Time'] = pd.to_datetime(df['Start_Time'],format='%m/%d/%Y %H:%M:%S %p'); 
df['TargetVol_(mL)'] = pd.to_numeric(df['TargetVol_(mL)'])
# pre-filter for now...
df = df[df['TargetVol_(mL)'] > 3000]
print(df)
#
Baths = df['Bath'].unique(); print(Baths)
Chemicals = df['Chemical'].unique(); print(Chemicals)
Stations = df['Station'].unique(); print(Stations)
#
