from flask import Flask, render_template, url_for, redirect, flash
from flask_restful import request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import EmailField, PasswordField, StringField
from wtforms import validators
import requests
import pandas as pd


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretlol'
bootstrap = Bootstrap(app)


class LoginForm(FlaskForm):
    user_email = EmailField(label='Email', validators=[validators.DataRequired()])
    user_password = PasswordField(label='Password', validators=[validators.DataRequired()])


class InputForm(FlaskForm):
    ticker = StringField(label="Ticker", validators=[validators.DataRequired()])


@app.route('/')
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.user_email.data == 'admin@admin.com' and form.user_password.data == 'admin':
            return redirect(url_for('home'))
        else:
            flash('Authentication failure', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/home", methods=['GET', 'POST'])
def home():
    form = InputForm()
    return render_template('home.html', title='Home', form=form)


@app.route("/api/v1/stocks/")
def get_stocks():

    TICKER = request.args.get('ticker')
    HEADER = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0"}

    try:
        response = requests.get(f"https://finviz.com/quote.ashx?t={TICKER}", headers=HEADER)
        result = pd.read_html(response.text)
        parsed = result[5]

        dict_primary = {}

        dict_primary |= dict(parsed[[0,1]].values)
        dict_primary |= dict(parsed[[2,3]].values)
        dict_primary |= dict(parsed[[4,5]].values)
        dict_primary |= dict(parsed[[6,7]].values)
        dict_primary |= dict(parsed[[8,9]].values)
        dict_primary |= dict(parsed[[10,11]].values)

        return dict_primary, 200
    except IndexError:
        return {"Message": "Ticker ID not found."}


if __name__ == '__main__':
    app.run(debug=True)
