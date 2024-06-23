from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import pandas as pd
import sklearn

app = Flask(__name__)

outliers_lcap = pickle.load(open('object-instances/outliers_lcap.pkl', 'rb'))
outliers_ucap = pickle.load(open('object-instances/outliers_ucap.pkl', 'rb'))
missing_imputation = pickle.load(open('object-instances/missing_imputation.pkl', 'rb'))
model = pickle.load(open('models/RandomForest2.pkl', 'rb'))
scaler = pickle.load(open('models/scaler1.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('home.html')
@app.route("/moreinfo", methods = ["GET", "POST"])
def moreinfo():
    return render_template('moreinfo.html')
@app.route("/index", methods = ["GET", "POST"])
def index():
    return render_template('index.html')
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        data_dict = {}

        if request.form['FTI']=='':
            data_dict['FTI'] = missing_imputation['FTI']
        else:
            data_dict['FTI'] = max(min(float(request.form['FTI']), outliers_ucap['FTI']), outliers_lcap['FTI'])

        if request.form['T3']=='':
            data_dict['T3'] = missing_imputation['T3']
        else:
            data_dict['T3'] = max(min(float(request.form['T3']), outliers_ucap['T3']), outliers_lcap['T3'])
        
        if request.form['T4U']=='':
            data_dict['T4U'] = missing_imputation['T4U']
        else:
            data_dict['T4U'] = max(min(float(request.form['T4U']), outliers_ucap['T4U']), outliers_lcap['T4U'])
        
        if request.form['TSH']=='':
            data_dict['TSH'] = missing_imputation['TSH']
        else:
            data_dict['TSH'] = max(min(float(request.form['TSH']), outliers_ucap['TSH']), outliers_lcap['TSH'])
        
        if request.form['TT4']=='':
            data_dict['TT4'] = missing_imputation['TT4']
        else:
            data_dict['TT4'] = max(min(float(request.form['TT4']), outliers_ucap['TT4']), outliers_lcap['TT4'])
        
        if request.form['age']=='':
            data_dict['age'] = missing_imputation['age']
        else:
            data_dict['age'] = max(min(int(request.form['age']), outliers_ucap['age']), outliers_lcap['age'])

        data_dict['goitre'] = float(request.form['goitre'])
        data_dict['hypopituitary'] = float(request.form['hypopituitary'])
        data_dict['lithium'] = float(request.form['lithium'])
        data_dict['pregnant'] = float(request.form['pregnant'])
        data_dict['psych'] = float(request.form['psych'])
        data_dict['sex'] = float(request.form['sex'])
        data_dict['sick'] = float(request.form['sick'])
        data_dict['thyroid_surgery'] = float(request.form['thyroid_surgery'])
        data_dict['tumor'] = float(request.form['tumor'])

        data_df = pd.DataFrame(columns = data_dict.keys(), index = [0])
        for var in data_dict.keys():
            data_df.loc[0,[var]] = data_dict[var]
        prediction = model.predict(data_df)[0]

        if prediction:
            return render_template('index.html', prediction_text="Thyroid Disease Detected")
        else:
            return render_template('index.html', prediction_text="Thyroid Disease not Detected")
    else:
        return render_template('home.html')

if __name__=="__main__":
    app.run(debug=True)
        
