import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

# SESSAO PARA A CHECAGEM DE MUDANÇA DE STATUS E LAST UPDATE DO SITE
url = "https://immi.homeaffairs.gov.au/what-we-do/whm-program/status-of-country-caps?utm_source=chatgpt.com"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

tabela = soup.find("table")
status_brasil = None

if tabela:
    linhas = tabela.find_all("tr")
    for linha in linhas:
        colunas = linha.find_all("td")
        if colunas and "Brazil" in colunas[0].text:
            status_brasil = [coluna.text.strip() for coluna in colunas][1]
            status_brasil = status_brasil.replace('\u200b', '').strip()
            break

text_last_upd = None
for div in soup.find_all("div"):
    if "Last updated" in div.text:
        text_last_upd = div.text.strip() 
        break
match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", text_last_upd)
if match:
    date_str = match.group(0)
    last_upd_data = datetime.strptime(date_str, "%d/%m/%Y")
    # print(last_upd_data)

# SESSAO PARA O ENVIO DE EMAIL CASO HAJA A MUDANÇA DE STATUS
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()  

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PSW = os.getenv("PSW_EMAIL")

def send_email(subject, body, to_email):
    from_email = EMAIL_SENDER
    psw = EMAIL_PSW
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(from_email, psw)
        server.sendmail(from_email, [to_email], msg.as_string())
list_status = ["paused", "closed"]

if any(s in status_brasil for s in list_status):
    print("Status it is 'paused' or 'closed'")
else:
    for email in os.getenv("LIST_EMAIL_RECIVER").split(","):
        print(email)
        print("EMAIL SENT")
        send_email(
            "Change in Australia Visa!!",
            f'New status: {status_brasil} \nLast update: {last_upd_data}\n'
            'Go to: https://online.immi.gov.au/ola/app and secure your spot',
            email
        )
