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
        self.links = []
        self.start = "https://www.google.com"
        self.CodRef = []
        self.filename = "Tramo.csv"

    def CSVREADER(self):
        with open(self.filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.CodRef.append(row["ID"])


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
Produto.CSVREADER()
url = "https://www.google.com/shopping?hl=pt-BR"
driver.get(url)
cont = 0
for ID in Produto.CodRef:
    # Executa a pesquisa do produto (CODREF PRODUTO)
    input_element = driver.find_element_by_name("q")
    input_element.clear()

    input_element.send_keys(ID)
    print("Current : " + ID)
    input_element.submit()
    RND = randoms(4)
    time.sleep(RND)
    cont += 1
    existe = len(driver.find_elements_by_xpath(
        "//li[contains(text(),'Certifique-se')]"))
    if(existe == 0):
        try:
            link = driver.find_element_by_xpath(
                '//a[contains(@href, "shopping/product")]')
            link = link.get_attribute("href")
            link = urlparse(link).path.split("/online")
            link = Produto.start + link[0]
        except:
            link = "Not Found"
    else:
        link = "Not Found"
        print(ID + " Not Found")

    dicionario = dict(ID=ID, URL=link)
    Produto.links.append(dicionario)

print(Produto.links)

with open("Gshop-Remendo4.csv", 'w') as f:
    fieldnames = ["CODREF", "URL"]
    dict_writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(Produto.links)

print(cont)
# driver.quit()
