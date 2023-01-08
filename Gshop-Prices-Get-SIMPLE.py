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
from urllib.parse import urlsplit, urljoin, urlparse


GSHOP = "GSHOP4"


class Product(object):
    def __init__(self):
        self.filename = GSHOP + time.strftime("%d-%b").replace(":", ".")+".csv"
        self.vtex = []
        self.name = []
        self.price = []
        self.items = []
        self.ID = []
        self.links = {}

    def CSVREADER(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.ID.append(row["ID"])
                self.links[row["ID"]] = row["Link"]


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
        r'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe')

    Produto = Product()
    Produto.CSVREADER(GSHOP+".csv")

    for ID in Produto.ID:
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
            bleh = dict(
                CODREF=ID, Player=Produto.name[lastcont], Price=Produto.price[lastcont])
            Produto.items.append(bleh)
            lastcont += 1

    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=bleh.keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.items)

except KeyboardInterrupt:
    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=bleh.keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.items)


driver.quit()
