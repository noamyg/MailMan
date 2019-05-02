import smtplib as SMTPLib
import xml.etree.ElementTree as ET
from model.server import Server as SMTPServer
from controllers import templateController
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

logger = logging.getLogger('mailman_logger')

configTree = ET.parse('config.xml')
configTreeRoot = configTree.getroot()

server = SMTPServer
connection = SMTPLib.SMTP
currentConnectionName = ''

def connect(connectioName):
    global currentConnectionName
    currentConnectionName = connectioName
    for node in configTreeRoot.findall('SMTPServer'):
        if node.find('Name').text == connectioName:
            logger.info('Found Server Config: {}'.format(connectioName))
            global server
            server = SMTPServer(connectioName, node.find('Host').text, node.find('Port').text, node.find('Auth').text, node.find('UserName').text, node.find('Password').text)
            try:
                global connection
                connection = SMTPLib.SMTP(host=server.host, port=int(server.port))
                connection.set_debuglevel(1)
                try:
                    connection.connect(server.host, int(server.port))
                    connection.ehlo()
                    connection.starttls()
                    if server.auth != 'None':
                        connection.login(server.username, server.password)
                except:
                    connection.quit()
                    pass
                logger.info('Connected to {}'.format(connectioName))
                return True
            except:
                logger.info("Unable to connect to {}".format(server.name))

def testCurrentConnection(conn):
    try:
        status = conn.noop()[0]
    except:
        status = -1
    return True if status == 250 else False

def sendMail(to, cc, bcc, template, bodyParams, subjectParams):
    global connection
    if not testCurrentConnection(connection):
        connect(currentConnectionName)
    subject, fromEmail, body = templateController.readTemplate(template)
    msg = MIMEMultipart('alternative')
    msg['From'] = fromEmail
    msg['To'] = to
    msg['Cc'] = cc
    if subjectParams:
        msg['Subject'] = templateController.replaceTextWithParams(subject, subjectParams)
    else:
        msg['Subject'] = subject
    if bodyParams:
        msg['Body'] = templateController.replaceTextWithParams(body, bodyParams)
    else:
        msg['Body'] = body

    msg.attach(MIMEText(msg['Body'], 'html'))
    connection.sendmail(msg['From'], to.split(',') + cc.split(',') + bcc.split(','), msg.as_string())
    del msg

def disconnect():
    global connection
    connection = None