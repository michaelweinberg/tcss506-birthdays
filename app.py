from pickle import FALSE
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
import datetime
import requests
import json

class loginForm(FlaskForm):
    email=StringField(label="Enter email", validators=[DataRequired(),Email()])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    submit=SubmitField(label="Login")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

passwords={}
passwords['email@example.com'] = "qwerty5"

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]
# ...

@app.route('/')
def redirectToLogin():
    return redirect("/login")

@app.route('/test')  
def test():
    return render_template("test.html")

@app.route("/login",methods=['GET','POST'])
def login():
    form=loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email=request.form["email"]
            pw=request.form["password"]
            # return "user is {} and pw is {}\n".format(email, pw)
            if email is not None and email in passwords and passwords[email] == pw:
            # user = UserModel.query.filter_by(email = email).first()
            # if user is not None and user.check_password(pw) :
            #     login_user(user)
                return redirect('/birthdays')
    return render_template("login.html",form=form)

@app.route("/logout")
def logout():
    return redirect('/login')

@app.route('/birthdays', methods=('GET', 'POST'))
def birthdays():
    result = []
    loading = 0
    if request.method == 'POST':
        print(loading)
        month = request.form['month']
        day = request.form['day']
        year= request.form['year']
        result = findBirths(month + '/' + day, year)
        loading = 0
        # if not title:
        #     flash('Title is required!')
        # elif not content:
        #     flash('Content is required!')
        # else:
        #     messages.append({'title': title, 'content': content})
        #     return redirect(url_for('index'))

    return render_template('birthdays.html', birthdays=result)

def findBirths(monthDay,year,size=10):
    #monthDay is in form "mm/dd"
    #year is in form "yyyy"
    #returns a list of names, birth years and thumbnails 
    #sortedbyClosestYear[i]['text'] has name of ith match
    #sortedbyClosestYear[i]['year'] has year of ith match's birthdate
    #sortedbyClosestYear[i]['thumbnail'] has url of ith match's thumbnail picture or localhost if there is none
    size=int(size)
    year=int(year)
    path="https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday"
    response=requests.get(path+"/births/"+monthDay)
    data=response.json()
    sortedbyClosestYear=sorted(data["births"], key=lambda i: abs(int(i['year'])-year))
    if len(sortedbyClosestYear) > size:
        sortedbyClosestYear=sortedbyClosestYear[0:size]
    for item in sortedbyClosestYear:
        item['thumbnail']="localhost"
        if "thumbnail" in item['pages'][0]:
            item['thumbnail']=item['pages'][0]["thumbnail"]["source"]
    return sortedbyClosestYear

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)