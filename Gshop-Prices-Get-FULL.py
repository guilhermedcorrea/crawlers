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


class Product(object):
    def __init__(self):
        self.filename = None
        self.vtex = []
        self.name = []
        self.price = []
        self.items = []
        self.ID = []
        self.links = {}


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


driver = webdriver.Chrome(
    'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe')

Produto = Product()

for ID in Produto.ID:
    driver.get(Produto.links[ID])
    RND = randoms(6)
    time.sleep(RND)
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

        # IHA = verificador de next page
    IHA = 0

    while IHA == 0:
        test = driver.find_elements_by_xpath(
            "//div[contains(@class ,'jfk-button-disabled') and @id='online-next-btn']")
        test = len(test)
        if test < 1:
            driver.find_elements_by_id('online-next-btn')[0].click()

            RND = randoms(3)
            time.sleep(RND)

            names2 = driver.find_elements_by_xpath(
                "//span[@class='os-seller-name-primary']/a")

            for nam2 in names2:
                Produto.name.append(nam2.text)

            prices2 = driver.find_elements_by_xpath(
                "//span[@class='tiOgyd']")

            for pric2 in prices2:
                Produto.price.append(pric2.text)
            time.sleep(2)
        else:
            IHA = 1
            print("ACABOU")

    lastcont = 0
    while lastcont < len(Produto.name):
        bleh = dict(
            CODREF=ID, Player=Produto.name[lastcont], Price=Produto.price[lastcont])
        Produto.items.append(bleh)
        lastcont += 1

Produto.endtime = time.strftime("%b.%d-%X").replace(":", ".")
Produto.filename = Produto.endtime+".csv"

with open(Produto.filename, 'w', encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, fieldnames=bleh.keys(), delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(Produto.items)
