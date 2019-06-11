import smtplib

host = 'smtp.mailtrap.io'
port = 2525
username = '35168fcb5b067e'
password = '18326454908117'

sender = 'pi@raspberry.com'
receiver = 'whore@cutup.com'
msg = 'you got robbed, manqk.'


def send(message=msg):
    try:
        smtp_server = smtplib.SMTP(host, port)
        smtp_server.login("35168fcb5b067e", "18326454908117")
        smtp_server.sendmail(sender, receiver, message)
        smtp_server.quit()
        print('mail sent :)')
    except:
        print('fail....')

