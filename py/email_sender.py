import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviar_email(oportunidades):
    remetente = "noticiasppps@gmail.com"
    senha = "soiq wcda exdt ayns"  # senha de app do gmail

    destinatario = "andre.mello@engeform.com.br"

    # monta texto do email
    corpo = "Novas oportunidades:\n\n"

    for op in oportunidades:
        corpo += f"{op.get('titulo')}\n"
        corpo += f"{op.get('link')}\n\n"

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = "Radar PPP - Novas oportunidades"

    msg.attach(MIMEText(corpo, "plain"))

    # envia
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)

    print("📧 Email enviado com sucesso")