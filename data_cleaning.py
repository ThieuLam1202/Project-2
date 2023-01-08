import pandas as pd

#import datasets 1 and 2 to df1 and df2
df1 = pd.read_csv('dataset1.csv')
df2 = pd.read_csv('dataset2.csv')

#check null values
#then drop rows contain null values
if df1.isna().any(axis=1).sum() > 0:
    print (str(df1.isna().any(axis=1).sum()) + 'rows contain null values in dataset1 were found, they will be dropped')
    df1.dropna(inplace = True)
    print ('rows contain null values has been dropped successfully')
if df2.isna().any(axis=1).sum() > 0:  
    print (str(df2.isna().any(axis=1).sum()) + 'rows contain null values in dataset2 were found, they will be dropped')
    df2.dropna(inplace = True)
    print ('rows contain null values has been dropped successfully')

#check duplicated values
#then drop duplicated values (only the first value will be kept)
if df1.duplicated().sum():
    print (str(df1.duplicated().sum()) + 'rows contain duplicated values in dataset1 were found, they will be dropped')
    df1 = df1.drop_duplicates(keep='first')
    print ('rows contain duplicated values has been dropped successfully')
if df2.duplicated().sum():
    print (str(df2.duplicated().sum()) + 'rows contain duplicated values in dataset2 were found, they will be dropped')
    df2 = df2.drop_duplicates(keep='first')
    print ('rows contain duplicated values has been dropped successfully')

#split location in dataset1 into multiple rows
location_lists = df1.location.str.split(', ')
df1.location = location_lists
df1 = df1.explode('location')

#change value of location "Ho Chi Minh" from dataset2 to "TP.HCM" to identical with dataset1
df2['location'] = df2['location'].replace(['Ho Chi Minh'], 'TP.HCM')

#save to csv
df1.to_csv('dataset1.csv',index = False)
df2.to_csv('dataset2.csv',index = False)