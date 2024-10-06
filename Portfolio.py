import json
import datetime
from collections import defaultdict
import numpy as np
import numpy_financial as npf

with open('transaction_detail.json') as f:
    data = json.load(f)

portfolio_value = 0
portfolio_gain = 0

cashflows = []
dates = []

for summary in data[0]['data']:
    for scheme in summary['dtSummary']:
        closing_balance = float(scheme['closingBalance'])
        nav = float(scheme['nav'])
        cost_value = float(scheme['costValue'])

        current_value = closing_balance * nav
        acquisition_cost = cost_value

        portfolio_value += current_value
        portfolio_gain += (current_value - acquisition_cost)

for transaction in data[0]['data']:
    for trxn in transaction['dtTransaction']:
        if trxn['trxnDesc'] == 'Purchase':  
            amount = float(trxn['trxnAmount'])
            trxn_date = datetime.datetime.strptime(trxn['trxnDate'], '%d-%b-%Y')
            cashflows.append(-amount) 
            dates.append(trxn_date)
cashflows.append(portfolio_value)
dates.append(datetime.datetime.now())

portfolio_xirr = npf.irr(cashflows) * 100  

print(f"Total Portfolio Value: {portfolio_value:.2f}")
print(f"Total Portfolio Gain: {portfolio_gain:.2f}")
print(f"Portfolio XIRR: {portfolio_xirr:.2f}%")
