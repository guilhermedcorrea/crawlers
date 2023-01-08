from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import lxml.html as parser
import requests
import csv
import random
import decimal
from re import sub
from decimal import Decimal
from urllib.parse import urlsplit, urljoin, urlparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path


class Product(object):
    def __init__(self):
        self.filename = "GSHOP - " + \
            time.strftime("%b.%d-%X").replace(":", ".") + ".csv"
        self.vtex = []
        self.name = []
        self.ref = {}
        self.price = []
        self.items = []
        self.ID = []
        self.links = {}
        self.custo = {}
        self.marca = {}

    def CSVREADER(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.ID.append(row["ID"])
                self.links[row["ID"]] = row["Link"]
                self.custo[row["ID"]] = row["Custo"]
                self.ref[row["ID"]] = row["Nome"]
                self.marca[row["ID"]] = row["Marca"]

    def sugerido(self, preco):

        suggest = percentage(1, float(PC))

        suggest = Decimal(suggest).quantize(
            Decimal('1.00'), rounding=decimal.ROUND_DOWN)

        total = PC - suggest
        print(total)

    # calculo de margem  (PC - custo)/PC

    def margem(self, PC, ID):  # pc = Custo Player
        a = PC.replace(".", "*")
        a = a.replace(",", ".")

        value = Decimal(sub(r'[^\d.]', '', a)).quantize(
            Decimal('1.00'), rounding=decimal.ROUND_DOWN)

        value2 = Decimal(sub(r'[^\d.]', '', self.custo[ID])).quantize(
            Decimal('1.00'), rounding=decimal.ROUND_DOWN)

        margem = (value - value2)/value * 100
        margem = Decimal(margem).quantize(
            Decimal('1.00'), rounding=decimal.ROUND_DOWN)

        return margem

    def send_email(self, filee):  # filee = NOME DO ARQUIVO A SER ENVIADO
        email = 'ricardo.vieira3101@gmail.com'
        password = 'C4mV3nus'
        send_to_email = 'ricardo.vieira3101@gmail.com'
        subject = 'Precificador GSHOP'
        message = 'Não esquecer de alterar a coluna CODREF para numero e remover as casas decimais'
        file_location = filee

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


def percentage(percent, whole):
    return (percent * whole) / 100.0


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
    driver = webdriver.Chrome(
        'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe')

    Produto = Product()
    Produto.CSVREADER("teste-id.CSV")

    for ID in Produto.ID:
        Nome = Produto.ref[ID]
        Marca = Produto.marca[ID]
        Custo = Produto.custo[ID]
        Produto.custo[ID] = Produto.custo[ID].replace(".", "*")
        Produto.custo[ID] = Produto.custo[ID].replace(",", ".")
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
        while lastcont < len(Produto.name):
            PC = Produto.price[lastcont]
            margem = Produto.margem(PC, ID)
            margem = str(margem) + " %"
            suggest = Produto.sugerido(PC)
            bleh = dict(
                CODREF=ID, Player=Produto.name[lastcont], Price=Produto.price[lastcont], Nome=Nome, Marca=Marca, Custo=Custo, Margem=margem, Sugerido=sugerido)
            Produto.items.append(bleh)
            lastcont += 1
    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=bleh.keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.items)
    Produto.send_email(Produto.filename)

except KeyboardInterrupt:
    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=bleh.keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.items)
    Produto.send_email(Produto.filename)
