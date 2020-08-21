from __future__ import print_function
import pickle
import os.path
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SAMPLE_SPREADSHEET_ID = '1xM0am0yPoynN5aZgJ3v0-NBB_8QJrPoTnGdynILPJ8o'
SAMPLE_RANGE_NAME = 'Respostas ao formulário 1!A2:G'

def setup():
    creds = None
    if os.path.exists('secrets/falcao/token.pickle'):
        with open('secrets/falcao/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets/falcao/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('secrets/falcao/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)

def getMotoristasSet():
    service = setup()

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    motorista_set = []

    if not values:
        print('No data found.')
    else:
        for row in values:
            motorista_set.append({'nome': row[1], 'horarios': dict(), 'total_final': '00:00:00'})

    motorista_set = list({v['nome']:v for v in motorista_set}.values())

    for motorista in motorista_set:
        for row in values:
            if row[1] == motorista['nome']:
                data, hora = row[0].split(' ')
                motorista['horarios'][data] = [['','','']]

        for row in values:
            if row[3] == 'Inicial' and motorista['nome'] == row[1]:
                registered = False
                data, hora = row[0].split(' ')
                try:
                    for hrs in motorista['horarios'][data]:
                        if hrs[0] == '':
                            hrs[0] = row[4]
                            registered = True
                            break;
                    if not registered:
                        motorista['horarios'][row[5]].append((row[4],'',''))
                    registered = False
                except:
                    continue
            if row[3] == 'Final' and motorista['nome'] == row[1]:
                data, hora = row[0].split(' ')
                try:
                    for hrs in motorista['horarios'][data]:
                        if hrs[1] == '':
                            hrs[1] = row[4]
                            break;
                except:
                    continue

        for dia in list(motorista['horarios']):
            for hrs in list(motorista['horarios'][dia]):
                if (not hrs[0] == '') and (not hrs[1] == ''):
                    s = '2020/01/01 ' + hrs[0]
                    t = '2020/01/01 ' + hrs[1]
                    f = '%Y/%m/%d %H:%M:%S'
                    diff = (datetime.strptime(t, f) - datetime.strptime(s, f))
                    seconds = diff.total_seconds()
                    seconds = seconds % (24 * 3600) 
                    hour = seconds // 3600
                    seconds %= 3600
                    minutes = seconds // 60
                    seconds %= 60
                    
                    if not hour == 0:
                        hrs[2] = "%d:%02d:%02d" % (hour - 1, minutes, seconds)
                    else:
                        hrs[2] = "%d:%02d:%02d" % (hour, minutes, seconds)
                    

                    h, m, s = motorista['total_final'].split(':')

                    old_s = int(s)
                    s = (int(s) + seconds) % 60
                    old_m = int(m)
                    m = ((int(m) + minutes) % 60) + ((old_s + seconds) // 60)
                    h = (int(h) + int(hour - 1)) + ((old_m + minutes) // 60)
                    
                    motorista['total_final'] = '%.2d' % int(h) + ':' + '%.2d' % int(m) + ':' + '%.2d' % int(s)

    return motorista_set
