#pylint: disable=E1101

import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sendMail import sendMail
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"{os.environ.get('DATABASE_URL')}"
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    emailDB = db.Column(db.String(120), unique=True)
    heightDB = db.Column(db.Integer)
    weightDB = db.Column(db.Integer)
    bmiDB = db.Column(db.Float(precision=1))

    def __init__(self, emailDB, heightDB, weightDB, bmiDB):
        self.emailDB = emailDB
        self.heightDB = heightDB
        self.weightDB = weightDB
        self.bmiDB = bmiDB

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/successful", methods=["POST"])
def successful():
    try:
        if request.method == "POST":
            email = request.form["emailVal"]
            height = request.form["heightVal"]
            weight = request.form["weightVal"]

            #If email doesn't exist in database
            if db.session.query(Data).filter(Data.emailDB == email).count() == 0:
                bmi = (float(weight)) / (float(height) / 100) ** 2
                data = Data(email, height, weight, bmi)
                bmiRange = bmiRangeGet(bmi)
                average = db.session.query(func.avg(Data.bmiDB)).scalar()
                sendMail(email, height, weight, bmi, bmiRange, average)
                db.session.add(data)
                db.session.commit()
                return render_template("successful.html") 
            
            #Update info if email exists in database
            elif db.session.query(Data).filter(Data.emailDB == email).count() == 1:
                entity = db.session.query(Data).filter(Data.emailDB == email).first()
                entity.heightDB = height
                entity.weightDB = weight
                entity.bmiDB = (float(entity.weightDB)) / (float(entity.heightDB) / 100) ** 2
                bmiRange = bmiRangeGet(entity.bmiDB)
                average = db.session.query(func.avg(Data.bmiDB)).scalar()
                sendMail(email, height, weight, entity.bmiDB, bmiRange, average)
                db.session.commit()
                return render_template("updated.html")
    except Exception as e:
        print(e)
        return render_template("error.html") 

def bmiRangeGet(bmi):
    if (bmi < 18.5):
        return "underweight"
    elif (bmi > 18.5 and bmi < 24.9):
        return "normal"
    elif (bmi > 25 and bmi < 29.9):
        return "overweight"
    elif (bmi > 30 and bmi < 34.9):
        return "obese"
    elif (bmi > 35):
        return "extremely obese"

if __name__ == "__main__":
    app.debug = True
    app.run()