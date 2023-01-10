import pandas as pd
import numpy as np

import gradio as gr
import pickle

from unidecode import unidecode

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import hstack, coo_matrix

#function to generate prediction
def create_predict(name, company, location, model_name):
    filename = model_name + '.pkl'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
        X = convert(name, company, location)
        #resize input to suitable with model size
        coo_matrix.resize(X, (1, model.n_features_in_))
        y = model.predict(X)
    return str(round(y[0], 3)) + " million VND"

#function to handle inputs (convert from text to vectors)
def convert(name, company, location):
    #first, convert Vietnamese characters to ascii characters
    name = unidecode(name)
    company = unidecode(company)
    location = unidecode(location)

    #insert to a dataframe for easier convertion
    data = [{'name': name, 'company': company, 'location': location}]
    df = pd.DataFrame(data)

    #convert text similarly when converting for preprocessing data
    df['name'].str.lower()
    df['company'].str.lower()

    df['name'].replace('[^a-zA-Z0-9]', ' ', regex = True)
    df['company'].replace('[^a-zA-Z0-9]', ' ', regex = True)

    #convert using TfidfVectorizer and DictVectorizer
    vectorizer = TfidfVectorizer()
    X_tfidf = vectorizer.fit_transform(df['name'])

    encoder = DictVectorizer()
    X_categ = encoder.fit_transform(df[['company','location']].to_dict('records'))

    X = hstack([X_tfidf, X_categ])
    return X

#create input components
name_input = gr.Textbox(label = 'Enter job name:')
company_input = gr.Textbox(label = 'Enter company name:')
location_input = gr.Textbox(label = 'Enter location of job:')
model_input = gr.Dropdown(["decision_dataset1", "decision_dataset2", "forest_dataset1", "forest_dataset2"], label = 'Select model to predict:')

#create output
output = gr.Textbox(label = "Salary prediction:")

app =  gr.Interface(fn = create_predict, inputs=[name_input, company_input, location_input, model_input], outputs=output)
app.launch()