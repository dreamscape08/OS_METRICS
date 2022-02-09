# %%
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import json
from decouple import config
import csv 
import datetime
import smtplib


f = open('/Users/dreamscape08/Desktop/Osteostrong Project/OSPGRM_files/DTC/DTC-users.json')
DTC_data = json.load(f)

DTC_username = config('DTC_username')
DTC_password = config('DTC_password')

DTC_payload = {'username': DTC_username, 'password': DTC_password}
loginurl = ('https://osteostrong.org/auth')
DTC_totals = []


with requests.session() as DTC_s:
    DTC_s.post(loginurl, data=DTC_payload)
    for i in DTC_data:
        x=i['UserId']['S']
        DTC_url = f"https://osteostrong.org/chart?UserId={x}&LocationId=00093"
        DTC_r = DTC_s.get(DTC_url)
        DTC_soup = BeautifulSoup(DTC_r.content, 'html.parser')
        DTC_total_sesh = DTC_soup.find_all('div', attrs={'class': 'col-1'})
        DTC_Total_Sessions = (DTC_total_sesh[2].text.strip())
        DTC_sesh_totals = int(DTC_Total_Sessions)
        DTC_names = DTC_soup.find_all('div', attrs={'class': 'col-2'})
        DTC_name = DTC_names[2].text.strip()[20:]
        DTC_totals.append([DTC_name, DTC_sesh_totals, x])
        
        
# fields = ['Client Name', 'Total Sessions',  'UserId']


def dateme():
    parser = datetime.datetime.now()
    return parser.strftime("%d-%m-%Y")

DTC_df=pd.DataFrame(DTC_totals, columns=['Client Name', 'Total Sessions',  'UserId'])
DTC_df['Client Name']=DTC_df['Client Name'].str.strip().convert_dtypes(str)

five=DTC_df[DTC_df['Total Sessions']==5]
ten = DTC_df[DTC_df['Total Sessions']==10]
twenty = DTC_df[DTC_df['Total Sessions']==20]
fifty=DTC_df[DTC_df['Total Sessions']==50]
seventyfive = DTC_df[DTC_df['Total Sessions']==75]
hundo = DTC_df[DTC_df['Total Sessions']==100]
hundotwenty = DTC_df[DTC_df['Total Sessions']==120]
hundofifty = DTC_df[DTC_df['Total Sessions']==150]
toohundo = DTC_df[DTC_df['Total Sessions']==200]



alert=pd.concat([five,ten,twenty,fifty,seventyfive,hundo,hundotwenty,hundofifty,toohundo],
                    axis=0,
                    join="outer"
                    ,ignore_index=True).drop(columns=['UserId'])
# alert=alert.drop(columns=['UserId'])
# alert.columns=['Client Name', 'Total Sessions'] 

DTC_df.to_excel(f'/Users/dreamscape08/Desktop/Osteostrong Project/OS_Operations/DTC_Clientdb_{dateme()}.xlsx', header=True,index=False)

operations_manager = config('opm_email')
sender_proton = config('proton_email')
p_key = config('proton_key')


to = f'{operations_manager}'
admin_email = f'{sender_proton}' # (You should provide your gmail account name)
admin_pass = f'{p_key}' # (You should provide your gmail password)
smtpserver = smtplib.SMTP('localhost',1025)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(admin_email, admin_pass)
header = 'To:' + to + '\n' + 'From: ' + admin_email + '\n' + f'Subject:DTC BASELINE ALERTS-{dateme()} \n'
msg = header + f'\n {alert} \n\n'
print(header)
smtpserver.sendmail(admin_email, to, msg)
print('done!')
smtpserver.close() 

# %%


# %%


# %%



