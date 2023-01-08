from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import lxml.html as parser
import requests
import csv
from urllib.parse import urlsplit, urljoin


class Product(object):
    def __init__(self):
        self.filename = "Fretes2.csv"
        self.CEP = ["13091120", "57540000"]
        self.infos = []
        self.nome = ["Carrinho 7", "Carrinho 10",
                     "Carrinho 6", "Carrinho 8", "Carrinho 9"]
        self.prod = [
            "https://www.lojasguapore.com.br/produto/misturador-monocomando-de-chuveiro-minimal-advance-c-78-2997-meber-125910"]
        self.links = {}
        self.QTD = ["1", "5", "10"]
        self.CodRef = []
        self.username = "ricardo@lojasguapore.com.br"
        self.password = "odra31cir"

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
                self.city[row["CEP"]] = row["Cidade"]
                self.est[row["CEP"]] = row["Estado"]

    def CSVREADER2(self, filename):
        self.prod = []
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.prod.append(row["Link"])

    def login(self, driver):
        email = driver.find_element_by_id("txtLoginEmail")
        email.send_keys(self.username)
        time.sleep(2)
        senha = driver.find_element_by_id("txtLoginPassword")
        senha.send_keys(self.password)
        login = driver.find_element_by_id("btnLogin").click()


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


Produto = Product()
for nome in Produto.nome:
    driver = webdriver.Chrome(
        'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe', chrome_options=chrome_options)
    Produto.CSVREADER2(nome+".csv")
    for link in Produto.prod:
        print(link)
        driver.get(link)

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "comprarProduto")))

        comprar = driver.find_element_by_css_selector(
            "a.bt.comprarProduto.btn-comprar")
        driver.execute_script(
            "document.querySelector('a.bt.comprarProduto.btn-comprar').click();")
        for QTD in Produto.QTD:

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "qtdCarrinho")))

            quantidade = driver.find_elements_by_xpath(
                "//input[@class='input qtdCarrinho']")

            for x in quantidade:
                x.send_keys(Keys.CONTROL, 'a')
                x.send_keys(QTD)
                time.sleep(4)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "btfinalizar")))

            finalizar = driver.find_element_by_css_selector(
                "input#btnFinalizarPedido2")
            driver.execute_script(
                "document.querySelector('input#btnFinalizarPedido2').click();")

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "title-fechamento")))

            check = driver.find_elements_by_xpath("//span[@class='lblNome']")
            if(len(check) < 1):
                Produto.login(driver)

            time.sleep(8)
            #WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "freteheader")))

            transportadora = driver.find_elements_by_xpath(
                "//div[@class='freteheader']")
            valor = driver.find_elements_by_xpath(
                "//div[@class='descricaoFrete']//strong")
            prazo = driver.find_elements_by_xpath(
                "//div[@class='prazofrete']//span[1]")
            cont = 0

            while cont < (len(transportadora)):
                bleh = dict(Nome=nome,
                            Transportadora=transportadora[cont].text, Quantidade=QTD, Preço=valor[cont].text, Prazo=prazo[cont].text)
                Produto.infos.append(bleh)
                cont += 1

            driver.get("https://checkout.lojasguapore.com.br/")

    driver.quit()

with open("TESTE-FRETE.csv", 'w') as f:
    dict_writer = csv.DictWriter(f, fieldnames=bleh.keys(), delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(Produto.infos)
print(Produto.infos)
