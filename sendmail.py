## Based on: http://docs.python.org/library/email-examples.html

# Import smtplib for the actual sending function
import smtplib

# Here are the email package modules we'll need
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '

def sendout(subject, sender, target, text, attachimage):
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(target)

    part1 = MIMEText(text, 'plain')
    msg.attach(part1)

    # Assume we know that the image files are all in PNG format
    for file in attachimage:
        # Open the files in binary mode.  Let the MIMEImage class automatically
        # guess the specific image type.
        fp = open(file, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        img.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(img)

    # Send the email via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.sendmail(sender, target, msg.as_string())
    s.quit()
