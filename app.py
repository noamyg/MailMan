from werkzeug.utils import redirect, secure_filename

from controllers import smtpController
from controllers import templateController
from flask import Flask, request, abort, json, render_template, send_from_directory, send_file, flash
from flask_restful import Resource, Api
from flask_cors import CORS
from validate_email import validate_email
import sys
import os
import logging

app = Flask(__name__, template_folder='views')
CORS(app)
api = Api(app)

file_handler = logging.FileHandler('mailMan.console.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('mailman_logger')

if len(sys.argv) < 2 or smtpController.connect(sys.argv[1]) is not True:
    logger.error("You must supply a SMTP connection name as a parameter (using a valid connection from config.xml)")
    logger.error("If running as NSSM service, use nssm.exe edit to add server name as parameter")
    sys.exit(2)


class SendMail(Resource):
    def post(self):
        logger.info('Got a request to send mail.')
        body = request.get_json()
        to = body.get("to")
        cc = body.get("cc")
        if not to and not cc:
            logger.warning('"to" or "cc" attributes are missing')
            abort(400, 'You must supply either a "to" or "cc" attributes')
        if to:
            for toAddress in to.split(','):
                if not validate_email(toAddress):
                    logger.warning('Invalid "to" attribute')
                    abort(400, '"{}" is not a valid email address.'.format(toAddress))
        if cc:
            for ccAddress in cc.split(','):
                if not validate_email(ccAddress):
                    logger.warning('Invalid "cc" attribute')
                    abort(400, '"{}" is not a valid email address.'.format(ccAddress))
        template = 'templates/{}.html'.format(body.get("t"))
        logger.info('Recipients: {}, CCRecipients: {}, Template: {}'.format(to, cc, body.get("t")))
        subjectParams = body.get("sp")
        bodyParams = body.get("bp")
        smtpController.sendMail(to, cc, template, bodyParams, subjectParams)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/')
def render_static_home():
    return render_template("index.html")

@app.route('/templates')
def render_static_templates():
    templates = templateController.getAllTemplates('./templates')
    table = ""
    for t in templates:
        table+='\t\t<tr><td><a href="{0}">{1}</a></td></tr>\n'.format('/templates/'+t, t)
    return render_template("templates.html").format(table)

@app.route('/contact')
def render_static_contact():
    return render_template("contact.html")


@app.route("/templates/<path>")
def downloadTemplate (path = None):
    if path is None:
        abort(400)
    try:
        return send_file("templates/"+path, as_attachment=True)
    except Exception as e:
        logger.log.exception(e)
        abort(400)


@app.route('/templateUploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join('./templates/', filename))
        return redirect('/templates')

api.add_resource(SendMail, '/sendMail')

if __name__ == '__main__':
    app.run(threaded=False ,host='0.0.0.0')