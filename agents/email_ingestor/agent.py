import os.path
import base64
import re
from email import message_from_bytes

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.cloud import firestore


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class EmailIngestorAgent:
    def __init__(self):
        self.service = self.authenticate_gmail()
        self.db = firestore.Client()

    def authenticate_gmail(self):
        creds = None
        token_path = 'infra/credentials/token.json'
        creds_path = 'infra/credentials/gmail_credentials.json'

        # Load or generate tokens
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def fetch_unread_emails(self):
        results = self.service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        messages = results.get('messages', [])

        for msg in messages:
            full_msg = self.service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = full_msg.get("payload", {})
            body_data = self.extract_body(payload)
            subject = self.extract_header(payload, 'Subject')
            sender = self.extract_header(payload, 'From')

            email_data = {
                "subject": subject,
                "sender": sender,
                "body": body_data
            }

            # Store in Firestore
            self.store_email(email_data)

    def extract_header(self, payload, header_name):
        headers = payload.get("headers", [])
        for header in headers:
            if header.get("name") == header_name:
                return header.get("value")
        return ""

    def extract_body(self, payload):
        try:
            parts = payload.get("parts", [])
            for part in parts:
                if part["mimeType"] == "text/plain":
                    body_data = part["body"]["data"]
                    decoded_data = base64.urlsafe_b64decode(body_data).decode("utf-8")
                    return decoded_data.strip()
        except Exception:
            return ""
        return ""

    def store_email(self, data):
        doc_ref = self.db.collection('emails').document()
        doc_ref.set(data)
        print("Email stored:", data)


# Test the agent (only for dev testing)
if __name__ == "__main__":
    agent = EmailIngestorAgent()
    agent.fetch_unread_emails()
