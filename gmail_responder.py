import os
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Configuración general
MAX_EMAILS = 1  # Cantidad de emails no leídos a procesar

# Configuración de scopes y credenciales
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.compose']

class GmailResponder:
    def __init__(self):
        self.service = self.authenticate_gmail()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def authenticate_gmail(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.getenv('GMAIL_CREDENTIALS_PATH'), SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return build('gmail', 'v1', credentials=creds)

    def get_unread_emails(self):
        results = self.service.users().messages().list(
            userId='me',
            labelIds=['INBOX', 'UNREAD'],
            maxResults=MAX_EMAILS
        ).execute()
        return results.get('messages', [])

    def get_email_details(self, msg_id):
        message = self.service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()
        
        headers = message['payload']['headers']
        subject = next(h['value'] for h in headers if h['name'] == 'Subject')
        from_email = next(h['value'] for h in headers if h['name'] == 'From')
        
        # Extraer solo la dirección de email del campo From
        from_email = from_email.split('<')[-1].replace('>', '') if '<' in from_email else from_email
        
        body = ''
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body += base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            data = message['payload']['body']['data']
            body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return subject, body, from_email

    def generate_response(self, subject, body):
        prompt = f"Genera una respuesta profesional, en tono cordial y empatico, para el asunto: '{subject}'. Contenido del correo:\n{body}"
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente profesional que genera respuestas a correos electrónicos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1600,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    def create_gmail_draft(self, response_text, original_subject, to_email):
        message = EmailMessage()
        
        message.set_content(response_text)
        message['To'] = to_email
        message['Subject'] = f"Re: {original_subject}"
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        draft = {
            'message': {
                'raw': encoded_message
            }
        }
        
        self.service.users().drafts().create(
            userId='me',
            body=draft
        ).execute()

    def process_emails(self):
        emails = self.get_unread_emails()
        for email in emails:
            subject, body, from_email = self.get_email_details(email['id'])
            response = self.generate_response(subject, body)
            self.create_gmail_draft(response, subject, from_email)
            print(f"Respuesta guardada para: {subject}")

if __name__ == '__main__':
    responder = GmailResponder()
    responder.process_emails()
