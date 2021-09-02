# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import base64
import dateutil
import mysql.connector as sql
import os
import pandas as pd
import streamlit as st
import ruamel.yaml as yaml
import lib
import deetly as dl
import numpy as np
import datetime



db_config = dict([
    ('hostname', 'canvasdb.caxvr8jox9y6.us-east-2.rds.amazonaws.com'),
    ('port', 3306),
    ('username', 'admin'),
    ('password', '77YnH0bqO8oHMYZGmu78'),
    ('database', 'Vriddhi')
])

conn = sql.connect(host=db_config['hostname'], port=db_config['port'], user=db_config['username'], password=db_config['password'], database=db_config['database'])


mem_list = pd.read_sql(f"SELECT MemID FROM Curr_Accounts_2021_08_Member",
                       conn)

st.title("DISBURSEMENT CALCULATOR")

member_id = st.selectbox("Member-List", mem_list)

print(member_id)

loan_amount = st.number_input('Loan Amount', min_value=0, max_value=1000000, value=0)

interest_rate = st.number_input('Interest Rate', min_value=0, max_value=30, value=0)

today = datetime.date.today()

Date_Disb_JLG_Loan = st.date_input('Date_Of_Disbursement', today)

Balance_IB = pd.read_sql(f"SELECT COT_Balance_IB FROM Curr_Accounts_2021_08_Member WHERE MemID = %s",
                       conn, params={member_id})

Balance_IB = float(Balance_IB.iat[0, 0])


Mem_IB_Balance = pd.read_sql(f"SELECT Mem_Balance_IB FROM Curr_Accounts_2021_08_Member WHERE MemID = %s",
                       conn, params={member_id})

Mem_IB_Balance = float(Mem_IB_Balance.iat[0, 0])


# Guaranteed to get the next month. Force any_date to 28th and then add 4 days.
next_month = Date_Disb_JLG_Loan.replace(day=28) + datetime.timedelta(days=4)

# Subtract all days that are over since the start of the month.
Date_Disb_EOM = next_month - datetime.timedelta(days=next_month.day)



print(Balance_IB, Mem_IB_Balance)

Int_Amount = (Date_Disb_EOM.day - Date_Disb_JLG_Loan.day + 1)/365 * loan_amount * interest_rate/100

Loan_Processing_Fees = 2/100 * loan_amount


Disbursal_Amount = loan_amount - Balance_IB - Mem_IB_Balance - Int_Amount - Loan_Processing_Fees

Amount_Msg = '<p style="font-family:Courier; color:Blue; font-size: 20px;">"Amount to be Disbursed" round(Disbursal_Amount, 2)</p>'

st.write("COT Balance", Balance_IB)

st.write("Membership Balance", Mem_IB_Balance)

st.write("Interest Amount", round(Int_Amount, 2))

st.write("Loan Processing Fees", Loan_Processing_Fees)

st.write("Amount to be Disbursed", round(Disbursal_Amount, 2))






