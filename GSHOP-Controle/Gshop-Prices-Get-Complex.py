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
fieldnames = ["IDENTIFICADOR", "Player 1", "Price 1", "Player 2", "Price 2"]


class Product(object):
    def __init__(self):
        self.filename = GSHOP + time.strftime("%d-%b").replace(":", ".")+".csv"
        self.name = []
        self.price = []
        self.items = []
        self.ID = []
        self.links = {}
        self.min = {}

    def CSVREADER(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.ID.append(row["ID"])
                self.links[row["ID"]] = row["URL"]


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

        bleh = dict(IDENTIFICADOR=ID)

        while lastcont < len(Produto.name):
            Player = Produto.name[lastcont]
            Price = Produto.price[lastcont]

            if(Player == guapore):
                bleh["Lojas Guaporé"] = Price
            else:
                Produto.min[Player] = Price

            lastcont += 1

        if(len(Produto.min) == 1):
            print("None")
        elif(len(Produto.min) > 1):
            menor = min(Produto.min.keys(), key=(lambda k: Produto.min[k]))

            bleh["Player 1"] = menor
            bleh["Price 1"] = Produto.min[menor]
            Produto.min.pop(menor, None)
            menor = min(Produto.min.keys(), key=(lambda k: Produto.min[k]))

            bleh["Player 2"] = menor
            bleh["Price 2"] = Produto.min[menor]

        Produto.items.append(bleh)

    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.items)

except KeyboardInterrupt:
    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.items)


driver.quit()
