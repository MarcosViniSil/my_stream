import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv
load_dotenv()
import os

def sendEmail(idVideo:str,status:str,message:str,emailDestination:str) -> None:
    try:
        sender_email =  os.environ["EMAIL_USER_NAME"] 
        sender_password = os.environ["EMAIL_PASSWORD"] 
        recipient_email = emailDestination
        subject = message
        body = generateHTML(idVideo,status,message)

        html_message = MIMEText(body, "html")
        html_message["Subject"] = subject
        html_message["From"] = sender_email
        html_message["To"] = recipient_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, html_message.as_string())
    except Exception as r:
        raise ValueError(f"Erro ao enviar email para {emailDestination} sobre video de id {idVideo}")

def generateHTML(idVideo:str,status:str,message:str) -> str:
    messageTitle = ""
    if status.endswith("❌"):
        messageTitle = "ocorreu um erro ao processar o vídeo"
    else:
        messageTitle = f"O vídeo de id {idVideo} foi processado e já está disponível"
    body = f"""
    <html>
    <head>
    <style>
        {generateCSS()}
    </style>
    </head>
      <body>
        <h1> {messageTitle} </h1>
        <div id="wrapTable">
        <table>
            <tr>
                <td>id vídeo</td>
                <td id="status">Status</td>
                <td>Mensagem</td>
            </tr>
            <tr>
                <td>{idVideo}</td>
                <td>{status}</td>
                <td>{message}</td>
            </tr>
        </table>
        </div>
      </body>
    </html>
    """
    return body

def generateCSS() -> str:
    css = """    
        #wrapTable{
            width:100%;
            display:flex;
            align-contents:center;
            justify-content:center;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            font-family: Arial, sans-serif;
            margin: 20px 0;
        }

        th {
            background-color: #f2f2f2;
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }

        td {
            border: 1px solid #ddd;
            padding: 8px;
        }

        tr:hover {
            background-color: #f5f5f5;
        }
    """
    return css