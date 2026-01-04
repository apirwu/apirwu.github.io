from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import random as r
import csv
import ast
import os




app = Flask(__name__)
#randomized marks
def calculation():
    return {
        "Cmath": r.randint(30,75),
        "Omath": r.randint(30,75),
        "Science": r.randint(30,75),
        "Nepali": r.randint(30,75),
        "English": r.randint(30,75),
        "Computer": r.randint(17,50),
        "Social": r.randint(30,75)}
#main window
@app.route('/')
def main():
    new_marks=calculation()
    return render_template('home.html', marks=new_marks)
#time for the save shit
@app.route('/save', methods=['POST'])
def save():
    choice = request.form.get('choice')
    raw = request.form.get('all_marks')
    if choice == "Science":
        choice=1
    else:
        choice=0


    marks_dih = ast.literal_eval(raw)
    marks_dih['Result'] = choice
    
    file= 'data.csv'
    exist = os.path.isfile(file)
    with open(file,'a' ,newline="") as f:
        headers= list(marks_dih.keys())
        writer = csv.DictWriter(f , fieldnames=headers)
        if not exist:
            writer.writeheader()
        writer.writerow(marks_dih)
        return redirect(url_for('main'))
    




    
@app.route('/predict', methods = ['GET', 'POST'])

def predict():
    x=[]
    y=[]
    if os.path.isfile("data.csv"):
        with open("data.csv", newline="") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                Math1 = int(row[0])
                Math2 = int(row[1])
                Science1 = int(row[2])
                Nepali1 = int(row[3])
                English1= int(row[4])
                Computer1 = int(row[5])
                Social1 = int(row[6])
                result1 = int(row[7])
            x.append([Math1,Math2,Science1,Nepali1,English1,Computer1,Social1])
            y.append(result1)
        X_array = np.array(x)
        y_array = np.array(y)
        Model = RandomForestClassifier(n_estimators=100)
        Model.fit(X_array,y_array)
    else:
        return "Error: No data to train on yet! Go back and add some students."
    if request.method == 'POST':
        cm = request.form.get('c_math')
        om = request.form.get('o_math')
        sci = request.form.get('science')
        nep = request.form.get('nepali')
        eg = request.form.get('english')
        cp = request.form.get('computer')
        so = request.form.get('social')

        user = [[cm,om,sci,nep,eg,cp,so]]

        pcode= Model.predict(user)
        if pcode[0] == 1:
            result_text = "Science"
        else:
            result_text = "Management"
        return render_template('index.html', prediction=result_text)
    
    return render_template('index.html')


#actual run of web app
if __name__ == '__main__':  
    app.run(debug=True)

    