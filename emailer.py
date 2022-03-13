import smtplib, ssl, time

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "<Enter sending email>"
receiver_email = "<Enter recieveing email>"
password = "<Enter password for sending email>" #will implement enviroment variables in the future, for safer usage of the sender email

def email(message, recEmail):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, recEmail, message)
    time.sleep(0.1)
