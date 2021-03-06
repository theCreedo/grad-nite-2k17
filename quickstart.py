from __future__ import print_function
import httplib2
import os
import base64
import cPickle as pickle

from apiclient import errors
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from email.mime.text import MIMEText

# Load all the emails saved from pickle.py
emails = pickle.load(open( "emails.p", "rb" ))

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json

# We want the scope to be only able to create and send messages.
# https://developers.google.com/gmail/api/auth/scopes
SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError,e:
    print('An error occurred: ' + str(e))


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    # Initializing the service http request service
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    # name_email to list of sender-name_text
    # values = {'receiverName_receiverEmail':['senderName_senderMessage']}
    values = pickle.load(open("values.p", "rb"))
    # sender - Need to add your email here
    sender = '<Input your Gmail Email Here>'
    for graduate_name in values:
        # to
        to = emails[graduate_name]
        # For debugging purposes
        print(to)
        m = 'Dear '+ graduate_name + '!'
        subject = 'Graduate Blessings from Empire for ' + graduate_name
        for y in values[graduate_name]:
            sname_smsg = y.split('_')
            sname = sname_smsg[0]
            message_text = sname_smsg[1]
            # text
            m += '\n\n' + message_text + '\n\t\t\t\t\t\tLove,\n\t\t\t\t\t\t' + sname + '\n'
        # create the message
        message = create_message(sender, to, subject, m)
        # send message
        sent_message = send_message(service, 'me', message) 


if __name__ == '__main__':
    main()