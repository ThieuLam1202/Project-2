# 1. Import libraries
import pandas as pd

# 1.1. Libraries to handle preprocessing, including spliting to training and testing datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import hstack

from sklearn.model_selection import train_test_split

# 1.2. Libraries to handle training and evaluating
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

# 1.3. Library to save models to pickle files
import pickle

# 2. Load datasets from csv files
#Dataframes 1 and 2 are loaded from dataset1 and dataset2 csv files respectively
df1 = pd.read_csv('dataset1.csv')
df2 = pd.read_csv('dataset2.csv')

# 3. Data preparation
# 3.1. Data preprocessing
#Since algorithms can only process numeric datas, we need to convert the scraped data previously to vectors
#to begin, transform job name and company name to lower case
df1['name'].str.lower()
df1['company'].str.lower()
df2['name'].str.lower()
df2['company'].str.lower()

#remove everything in names' strings except for the words and numbers
df1['name'].replace('[^a-zA-Z0-9]', ' ', regex = True)
df1['company'].replace('[^a-zA-Z0-9]', ' ', regex = True)
df2['name'].replace('[^a-zA-Z0-9]', ' ', regex = True)
df2['company'].replace('[^a-zA-Z0-9]', ' ', regex = True)

#convert a collection of raw documents to a matrix of TF-IDF features with TfidfVectorizer
vectorizer = TfidfVectorizer()
X1_tfdif = vectorizer.fit_transform(df1['name'])
X2_tfdif = vectorizer.fit_transform(df2['name'])

#use DictVectorizer to do binary one-hot (aka one-of-K) coding
#it means one boolean-valued feature is constructed for each of the possible string values that the feature can take on.
encoder = DictVectorizer()
X1_categ = encoder.fit_transform(df1[['company','location']].to_dict('records'))
X2_categ = encoder.fit_transform(df2[['company','location']].to_dict('records'))

#stack together to get the input matrix to fit in models
X1 = hstack([X1_tfdif, X1_categ])
X2 = hstack([X2_tfdif, X2_categ])

#output value
y1 = df1['average_salary']
y2 = df2['average_salary']

# 3.2. Split the preprocessed data above to train and test sets
#split X1, y1, X2, and y2 to training and testing sets
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2)
X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.2)

#shapes of sets
print(X1_train.shape, X1_test.shape, y1_train.shape, y1_test.shape, X2_train.shape, X2_test.shape, y2_train.shape, y2_test.shape)

# 4. Train models
# 4.1. Train Decision Tree model with dataset1
#fit DecisionTreeRegressor on dataset1
decision_dataset1 = DecisionTreeRegressor(random_state=0)
decision_dataset1.fit(X1_train, y1_train)
y1_pred = decision_dataset1.predict(X1_test)

#save model to pickle file
pickle.dump(decision_dataset1, open('decision_dataset1.pkl','wb'))

#calculate mean squared error, squared = False to return RMSE
print('RMSE of Decision Tree on dataset1: ' + str(mean_squared_error(y1_test, y1_pred, squared=False)))

#calculate MAPE
print('MAPE of Decision Tree on dataset1: ' + str(mean_absolute_percentage_error(y1_test, y1_pred)))

# 4.2. Train Decision Tree model with dataset2
#fit DecisionTreeRegressor on dataset2
decision_dataset2 = DecisionTreeRegressor(random_state=0)
decision_dataset2.fit(X2_train, y2_train)
y2_pred = decision_dataset2.predict(X2_test)

#save model to pickle file
pickle.dump(decision_dataset2, open('decision_dataset2.pkl','wb'))

#calculate mean squared error, squared = False to return RMSE
print('RMSE of Decision Tree on dataset2: ' + str(mean_squared_error(y2_test, y2_pred, squared=False)))

#calculate MAPE
print('MAPE of Decision Tree on dataset2: ' + str(mean_absolute_percentage_error(y2_test, y2_pred)))

### 4.3. Train Random Forest model with dataset1
#fit RandomForestRegressor to dataset1
forest_dataset1 = RandomForestRegressor(random_state=0)
forest_dataset1.fit(X1_train, y1_train)
y1_pred = forest_dataset1.predict(X1_test)

#save model to pickle file
pickle.dump(forest_dataset1, open('forest_dataset1.pkl','wb'))

#calculate mean squared error, squared = False to return RMSE
print('RMSE of Random Forest on dataset1: ' + str(mean_squared_error(y1_test, y1_pred, squared=False)))

#calculate MAPE
print('MAPE of Random Forest on dataset1: ' + str(mean_absolute_percentage_error(y1_test, y1_pred)))

# 4.4. Train Random Forest model with dataset2
#fit RandomForestRegressor to dataset2
forest_dataset2 = RandomForestRegressor(random_state=0, max_depth=6)
forest_dataset2.fit(X2_train, y2_train)
y2_pred = forest_dataset2.predict(X2_test)

#save model to pickle file
pickle.dump(forest_dataset2, open('forest_dataset2.pkl','wb'))

#calculate mean squared error, squared = False to return RMSE
print('RMSE of Random Forest on dataset2: ' + str(mean_squared_error(y2_test, y2_pred, squared=False)))

#calculate MAPE
print('MAPE of Random Forest on dataset2: ' + str(mean_absolute_percentage_error(y2_test, y2_pred)))