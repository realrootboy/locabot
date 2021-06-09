from __future__ import print_function
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/drive.appdata',
          'https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']

def get_gdrive_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('src/backup/token.json'):
        creds = Credentials.from_authorized_user_file('src/backup/token.json', SCOPES)
    


    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'src/backup/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('src/backup/token.json', 'w') as token:
            token.write(creds.to_json())

    drive_service = build('drive', 'v3', credentials=creds)

    return  drive_service



# @brief:Esta função faz upload para o drive das fotos de combustível enviadas pelos motorista
# @param path: é o caminho da pasta onde as fotos estão quando enviadas
# @return: Função sem retorno
def upload_photos_fuel(path): 
    drive_service = get_gdrive_service()
  
    folder_id = '1wR4dsOgXWuE51gA55lSfL3PVEa7SEcFZ'
    files = os.listdir(path)

    file_metadata = {
        'name': path.replace('media/', ''),
        'mimeType': 'application/vnd.google-apps.folder',
        'parents':[folder_id]
    }

    file_folder = drive_service.files().create(body=file_metadata,
                                    fields='id').execute()

    for f in files:
        file_metadata = {  
            'name': f,
            'parents':[file_folder.get('id')] 
        }
        media = MediaFileUpload( path + f,
                             mimetype = '*/*'
                             )

        file = drive_service.files().create(body=file_metadata,
                                         media_body=media,
                                         fields='id').execute()



# @brief:Esta função faz upload para o drive dos Dumps Postgres
# @param path: é o caminho da pasta onde os Dumps estão
# @return: Função sem retorno
def upload_photos_Dumps_Postgres(path): 
    drive_service = get_gdrive_service()
    
    folder_id = '1cTjgn3sy4R1p7Hcc47EGMiIeayndBG5i'
    files = os.listdir(path)

    for f in files:
        file_metadata = {  
            'name': f,
            'parents':[folder_id] 
        }
        media = MediaFileUpload( path + f,
                             mimetype = '*/*'
                             )

        file = drive_service.files().create(body=file_metadata,
                                         media_body=media,
                                         fields='id').execute()



    #Criacao da pasta Backup de Fotos
    # file_metadata = {
    # 'name': 'Backup de Fotos',
    # 'mimeType': 'application/vnd.google-apps.folder'
    # }
    # file = drive_service.files().create(body=file_metadata,
    #                                     fields='id').execute()
    # print('Folder ID: %s' % file.get('id'))
    #ID da pasta Backup de Fotos: 1eArdfcIfPmNAJTSdzY5WqqBjSRdJo0Ah

    #Criacao da pasta 1. Fotos de Combustivel
    # file_metadata = {
    # 'name': ' 1. Fotos de Combustivel',
    # 'mimeType': 'application/vnd.google-apps.folder'
    # }
    # file = drive_service.files().create(body=file_metadata,
    #                                     fields='id').execute()
    # print('1. Fotos de Combustivel ID: %s' % file.get('id'))
    #1. Fotos de Combustivel ID: 1wR4dsOgXWuE51gA55lSfL3PVEa7SEcFZ

    #Criacao da pasta 2.Dumps Postgres
    # file_metadata = {
    # 'name': '2. Dumps Postgres',
    # 'mimeType': 'application/vnd.google-apps.folder'
    # }
    # file = drive_service.files().create(body=file_metadata,
    #                                     fields='id').execute()
    # print('2.Dumps Postgres ID: %s' % file.get('id'))
    # 2.Dumps Postgres ID: 1cTjgn3sy4R1p7Hcc47EGMiIeayndBG5i