import smtplib
from flask_restful import Resource, Api
from flask import Flask, request, send_from_directory, render_template, send_file

def send_email(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        return "successfully sent the mail"
    except:
        return "failed to send mail"


class Email(Resource):
    def get(self):
        to = request.args['to']
        heading = request.args['heading']
        message = request.args['message']

        email = send_email("restfulnewsinfo", "Restful123", to, heading, message)
        return email
