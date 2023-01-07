import pandas as pd

#import datasets 1 and 2 to df1 and df2
df1 = pd.read_csv('dataset1.csv')
df2 = pd.read_csv('dataset2.csv')

#drop rows contain null values
#dataset1 has no null values so no need to drop null values on df1
df2.dropna(inplace = True)

#split location in dataset1 into multiple rows
location_lists = df1.location.str.split(', ')
df1.location = location_lists
df1 = df1.explode('location')

#change value of location "Ho Chi Minh" from dataset2 to "TP.HCM" to identical with dataset1
df2['location'] = df2['location'].replace(['Ho Chi Minh'], 'TP.HCM')

#save to csv
df1.to_csv('dataset1.csv',index = False)
df2.to_csv('dataset2.csv',index = False)