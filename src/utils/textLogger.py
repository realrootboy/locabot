from datetime import datetime
from pytz import timezone

default_path = 'logs/'

def log(msg):
    F = open(default_path + getDailyFilename(),'a')
    F.write('[' + getFormattedTime() + ']\n')
    F.write('LOG: ' + msg + '\n\n')
    F.close()

def getDailyFilename():
    time = datetime.now(timezone('America/Sao_Paulo'))
    try:
        return time.astimezone(timezone('America/Sao_Paulo')).strftime('%d-%m-%Y')
    except:
        return None

def getFormattedTime():
    time = datetime.now(timezone('America/Sao_Paulo'))
    try:
        return time.astimezone(timezone('America/Sao_Paulo')).strftime('%d-%b-%Y (%H:%M:%S)')
    except:
        return None