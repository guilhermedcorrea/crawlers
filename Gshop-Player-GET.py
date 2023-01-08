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
        self.filename = "sink.csv"
        self.vtex = []
        self.file = "g-sink.csv"
        self.name = {}
        self.ref = {}
        self.price = []
        self.items = []
        self.ID = []
        self.links = {}
        self.custo = {}
        self.marca = {}
        self.url = []

    def CSVREADER(self):
        with open(self.filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.ID.append(row["ID"])
                self.links[row["ID"]] = row["URL"]
        print(self.ID)


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
    driver = webdriver.Chrome(
        'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe')

    Produto = Product()
    Produto.CSVREADER()

    for ID in Produto.ID:
        cont = 0
        print(Produto.links[ID])
        driver.get(Produto.links[ID])
        time.sleep(0.5)
        names = driver.find_elements_by_xpath(
            "//span[@class='os-seller-name-primary']/a")
        price = driver.find_elements_by_xpath("//span[@class='tiOgyd']")
        Produto.name = []
        Produto.price = []

        for nam in names:
            bleh = dict(
                CODREF=ID, Player=nam.text, URL=nam.get_attribute('href'), Preço=price[cont].text)

            cont += 1
            Produto.items.append(bleh)

    with open(Produto.filename, 'w') as f:
        print(Produto.items)
        dict_writer = csv.DictWriter(f, fieldnames=bleh.keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.items)

except KeyboardInterrupt:
    with open(Produto.filename, 'w') as f:
        print(Produto.items)
        dict_writer = csv.DictWriter(f, fieldnames=bleh.keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.items)

driver.quit()
