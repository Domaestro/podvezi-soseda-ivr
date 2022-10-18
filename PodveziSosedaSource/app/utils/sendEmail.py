from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl

from config import Config

def send_link(link, to):
    msg = MIMEMultipart()

    domain = Config.domain
    password = Config.email_password
    msg['From'] = Config.email_login
    msg['Subject'] = "Код подтвержения - Подвези соседа!"

    template = f'''
    <html>
    <head>
        <style>
            .content 
        </style>
    </head>
    <body>
        <div class="content" style="width: 440px; text-align: center; ">
            <h2>Поздравляем с регистрацией на <br> Подвези соседа!</h2>
            <p style="font-size: medium; margin: 15px 0px 15px 0px; ">Чтобы полноценно пользоваться сервисом, осталось только подтвердить аккаунт. <br> Нажмите на кнопку ниже<br><br><br></p>
            <a href="{domain}{ link }" style="margin-top: 10px; padding: 15px; border-radius: 10px; background-color: #4572ed;color: white; font-size: large; text-decoration: none;">Подтвердить</a>
            <p style="font-size: smaller; margin-top: 20px"><br><br><br><br>Если вы не регистрировались в "Подвези соседа!" - игнорируйте это письмо</p>
            <p style="font-size: smaller">Письмо сгенерировано автоматически, не отвечайте на него</p>
        </div>
        <p style="font-size: smaller; margin-top: 20px"><br><br><br><br>Если вы не можете нажать на кнопку, перейдите по ссылке: {domain}{ link }</p>
    </body>
    </html>
    '''

    msg.attach(MIMEText(template, 'html'))

    context = ssl.create_default_context()
    #context = ssl._create_unverified_context() # на случай, если ssl-сертификат будет просрочен
    with smtplib.SMTP_SSL("mail.kerpan.ru", 465, context=context) as server:
        server.login(msg['From'], password)
        server.sendmail(msg['From'], to, msg.as_string())
        print('mail successfully sent')