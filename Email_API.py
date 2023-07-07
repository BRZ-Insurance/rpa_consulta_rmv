from __future__ import print_function

from googleapiclient.discovery import build
import os.path
import pickle
import base64
from bs4 import BeautifulSoup

def get_Verification_Code_RMV(name_rpa):

    # index_rpa
    # if index_rpa == 0:
    #     name_rpa = 'rpa'
    # if index_rpa == 1:
    #     name_rpa = 'rpa1'
    # if index_rpa == 2:
    #     name_rpa = 'arp2'
    # if index_rpa == 3:
    #     name_rpa = 'arp3'
    # if index_rpa == 4:
    #     name_rpa = 'par4'
    # if index_rpa == 5:
    #     name_rpa = 'par5'
    # if index_rpa == 6:
    #     name_rpa = 'rap6'
    # if index_rpa == 7:
    #     name_rpa = 'rap7'
    # if index_rpa == 8:
    #     name_rpa = 'pra8'
    # if index_rpa == 9:
    #     name_rpa = 'pra9'   

    path = 'token.pickle'
    with open(path, 'rb') as token:
        creds = pickle.load(token)

    service = build('gmail', 'v1', credentials=creds)
    messages = service.users().messages().list(userId='me').execute().get('messages')
    
    for index,msg in enumerate(messages):
        if index < 15: 
            email = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = email['payload'] 
            headers = payload['headers'] 
            
            for d in headers:
                if d['name'] == 'To':
                    To = d['value']
                    
                if d['name'] == 'Subject':
                    Subject = d['value']          

            if "RMV’s ATLAS eServices Portal Security Code" in (Subject):
                if To == f'{name_rpa}@brzinsurance.com':
                    html = BeautifulSoup(base64.b64decode(payload['body']['data'].replace("-","+")),'html.parser')
                    verification_code = str(html).split('Here is the temporary one-time Security Code: ')[1][0:6]
                    print(verification_code)
                    return verification_code
        else:break
    return None