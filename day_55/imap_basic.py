import imaplib
import logging
import ssl
import os
import sys
import email

import cchardet

IMAP_USER_NAME = os.getenv("IMAP_USER_NAME")
IMAP_USER_PASSWORD = os.getenv("IMAP_USER_PASSWORD")

imap_server_name = "imap.slack.net"

# Load system's trusted SSL certificates
tls_context = ssl.create_default_context()

# Connect (unencrypted at first)
server = imaplib.IMAP4(imap_server_name)
# Start TLS encryption. Will fail if TLS session can't be established
server.starttls(ssl_context=tls_context)
# Login. ONLY DO THIS AFTER server.starttls() !!

try:
    server.login(IMAP_USER_NAME, IMAP_USER_PASSWORD)
except imaplib.IMAP4.error as imap_err:
    logging.fatal(f"IMAP login to {IMAP_USER_NAME}@{imap_server_name} failed with err '{imap_err}'")
    sys.exit(-1)

# Print list of mailboxes on server
code, mailboxes = server.list()
for mailbox in mailboxes:
    if mailbox is None:
        continue

    print(mailbox.decode("utf-8"))

# Select mailbox
server.select("INBOX")

i = 0
max_messages = 5

typ, data = server.search(None, 'ALL')
for num in data[0].split():
    typ, msg_data = server.fetch(num, '(RFC822)')
    for response_part in msg_data:

        if isinstance(response_part, tuple):
            print(cchardet.detect(response_part[1]))
            mail_part_bytes_encoding = cchardet.detect(response_part[1])
            if mail_part_bytes_encoding["encoding"] in ("UTF-8", "ASCII"):
                msg = email.message_from_string(response_part[1].decode("utf-8"))
                for header in ['subject', 'to', 'from']:
                    print('%-8s: %s' % (header.upper(), msg[header]))
            else:
                logging.info(f"Message {num} has unprocessable encoding {mail_part_bytes_encoding}. Skipping")
                break

    i += 1
    if i > max_messages:
        break

# Cleanup
server.close()  # 'close' closes the mail folder, not the connection
server.logout()
