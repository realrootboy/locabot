# sudo pip3 install xlsxwriter google-api-python-client google-auth-httplib2 google-auth-oauthlib tabulate requests tqdm
# sudo pip3 install --upgrade google-api-python-client

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']

def get_gdrive_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('secrets/gdrive/token.pickle'):
        with open('secrets/gdrive/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets/gdrive/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('secrets/gdrive/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return Google Drive API service
    return build('drive', 'v3', credentials=creds)

def upload_gdrive(local_path='', name_to_save=''):
    service = get_gdrive_service()
    folder_id = '1gg7tafAZTnlsbrDgV8uPJHocKwFODQZ2'

    file_metadata = {'name': name_to_save,
                     'parents': [folder_id]}

    page_token = None

    while True:
        response = service.files().list(q="name='" + name_to_save+"'",
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name, parents)',
                                        pageToken=page_token).execute()
        for file in response.get('files', []):
            if (folder_id in file.get('parents')):
                service.files().delete(fileId=file.get('id')).execute()
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    media = MediaFileUpload(local_path,
                            mimetype='application/vnd.ms-excel')

    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

    print ('File ID: %s' % file.get('id'))
# create the folder
# folder_metadata = {
#     "name": "TestFolder",
#     "mimeType": "application/vnd.google-apps.folder"
# }
# file = service.files().create(body=folder_metadata, fields="id").execute()
# get the folder id
# folder_id = file.get("id")
# print("Folder ID:", folder_id)