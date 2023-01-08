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

# Page Down       : https://stackoverflow.com/questions/21006940/how-to-load-all-entries-in-an-infinite-scroll-at-once-to-parse-the-html-in-pytho
# Infinite Scroll : https://michaeljsanders.com/2017/05/12/scrapin-and-scrollin.html


class Product(object):
    def __init__(self):
        self.links = {}
        self.start = "https://www.google.com"
        self.ean = []
        self.nome = []
        self.filename = time.strftime("%b.%d-%X").replace(":", ".")
        self.infos = []

    def CSVREADER(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.nome.append(row["Nome"])
                self.links[row["Nome"]] = row["Link"]


def blank(texto):
    teste = " ".join(texto.split())
    return teste


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


def randoms(ranges):
    ranges = random.randint(1, ranges)
    return ranges


driver = webdriver.Chrome(
    'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe')

Produto = Product()
Produto.CSVREADER("Avant-Urls.CSV")

try:
    for nome in Produto.nome:
        driver.get(Produto.links[nome])
        time.sleep(1)
        names = driver.find_elements_by_xpath(
            "//div[@class='l7AxXb']")
        for name in names:
            if 'GTIN' in name.text:
                ean = name.text.replace("GTIN", "")

        infos = dict(EAN=ean, Nome=nome, Link=Produto.links[nome])
        Produto.infos.append(infos)

    Produto.filename = Produto.filename + " - " +\
        time.strftime("%b.%d-%X").replace(":", ".")+".csv"
    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(
            f, fieldnames=infos.keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.infos)

except KeyboardInterrupt:
    Produto.filename = Produto.filename + " - " +\
        time.strftime("%b.%d-%X").replace(":", ".")+".csv"
    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(
            f, fieldnames=infos.keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.infos)

driver.quit()
