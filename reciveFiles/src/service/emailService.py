import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()
import os


def sendEmail(code: int, emailDestination: str) -> None:
    try:
        sender_email = os.environ["EMAIL_USER_NAME"]
        sender_password = os.environ["EMAIL_PASSWORD"]
        recipient_email = emailDestination
        subject = "Alteração de senha - easy stream"
        body = generateHTML(code)

        html_message = MIMEText(body, "html")
        html_message["Subject"] = subject
        html_message["From"] = sender_email
        html_message["To"] = recipient_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, html_message.as_string())
    except Exception as r:
        raise ValueError(
            f"Erro ao enviar email para {emailDestination}"
        )


def generateHTML(code: int) -> str:

    body = f"""
    <html>
    <head>
    <style>
        {generateCSS()}
    </style>
    </head>
      <body>
        <div id="container">
            <h3>Código para alterar a senha</h3>
            <div id="code">{code}</div>
            <p class="info">Este código é válido por 5 minutos.</p>
        </div>
      </body>
    </html>
    """
    return body


def generateCSS() -> str:
    css = """    
            body {
      font-family: 'Roboto', sans-serif;
      background-color: #f9f9f9;
      display: flex;

      align-items: center;
      flex-direction: column;
      height: 100vh;
      margin: 0;
    }

    #container {
      text-align: center;
      background: white;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    h1 {
      color: #333;
      margin-bottom: 20px;
    }

    #code {
      font-size: 2em;
      color: black;
      margin-bottom: 10px;
      font-weight: bold;
    }

    .info {
      color: #666;
      font-size: 0.9em;
    }
    """
    return css
