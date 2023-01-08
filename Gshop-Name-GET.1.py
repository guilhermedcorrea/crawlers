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
        self.CodRef = []
        self.nome = []
        self.filename = time.strftime("%b.%d-%X").replace(":", ".")

    def CSVREADER(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.nome.append(row["ID"])


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


try:
    driver = webdriver.Chrome(
        'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe')

    Produto = Product()
    Produto.CSVREADER("AVANT-IDS.csv")
    url = "https://www.google.com/shopping?hl=pt-BR"
    driver.get(url)
    cont = 0

    for nome in Produto.nome:
        # Executa a pesquisa do produto (CODREF PRODUTO)

        RND = randoms(1)
        time.sleep(RND)
        input_element = driver.find_element_by_name("q")
        input_element.clear()
        input_element.send_keys(nome)
        print("Current : " + nome)
        input_element.submit()
        time.sleep(1)
        existe = len(driver.find_elements_by_xpath(
            "//li[contains(text(),'Certifique-se')]"))
        if(existe == 0):
            el = driver.find_elements_by_xpath("//body")[0]

            action = webdriver.common.action_chains.ActionChains(driver)
            time.sleep(1)
            action.move_to_element_with_offset(el, 370, 289)
            action.click()
            action.perform()
            try:
                link = driver.find_elements_by_xpath(
                    "//a[@class='_-by']")[0]
                textlink = link.get_attribute("href")
                textlink = urlparse(textlink).path.split("/online")[0]
                textlink = Produto.start + textlink
                Produto.links[nome] = textlink
            except IndexError as e:
                None
        else:
            Produto.links[nome] = "Nao Encontrado"

    Produto.filename += " "+time.strftime("%b.%d-%X").replace(":", ".")+".csv"

    with open(Produto.filename, 'w') as f:
        dict_writer = csv.writer(
            f, delimiter=';')
        for key, value in Produto.links.items():
            dict_writer.writerow([key] + [value])

except KeyboardInterrupt:
    Produto.filename += " "+time.strftime("%b.%d-%X").replace(":", ".")+".csv"
    with open(Produto.filename, 'w') as f:
        dict_writer = csv.writer(
            f, delimiter=';')
        for key, value in Produto.links.items():
            dict_writer.writerow([key] + [value])

driver.quit()
