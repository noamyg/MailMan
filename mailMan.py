from werkzeug.utils import redirect, secure_filename
from controllers import smtpController
from controllers import templateController
from flask import Flask, request, abort, json, render_template, send_file
from flask_restful import Resource, Api
from flask_cors import CORS
from validate_email import validate_email
import traceback
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

if len(sys.argv) < 2:
    logger.error("You must supply a SMTP connection name as a parameter (using a valid connection from config.xml)")
    logger.error("If running as NSSM service, use nssm.exe edit to add server name as parameter")
    sys.exit(2)

if smtpController.connect(sys.argv[1]) is not True:
   logger.error("Connection not established. Please check your connection to server defined in config.xml")
   sys.exit(2)

port = 5000
if len(sys.argv) > 2:
    port = int(sys.argv[2])


class SendMail(Resource):
    def post(self):
        logger.info('Got a request to send mail.')
        body = request.get_json()
        to = body.get("to") if body.get("to") else ""
        cc = body.get("cc") if body.get("cc") else ""
        bcc = body.get("bcc") if body.get("bcc") else ""
        if not to and not cc and not bcc:
            logger.warning('"to", "cc" or "bcc" attributes are missing')
            abort(400, 'You must supply either a "to", "cc" or "bcc" attributes')
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
        if bcc:
            for bccAddress in bcc.split(','):
                if not validate_email(bccAddress):
                    logger.warning('Invalid "bcc" attribute')
                    abort(400, '"{}" is not a valid email address.'.format(bccAddress))
        template = 'templates/{}.html'.format(body.get("t"))
        logger.info('Recipients: {}, CCRecipients: {}, BCCRecipients {}, Template: {}'.format(to, cc, bcc, body.get("t")))
        subjectParams = body.get("sp")
        bodyParams = body.get("bp")
        try:
            smtpController.sendMail(to, cc, bcc, template, bodyParams, subjectParams)
        except Exception as err:
            logger.error(traceback.format_exc())
            return err.strerror, 500
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/')
def render_static_home():
    return render_template("index.html", page="index", port=port)


@app.route('/templates')
def render_static_templates():
    templates = templateController.getAllTemplates('./templates')
    return render_template("templates.html", templates=templates, page="templates")


@app.route('/contact')
def render_static_contact():
    return render_template("contact.html", page="contact")


@app.route('/login')
def render_static_login():
    return render_template("login.html", page="login")


@app.route("/templates/<path>")
def donwload_template(path = None):
    if path is None:
        abort(400)
    try:
        return send_file("templates/"+path, as_attachment=True)
    except Exception as e:
        logger.log.exception(e)
        abort(400)


ALLOWED_EXTENSIONS = set(['html'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/templateUploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join('./templates/', filename))
        else:
            return abort(400, 'Was that really and .HTML file?')
        return redirect('/templates')


@app.route('/deleteTemplate/<string:file_name>/')
def delete_file(file_name):
    os.remove(os.path.join('./templates/', file_name))
    return redirect('/templates')


api.add_resource(SendMail, '/sendMail')


if __name__ == '__main__':
    if os.path.isfile('./certificates/server.crt') and os.path.isfile('./certificates/server.key'):
        logger.info("Certificates found. Running with SSL context")
        context = ('./certificates/server.crt', './certificates/server.key')
        app.run(threaded=False, host='0.0.0.0', port=port, ssl_context=context)
    else:
        logger.info("Did not find any certificates. Running as HTTP")
        app.run(threaded=False, host='0.0.0.0', port=port)
