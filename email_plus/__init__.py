import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:

    def check_email(self, email):
        regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        if (re.search(regex, email)):   #return true if it is in email format
            return True
        else:
            return False
            

    def send_email(self, to_email, mnem):
        email = "nobodycares2997@gmail.com"
        password = "!123Nobody@Cares123!"
        subject = "IronGate Account Activation"
        message = """\
				<<html>
					<head></head>
					<body>
						<p>Dear user,<br>
						Here is the Mnemonic Phrase you need to activate your account {to_email}:<br><br>
						<b>{mnem}</b><br><br>
						<u>DO NOT LOSE THIS EMAIL.</u> The mnemonic phrase is the only way to recover your account!<br>
						</p>
					</body>
				</html>
				""".format(to_email=to_email, mnem=mnem)
        msg = MIMEMultipart()
        msg["From"] = email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        try:
            server.sendmail(email, to_email, text)
        finally:
            server.quit()
