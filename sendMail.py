from email.mime.text import MIMEText
import smtplib
import sys


def send_mail(claimer, giver, item_name):
    username = ''   # sender email
    password = ''   # sender emails password

    message = MIMEText(f'Hey {claimer}, you have just claimed {item_name} on {giver}s channel.')  # text
    message['Subject'] = 'CLAIM'  # Subject
    message['From'] = username  # From
    recipient = ''  # To

    # SMTP object with ecrypting using ssl
    with smtplib.SMTP_SSL('smtp.seznam.cz', 465) as smtp: # ready for email.cz domain, feel free to change to eg. gmail (also port)
        print('Logging in...')
        try:
            smtp.login(username, password)
        except Exception as e:
            print('Logging failed.', e)
            sys.exit()

        print('Sending email...')
        try:
            smtp.sendmail(username, recipient, message.as_string())
        except Exception as e:
            print('Sending failed.', e)
            sys.exit()

        print('OK')


def send_mail_availability(claimer, giver, item_name):
    username = ''
    password = ''

    message = MIMEText(f'Hey {claimer}, {item_name} on {giver}s channel is ready to be claimed. Added to QUEUE, wait for confirmation mail about your claim.')  # text
    message['Subject'] = 'CLAIM AVAILABLE'  # Subject
    message['From'] = username  # From
    recipient = ''  # To

    # SMTP object with ecrypting using ssl
    with smtplib.SMTP_SSL('smtp.seznam.cz', 465) as smtp:
        print('Logging in...')
        try:
            smtp.login(username, password)
        except Exception as e:
            print('Logging failed.', e)
            sys.exit()

        print('Sending email...')
        try:
            smtp.sendmail(username, recipient, message.as_string())
        except Exception as e:
            print('Sending failed.', e)
            sys.exit()

        print('OK')
