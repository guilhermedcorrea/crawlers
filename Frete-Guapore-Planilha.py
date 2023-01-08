from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import lxml.html as parser
import requests
import csv
from urllib.parse import urlsplit, urljoin

# Page Down       : https://stackoverflow.com/questions/21006940/how-to-load-all-entries-in-an-infinite-scroll-at-once-to-parse-the-html-in-pytho
# Infinite Scroll : https://michaeljsanders.com/2017/05/12/scrapin-and-scrollin.html


class Product(object):
    def __init__(self):
        self.filename = "Teste-Fretes.csv"
        self.CEP = []
        self.city = {}
        self.est = {}
        self.prod = []
        self.links = {}
        self.QTD = ["5"]
        self.Piso = ["30"]
        self.CodRef = []

    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    print("Duplicado")
                else:
                    self.key.append(check)

    def CSVREADER(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.CEP.append(row["CEP"])
                self.city[row["CEP"]] = row["Municipio"]
                self.est[row["CEP"]] = row["UF"]

    def CSVREADER2(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.prod.append(row["Nome"])
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


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')

driver = webdriver.Chrome(
    'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe', chrome_options=chrome_options)
Produto = Product()
Produto.CSVREADER("testeceps.csv")
Produto.CSVREADER2("produtos-ceps.csv")
teste = []
fieldnames = ["Nome", "CEP", "QTD", "Transportadora", "Preço", "Prazo"]
try:
    for nome in Produto.prod:
        driver.get(Produto.links[nome])
        frete = driver.find_element_by_id('txtCalculaFreteProduto')
        for cep in Produto.CEP:
            print(cep)
            frete.click
            time.sleep(1)
            frete.send_keys(Keys.HOME)
            frete.send_keys(cep)
            time.sleep(2)
            if "(PISO)" in nome:
                for QTD in Produto.Piso:
                    qtd = driver.find_element_by_id("quantidadeCx")
                    qtd.clear()
                    qtd.send_keys(QTD)
                    time.sleep(2)
                    clica = driver.find_element_by_id('btnCalculaFreteProduto')
                    clica.send_keys(Keys.ENTER)

                    time.sleep(4)
                    price = driver.find_elements_by_xpath(
                        "//table[@class='resultado-frete']/tbody/tr")
                    error = driver.find_element_by_class_name("errosFrete")
                    error = error.get_attribute("style")
                    if not("display: block;" in error):
                        for x in price:
                            if("\n" in x.text):
                                transportadora, preco, prazo = x.text.split(
                                    "\n")
                                bleh = dict(Nome=nome, CEP=cep, QTD=QTD, Transportadora=transportadora,
                                            Preço=preco, Prazo=prazo)
                                teste.append(bleh)
            else:
                for QTD in Produto.QTD:
                    qtd = driver.find_element_by_class_name('qtdProduto')
                    qtd.clear()
                    qtd.send_keys(QTD)
                    time.sleep(2)
                    clica = driver.find_element_by_id('btnCalculaFreteProduto')
                    clica.send_keys(Keys.ENTER)

                    time.sleep(4)
                    price = driver.find_elements_by_xpath(
                        "//table[@class='resultado-frete']/tbody/tr")

                    error = driver.find_element_by_class_name("errosFrete")
                    error = error.get_attribute("style")
                    if not("display: block;" in error):
                        for x in price:
                            if("\n" in x.text):
                                transportadora, preco, prazo = x.text.split(
                                    "\n")
                                bleh = dict(Nome=nome, CEP=cep, QTD=QTD, Transportadora=transportadora,
                                            Preço=preco, Prazo=prazo)
                                teste.append(bleh)
                    else:
                        bleh = dict(Nome=nome, CEP=cep, QTD=QTD, Transportadora="ERRO",
                                    Preço="ERRRO", Prazo="ERRO")
                        teste.append(bleh)

    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(
            f, fieldnames=fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(teste)
except KeyboardInterrupt:
    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(teste)

print(teste)
time.sleep(130)

driver.quit()
