"""

If you want to use really secure connection, you MUST read this articles:

https://docs.python.org/3/library/imaplib.html#imaplib.IMAP4_SSL
https://docs.python.org/3/library/ssl.html#ssl-security

"""

import ssl

from imap_tools import MailBoxTls

import ssl
import os

IMAP_USER_NAME = os.getenv("IMAP_USER_NAME")
IMAP_USER_PASSWORD = os.getenv("IMAP_USER_PASSWORD")

# Load system's trusted SSL certificates
tls_context = ssl.create_default_context()

print("Going to connect")

with MailBoxTls('imap.slack.net', ssl_context=tls_context).login(IMAP_USER_NAME, IMAP_USER_PASSWORD) as mailbox:
    print("Connected")
    for msg in mailbox.fetch():
        print(msg.subject, msg.date_str)


print("done")