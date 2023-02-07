from flask import Flask, request, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/import', methods=['GET', 'POST'])
def import_data():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)

        # Perform data analysis
        income_statement = df.groupby(['Year']).sum()
        income_statement = income_statement[['Revenue', 'Expenses']]
        income_statement['Profit'] = income_statement['Revenue'] - income_statement['Expenses']
        balance_sheet = df.groupby(['Year']).sum()
        balance_sheet = balance_sheet[['Assets', 'Liabilities', 'Equity']]
        balance_sheet['LiabilitiesAndEquity'] = balance_sheet['Liabilities'] + balance_sheet['Equity']

        # Generate smart reports
        reports = {}
        if income_statement['Profit'].mean() < 0:
            reports['income_statement'] = "The company has been operating at a loss, on average, over the years. Consider reviewing expenses."
        if balance_sheet['LiabilitiesAndEquity'].iloc[-1] > balance_sheet['Assets'].iloc[-1]:
            reports['balance_sheet'] = "The company's liabilities and equity are greater than its assets in the latest year. Consider reducing liabilities or increasing assets."

        # Create graphs
        img = io.BytesIO()
        plt.figure(figsize=(10,5))
        plt.plot(income_statement.index, income_statement['Revenue'], label='Revenue')
        plt.plot(income_statement.index, income_statement['Expenses'], label='Expenses')
        plt.plot(income_statement.index, income_statement['Profit'], label='Profit')
        plt.legend(loc='best')
        plt.title('Income Statement')
        plt.xlabel('Year')
        plt.ylabel('Amount (USD)')
        plt.savefig(img, format='png')
        img.seek(0)
        income_statement_plot = base64.b64encode(img.getvalue()).decode('utf-8')

        img = io.BytesIO()
        plt.figure(figsize=(10,5))
        plt.plot(balance_sheet.index, balance_sheet['Assets'], label='Assets')
        plt.plot(balance_sheet.index, balance_sheet['LiabilitiesAndEquity'], label='Liabilities and Equity')
        plt.legend(loc='best')
        plt.title('Balance Sheet')
        plt.xlabel('Year')
        plt.ylabel('Amount (USD)')
        plt.savefig(img, format='png')
        img
