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
import random
from urllib.parse import urlsplit, urljoin


class Product(object):
    def __init__(self):
        self.filename = "Fretes2.csv"
        self.CEP = ["13091120", "57540000"]
        self.infos = []
        self.cats = []
        self.catries = 1
        self.tries = 1
        self.nome = ["Carrinho 6", "Carrinho 6", "Carrinho 6", "Carrinho 6"]
        self.prod = []
        self.links = {}
        self.QTD = ["2"]
        self.CodRef = []
        self.username = "rikrdo_vieir@hotmail.com"
        self.password = "odra31cir"
        self.error = []

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

    def CATREADER(self, filename):
        self.prod = []
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.cats.append(row["Link"])

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


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')


Produto = Product()
Produto.CATREADER("Cats.csv")

pedcont = 1
for nome in Produto.nome:
    catcont = 0

    driver = webdriver.Chrome(
        'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe', chrome_options=chrome_options)
    Produto.prod = [
        "https://www.lojasguapore.com.br/produto/cuba-de-apoio-retangular-com-mesa-350x315mm-branco-l-7300-17-deca-116439"]
    while catcont < Produto.catries:
        RND = randoms(len(Produto.cats)) - 1
        print(len(Produto.cats))
        cont = 0
        driver.get(Produto.cats[RND])
        pegaprod = driver.find_elements_by_xpath("//a[@class='spot-parte-um']")
        while cont < Produto.tries:
            RND = randoms(len(pegaprod)) - 1
            Produto.prod.append(pegaprod[RND].get_attribute("href"))
            cont += 1
        catcont += 1

    print(Produto.prod)
    err = {}
    for link in Produto.prod:
        driver.get(link)

        Disponivel = driver.find_elements_by_xpath(
            "//div[@class='avisoIndisponivel']")

        if(Disponivel[0].get_attribute("style") == ""):  # PRODUTO NAO disponivel
            err = dict(Error=link)
            Produto.error.append(err)

        else:
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
        if(QTD != "1"):
            for x in quantidade:
                RND = randoms(6)
                x.send_keys(Keys.CONTROL, 'a')
                x.send_keys(RND)
                time.sleep(4)

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "btfinalizar")))

        finalizar = driver.find_element_by_css_selector(
            "input#btnFinalizarPedido2")
        driver.execute_script(
            "document.querySelector('input#btnFinalizarPedido2').click();")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "title-fechamento")))

        check = driver.find_elements_by_xpath(
            "//input[@id='txtLoginEmail']")
        print(len(check))
        if(len(check) > 0):
            Produto.login(driver)

        time.sleep(3)
        transportadora = driver.find_elements_by_xpath(
            "//div[@class='freteheader']")

        print(len(transportadora))
        if(len(transportadora) > 0):
            ID = randoms(len(transportadora))

            ID = "ddlEscolhaFrete-"+str(ID)

            frete = driver.find_element_by_id(ID)
            frete.click()

        time.sleep(8)
        boleto = driver.find_element_by_xpath(
            "//label[@for='rbnFormaPagamento-24']")
        boleto.click()

        FIM = driver.find_element_by_css_selector(
            "button#btnFinalizarPedidoFinal2")
        driver.execute_script(
            "document.querySelector('button#btnFinalizarPedidoFinal2').click();")
        time.sleep(10)

        alert = driver.switch_to_alert()
        alert.accept()

    WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "fbits-numero-pedido")))
    codigo = driver.find_element_by_xpath(
        "//p[@class='title biggest fbits-numero-pedido']")
    print(codigo.text)
    bleh = dict(NumeroPedido=codigo.text, PRODUTOS=Produto.prod)
    Produto.infos.append(bleh)

    driver.quit()

with open("TESTE-Pedidos.csv", 'w') as f:
    dict_writer = csv.DictWriter(f, fieldnames=bleh.keys(), delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(Produto.infos)

print(Produto.infos)
if(len(err) > 0):
    with open("ERROS-PEDIDOS.csv", 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames=err.keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(Produto.error)
