from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid

from flask import Flask, request, Response
import smtplib
from werkzeug.exceptions import BadRequestKeyError

from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)


@app.route('/email/post', methods=['POST'])
def post_email():

    try:
        json_file = request.get_json(force=False)
        smtp = json_file['smtp']
        name = json_file['data'][0]['name']
        phone = json_file['data'][1]['phone']
        login = json_file['login']
        passwd = json_file['password']
        to = json_file['email']
        try:
            msg = MIMEMultipart()
            msg['Message-ID'] = make_msgid()
            msg['Subject'] = f'Новый лид!!! имя {name} , номер телефона {phone}'
            msg['From'] = login
            msg['To'] = to
            s = smtplib.SMTP_SSL(smtp, 465)
            s.login(login, passwd)
            s.sendmail(login, to, msg.as_string())
            s.quit()
            return Response("Сообщение отправлено", 201)
        except:
            Response("Сообщение  не отправлено", 404)

    except BadRequestKeyError:
        return Response("Пустое значение", 400)

