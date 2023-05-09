import json
import os
import smtplib

import pandas as pd
from sqlalchemy import literal_column
from werkzeug.security import check_password_hash

from application.forms import ContactForm, LoginForm
from application.main import app, db, login_manager
from application.models import ChurnDataPrep, TrainDataPrep, Users
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, login_required, logout_user



def get_churn_rate_by_location(db, location, churn_col, table):
    results = db.session.query(getattr(table, location),
                               db.func.sum(getattr(table, churn_col)) * 1.0 / db.func.count('*').label('churn_rate')) \
        .group_by(getattr(table, location)) \
        .all()

    churn_rates_by_location = {f'{location}': [], 'churn_rate': []}
    for row in results:
        churn_rates_by_location[f'{location}'].append(row[0])
        churn_rates_by_location['churn_rate'].append(row[1])

    return churn_rates_by_location


def send_email(name, email, subject, message):
    smtp_username = os.environ['smtp_email']
    smtp_password = os.environ['smtp_email_password']
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=smtp_username, password=smtp_password)
        connection.sendmail(from_addr=smtp_username, to_addrs='nagair.goncalves@gmail.com',
                            msg=f'Subject: {subject}\n\n{name}\n{email}\n{message}')


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Define the custom error page for Bad Request error
@app.errorhandler(400)
def handle_bad_request(error):
    return render_template('pages-error-400.html'), 400


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Get the data
    if request.args.get('filter_id') and request.args.get('filter_id') == 'Last Year':
        filter_id = request.args.get('filter_id')
        churn_col = 'churn'
        table = TrainDataPrep
    else:
        filter_id = ''
        churn_col = 'prediction'
        table = ChurnDataPrep

    # ****************************Calculate Statistics**************************************
    risky_customers = db.session.query(db.func.sum(getattr(table, churn_col))).scalar()

    monthly_income_risky_customers = db.session.query(
        db.func.sum(
            (table.total_day_charge + table.total_eve_charge + table.total_night_charge) / (
                    table.account_length + literal_column('0.0')) * 30 *
            db.func.ifnull(getattr(table, churn_col), 0)
        )
    ).filter(getattr(table, churn_col) == 1).scalar()

    total_customers = db.session.query(db.func.count(getattr(table, churn_col))).scalar()
    retention_rate = (total_customers - risky_customers) / total_customers

    statistics = {'Risky Customers': risky_customers,
                  'Monthly Income Risky Customers': f'${monthly_income_risky_customers:.2f}',
                  'Customer Retention Rate': f'{(retention_rate * 100):.2f}%'
                  }
    # ****************************End Calculate Statistics**************************************

    # ****************************Churn By Account Length Data Plot*****************************
    churn_by_acct_length = db.session.query(table.account_length,
                                            db.func.sum(getattr(table, churn_col)) * 1.0 / db.func.count(
                                                '*').label('churn_rate')) \
        .group_by(table.account_length) \
        .all()

    churn_by_acct_length = pd.DataFrame(churn_by_acct_length, columns=['account_length', 'churn_rate'])
    churn_by_acct_length['churn_rate'] = churn_by_acct_length['churn_rate'].fillna(0)

    chart_data = {"labels": churn_by_acct_length['account_length'].tolist(),
                  "data": [round(num, 2) for num in churn_by_acct_length['churn_rate'].tolist()]}

    # ****************************End Churn By Account Length Data Plot*****************************

    # ************************** State Data Plot *****************************************************
    state_data = pd.DataFrame(get_churn_rate_by_location(db, 'state', churn_col, table))

    # creating a state indexed version of the dataframe so we can lookup values
    state_data_indexed = state_data.set_index('state')

    with open('application/us_state_test.json', 'r') as f:
        content = json.load(f)

    # looping through the geojson object and adding a new property(churn_rate)
    # and assigning a value from our dataframe
    for s in content['features']:
        s['properties']['churn_rate'] = state_data_indexed.loc[s['id'], 'churn_rate']

    json_string = json.dumps(content)

    with open('application/static/js/us_states.js', 'w') as f:
        f.write("var statesData = " + json_string + ";")

    # ************************** End State Data Plot *****************************************************

    # County data Plot
    county_data = [round(x, 2) for x in
                   sorted(get_churn_rate_by_location(db, 'county', churn_col, table)['churn_rate'], reverse=True)]

    # Region data plot
    region_data = [round(x, 2) for x in
                   sorted(get_churn_rate_by_location(db, 'region', churn_col, table)['churn_rate'], reverse=True)]

    return render_template('index.html', statistics=statistics, filter_id=filter_id,
                           county_data=json.dumps(county_data),
                           account_length_data=json.dumps(chart_data['data']),
                           region_data=json.dumps(region_data),
                           )


@app.route('/table')
@login_required
def get_data_table():
    table = ChurnDataPrep.query.all()
    return render_template('tables-data.html', table=table)


@app.route("/contact", methods=['GET', 'POST'])
@login_required
def get_contact_page():
    contact_form = ContactForm(request.form)
    if contact_form.validate_on_submit():
        data = contact_form.data
        send_email(data['name'], data['email'], data['subject'], data['message'])
        flash('Form submitted successfully!')
        return redirect(url_for("get_contact_page"))
    return render_template('pages-contact.html', form=contact_form)


@app.route('/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        data = login_form.data
        user = Users.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            remember = data.get('remember_me')
            login_user(user, remember=remember)
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect email or password')
            return redirect(url_for('login'))
    return render_template("pages-login.html", form=login_form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))