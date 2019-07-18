from flask import Flask, render_template, request, url_for,redirect,session
import os
import sqlite3

app = Flask(__name__)
app.secret_key= os.urandom(132)
sql = sqlite3.connect("database_1.db")
sql.execute("CREATE TABLE IF NOT EXISTS login(name TEXT,password TEXT)")

ques = {"Anusuiya Uikey is the new Governor of which state?":["Gujarat","Chhattisgarh","Himachal Pradesh"],
        " Which city hosted the UK-India Joint Economic and Trade Committee Meet 2019?":[" Birmingham"," Pune"," London"],
        "Who has won Women’s Singles title in 2019 Wimbledon Championships?":["Xu Yifan","Simona Halep"," Serena Williams"],
        "Which player will not be playing in Sachin Tendulkar’s World Cup XI?":["Virat Kohli","MS Dhoni"," Rohit Sharma"],
        "Which country reopened its airspace for India recently?":["China","Pakistan","UAE"],
        "NASA is commemorating the 50th anniversary of which historic mission on 20th July?":["Apollo 11","Apollo 1","Apollo 13"]}
crctans=["Chhattisgarh","London","Simona Halep","MS Dhoni","Pakistan","Apollo 11"]
selectques = []
answered=[]
for i in ques.keys():
    selectques.append(i)

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        sql = sqlite3.connect("database_1.db")
        sql.execute("INSERT INTO login(name,password)VALUES(?,?)",(request.form["name"],request.form["newpassword"]))
        sql.commit()
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/result",methods =["Post"])
def result():
    if "Username" in session:
        crct=0
        for i in selectques:
            answered.append(request.form[i])
        for j in range(0,6):
            if answered[j]==crctans[j]:
                crct= crct+1
        name = session["Username"]
        return render_template("html_ex.html",crct= crct,name=name)
    else:
        return redirect(url_for("login"))

@app.route("/quiz")
def quiz():
    if "Username" in session:
        return render_template("quiz.html",selectques=selectques,ques=ques)
    else:
        return redirect(url_for("login"))

@app.route("/",methods=["GET","POST"])
def login():
    error = ""
    if request.method=="POST":
        session["Username"]=request.form["Username"]
        sql= sqlite3.connect("database_1.db")
        data= sql.execute("SELECT * FROM login")
        for i in data:
            if i[0]== request.form["Username"] and i[1]== request.form["Password"]:
                return redirect(url_for("quiz"))
        else:
            error="Invalid Credentials try again"
            return render_template("login.html", error=error)
    return  render_template("login.html",error = error)

@app.route("/logout")
def logout():
    if "Username" in session:
        session.pop("Username",None)
        return redirect(url_for("login"))

if __name__=='__main__':
    app.run(debug=True)
