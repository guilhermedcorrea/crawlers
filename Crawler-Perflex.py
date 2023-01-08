from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import lxml.html as parser
import requests
import csv
import time
import re
import unidecode
import json
from urllib.parse import urlsplit, urljoin


def extract(driver):
    cod = driver.find_element_by_id("cod_prod").text
    try:
        nome = driver.find_elements_by_xpath(
            "//div[@id='descr_prod']/font[2]")[0].text
    except IndexError as e:
        nome = "Not Found"
    try:
        linha = driver.find_elements_by_xpath(
            "//div[@id='descr_prod']/font[3]")[0].text
    except IndexError as e:
        linha = "Not Found"

    try:
        desc = driver.find_elements_by_xpath(
            "//div[@id='descr_prod']/font[4]")[0].text
    except IndexError as e:
        desc = "Not Found"

    EspList = dict(Codigo=cod, Nome=nome, Descrição=desc, Linha=linha)

    img = driver.find_elements_by_xpath("//div[@id='thumb']/div//img")
    imgcont = 1
    for x in img:
        EspList["Imagem "+str(imgcont)] = x.get_attribute("src")
        imgcont += 1

    driver.execute_script(
        "document.getElementsByClassName('myButton')[0].click()")

    return(EspList)


class EcommerceSpider(object):
    def __init__(self, start_url):
        self.items = []
        self.start_url = start_url
        self.key = []
        self.contar = ["1", "2", "3", "4", "5", "6"]
        self.filename = "Perflex.csv"
        self.errors = 0

    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    self.errors += 1
                else:
                    self.key.append(check)

    def save_items(self):
        self.create_dict()
        with open(self.filename, 'w') as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=self.key, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


crawler = EcommerceSpider(
    "http://www.perflex.com.br/2016/produtos.asp?do=0&cd=")
driver = webdriver.Chrome()
try:
    for x in crawler.contar:
        url = crawler.start_url + x
        print(url)
        driver.get(url)
        time.sleep(5)
        cats = driver.find_elements_by_xpath("//div[@id='page']/div/a")
        categorias = len(cats)
        catcont = 0
        time.sleep(5)

        while catcont != categorias:
            driver.get(url)
            time.sleep(5)
            cats = driver.find_elements_by_xpath("//div[@id='page']/div/a")
            cats[catcont].click()
            time.sleep(5)
            cats = driver.find_elements_by_xpath("//div[@id='page']/div/a")
            produtos = len(cats)
            prodcont = 0
            while prodcont != produtos:
                time.sleep(5)
                cats = driver.find_elements_by_xpath("//div[@id='page']/div/a")
                cats[prodcont].click()
                prodcont += 1
                time.sleep(5)
                crawler.items.append(extract(driver))

            catcont += 1

        crawler.save_items()

except KeyboardInterrupt as e:
    crawler.save_items()

print(categorias)
print(produtos)
