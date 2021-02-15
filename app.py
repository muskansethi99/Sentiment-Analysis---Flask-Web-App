import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import sqlite3 as sql
import database

model = pickle.load(open('Desktop/RFModel.pkl','rb'))
vectorizer = pickle.load(open('Desktop/FVectorizer.pkl','rb'))
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/result',methods =['POST'])
def prediction():
    if request.method == 'POST':
        try:
            review = request.form['review']
            print([review])
            test_bag = vectorizer.transform([review]).toarray()
            review_prediction = model.predict(test_bag)
            result = 'Positive review' if review_prediction[0] else 'Negative Review'
            feedback = 'no feedback'
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO sentiment_analysis (review,prediction,feedback) VALUES (?,?,?)",(review,result,feedback))
                con.commit()
                print("Record successfully added")
        except:
            con.rollback()
            print("error in insert operation")
      
        finally:
            con.close()
            return render_template("result.html",pred = result,review=review)
           
       

@app.route('/data')
def list_all():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("select * from sentiment_analysis")
    
    rows = cur.fetchall() # returns list of dictionaries
    return render_template("data.html",rows = rows)

@app.route('/feedback',methods =['POST'])
def feedback():
    try:
        rev = request.form['rev']
        feedback = request.form['feedbac']
        result = request.form['predict']
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE sentiment_analysis SET feedback = ? WHERE review = ?;",(feedback,rev))
            print("Record successfully updated")
            con.commit()
    except:
        con.rollback()
        print("error in update operation")
      
    finally:
        con.close()
    return render_template("result.html",pred = result,review=rev)   


if __name__ == '__main__':
   app.run(debug=True)