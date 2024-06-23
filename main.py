from os import O_TRUNC
from flask import Flask,render_template,request
import requests
import pickle
import numpy as np


app = Flask(__name__)

with open("models/RandomForest2.pkl","rb") as model_file:
    model=pickle.load(model_file)

@app.route('/')
def index():
   return render_template('home.html')

@app.route("/moreinfo", methods = ["GET", "POST"])
def moreinfo():
    return render_template('moreinfo.html')

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    return render_template('predict.html')

@app.route("/predictresult", methods = ["GET", "POST"])
def predictresult():
    if request.method == "POST":
        sex= request.form.get('sex')
        age=float(request.form.get('age'))
        TSH= float(request.form.get('TSH'))
        T3= float(request.form.get('T3'))
        TT4= float(request.form.get('TT4'))
        T4U= float(request.form.get('T4U'))
        FTI=float(request.form.get('FTI'))
        goitre= request.form.get('goitre')
        hypopituitary = request.form.get('hypopituitary')
        pregnant= request.form.get('pregnant')
        sick= request.form.get('sick')
        thyroid_surgery=request.form.get('thyroid_surgery')
        tumor=request.form.get('tumor')
        psych = request.form.get('psych')
        lithium= request.form.get('lithium')


        #Sex
        if Sex=="Male":
            Sex=1
        else:
            Sex=0
        #On_thyroxine
        # if On_thyroxine=="Yes":
        #     On_thyroxine=1
        # else:
        #     On_thyroxine=0

        #On_antithyroid_medication
        # if On_antithyroid_medication=="Yes":
        #     On_antithyroid_medication=1
        # else:
        #     On_antithyroid_medication=0
        
        #Goitre
        if Goitre=="Yes":
            Goitre=1
        else:
            Goitre=0

        #Hypopituitary
        if Hypopituitary=="Yes":
            Hypopituitary=1
        else:
            Hypopituitary=0
        #pregnant
        if Pregnant=="Yes":
            Pregnant=1
        else:
            Pregnant=0

        #Psychological_symptoms
        if Psychological_symptoms=="Yes":
            Psychological_symptoms=1
        else:
            Psychological_symptoms=0

        #T3_measured
        if Lithium=="Yes":
            Lithium=1
        else:
            Lithium=0



        arr=np.array([[Age,Sex,Level_thyroid_stimulating_hormone,Total_thyroxine_TT4,Free_thyroxine_index,
        On_thyroxine,On_antithyroid_medication,Goitre,Hypopituitary,Psychological_symptoms,T3_measured]])
        pred=model.predict(arr)


        # if pred==0:
        #     res_Val="Compensated Hypothyroid"
        # elif pred==1:
        #     res_Val="No Thyroid"
        # elif pred==2:
        #     res_Val='Primary Hypothyroid'
        # elif pred==3:
        #     res_Val='Secondary Hypothyroid'
        data_df = pd.DataFrame(columns = data_dict.keys(), index = [0])
        for var in data_dict.keys():
            data_df.loc[0,[var]] = data_dict[var]
        prediction = model.predict(data_df)[0]

        if prediction:
            res_val="Thyroid Disease Detected"
        else:
            res_val="Thyroid Disease not Detected"
  
        
        Output=f"Patient has {res_Val}"
        return render_template('predictresult.html',output=Output)

    else:
        return render_template('home.html')
    # return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=False)
