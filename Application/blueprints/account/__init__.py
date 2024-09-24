import csv
import io
from flask import Blueprint, flash, redirect, render_template, send_file, url_for
from flask_login import login_required, current_user
import numpy as np
from .forms import CompanyFinancialForm
from Application import db
from .algo import algorithm
import pandas as pd
import os

bp = Blueprint(
    'Account',
    __name__,
    url_prefix='/account',
    static_folder='static',
    template_folder='templates'
)

format_csv_path = os.path.join(str(bp.static_folder), 'format.csv') 

def validate_csv_headers(input_df, reference_csv=format_csv_path):
    reference_df = pd.read_csv(reference_csv)

    input_headers = set(input_df.columns)
    reference_headers = set(reference_df.columns)

    if not input_headers == reference_headers:
        raise ValueError("The uploaded CSV file has invalid format")

    for index, row in input_df.iterrows():
        company_value = row['Company']

        if str(pd.to_numeric(company_value, errors='coerce')) != str(np.nan):
            raise ValueError(f"Row {index} has an invalid Company value: {company_value}")

        for column in input_df.columns:
            if column != 'Company':
                if str(pd.to_numeric(row[column], errors='coerce')) == str(np.nan):
                    raise ValueError(f"Row {index} has a non-numeric value in column '{column}': {row[column]}")   
        
    if input_df['Company'].duplicated().any():
        raise ValueError("The Company names must be unique.")

@bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = CompanyFinancialForm()

    if form.validate_on_submit():
        csv_file = io.StringIO(form.csv_file.data.stream.read().decode('utf-8'))
        try:
            df = pd.read_csv(csv_file)
            validate_csv_headers(df)
            print('firstout-------------------------------------')
            output = algorithm(df.copy())
            print('thirdout-------------------------------------')
            companies = df['Company'].tolist()
            print('finalout-------------------------------------')
            return render_template(
                'account/dashboard.html', 
                user=current_user,
                form=form,
                results=zip(companies, output)
            )
        except Exception as e:
            form.csv_file.errors.append(str(e))

    return render_template(
        'account/dashboard.html', 
        user=current_user,
        form=form
    )


@bp.get('/profile')
@login_required
def profile():
    return render_template('account/profile.html', user=current_user)


@bp.get('/format')
@login_required
def format():
    return bp.send_static_file('format.csv')