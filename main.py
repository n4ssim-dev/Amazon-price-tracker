import smtplib
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
AMAZON_URL = os.getenv("AMAZON_URL")
my_email = os.getenv('my_email')
to_email = os.getenv('to_email')
password = os.getenv('password')

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept-Language" : "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3"
}

response = requests.get(url=AMAZON_URL,headers=headers)

if response.status_code == requests.codes.ok:
    soup = BeautifulSoup(response.text, "html.parser")

    price_whole = (soup.find("span",class_="a-price-whole")).getText().replace(",","")
    price_fraction = (soup.find("span",class_="a-price-fraction")).getText()
    article_name = (soup.find("span",class_="a-size-large product-title-word-break")).getText()
    full_price = int(price_whole) + (int(price_fraction) * 0.10)

    if price_whole and price_fraction:
        price = f"${full_price}"
        price_limit = 500
        if full_price < price_limit:
            mail_message = f"Subject:Notification article Amazon \n\nLe prix de :\n\n {article_name} \n\n est descendu en dessous de {price_limit} \n\nCordialement,\nToi même ;)"
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email,password=password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=to_email,
                    msg=mail_message.encode('utf-8')
                )
        else:
            print(f"Pas d'envoi pour ajourd'hui, le prix de : {article_name} est de ${full_price}")
    else:
        print("Aucun prix n'a été trouvé")
else:
    print(f"Erreur : {response.status_code}: Impossible de récolter les informtations de la page :/")
