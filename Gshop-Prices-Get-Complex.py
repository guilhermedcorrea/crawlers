from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import time
import lxml.html as parser
import requests
import csv
import random
import ftplib
from urllib.parse import urlsplit, urljoin, urlparse


GSHOP = "GSHOP5"

fieldnames = ["IDENTIFICADOR", "SKU", "Lojas Guaporé",
              "Player 1", "Price 1", "Player 2", "Price 2"]


class Product(object):
    def __init__(self):
        self.filename = GSHOP + " - " + \
            time.strftime("%d-%b").replace(":", ".")+".csv"
        self.name = []
        self.price = []
        self.items = []
        self.ID = []
        self.links = {}
        self.min = {}
        self.sku = {}
        self.user = 'Ricardo'
        self.password = 'r!c4rdã0_2018_v1d4L0ka'
        self.ftp = 'server.lojasguapore.com.br'
        self.directory = "/Crawler"
        self.path = "C:\\Temp\\Projetos\\Python\\Gshop-Crawlers\\"+self.filename

    def ftp_send(self):
        session = ftplib.FTP(self.ftp, self.user, self.password)
        session.cwd(self.directory)
        file = open(self.filename, 'rb')                  # file to send
        session.storbinary('STOR '+self.filename, file)     # send the file
        file.close()                                    # close file and FTP
        session.quit()

    def CSVREADER(self, filename):
        path = "C:\\Temp\\Projetos\\Python\\Gshop-Crawlers\\"+filename
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.ID.append(row["ID"])
                self.links[row["ID"]] = row["URL"]
                self.sku[row["ID"]] = row["SKU"]

    def send_email(self):
        email = 'ricardo.vieira3101@gmail.com'
        password = 'C4mV3nus'
        send_to_email = 'crawler@lojasguapore.com.br'
        subject = self.filename
        message = 'PRECIFICADOR ' + time.strftime("%d-%b")
        file_location = self.path

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = send_to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        filename = os.path.basename(file_location)
        attachment = open(file_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit()


def randoms(ranges):
    ranges = random.randint(1, ranges)
    return ranges


def scrollpage(driver):
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False

    while(match == False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True


def blank(texto):
    teste = " ".join(texto.split())
    return teste


try:
    driver = webdriver.Chrome()

    Produto = Product()
    Produto.CSVREADER(GSHOP+".csv")

    for ID in Produto.ID:
        bleh = {}
        Produto.min = {}
        driver.get(Produto.links[ID])
        time.sleep(0.5)
        names = driver.find_elements_by_xpath(
            "//span[@class='os-seller-name-primary']/a")

        Produto.name = []
        Produto.price = []

        for nam in names:
            Produto.name.append(nam.text)

        prices = driver.find_elements_by_xpath(
            "//span[@class='tiOgyd']")

        for pric in prices:
            Produto.price.append(pric.text)

        lastcont = 0

        player1 = ""
        player2 = ""
        guapore = "Lojas Guaporé"

        bleh = dict(IDENTIFICADOR=ID, SKU=Produto.sku[ID])

        while lastcont < len(Produto.name):
            Player = Produto.name[lastcont]
            Price = Produto.price[lastcont]

            if(Player == guapore):
                bleh["Lojas Guaporé"] = Price
            else:
                Produto.min[Player] = float(Price.replace(
                    "R$ ", "").replace(".", "").replace(",", "."))

            lastcont += 1

        if(len(Produto.min) == 1):
            menor = min(Produto.min.keys(), key=(lambda k: Produto.min[k]))
            bleh["Player 1"] = menor
            bleh["Price 1"] = "R$ " + str(Produto.min[menor]).replace(".", ",")
        elif(len(Produto.min) > 1):
            menor = min(Produto.min.keys(), key=(lambda k: Produto.min[k]))
            bleh["Player 1"] = menor
            bleh["Price 1"] = "R$ " + str(Produto.min[menor]).replace(".", ",")

            Produto.min.pop(menor, None)
            menor = min(Produto.min.keys(), key=(lambda k: Produto.min[k]))

            bleh["Player 2"] = menor
            bleh["Price 2"] = "R$ " + str(Produto.min[menor]).replace(".", ",")

        Produto.items.append(bleh)

    with open(Produto.path, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.items)

except KeyboardInterrupt:
    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.items)


driver.quit()

Produto.send_email()
# Produto.ftp_send()
