from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ActionChains
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import time
import lxml.html as parser
import requests
import csv
import random
from urllib.parse import urlsplit, urljoin

# Page Down       : https://stackoverflow.com/questions/21006940/how-to-load-all-entries-in-an-infinite-scroll-at-once-to-parse-the-html-in-pytho
# Infinite Scroll : https://michaeljsanders.com/2017/05/12/scrapin-and-scrollin.html


class Product(object):
    def __init__(self):
        self.filename = "-Frete.csv"
        self.CEP = []
        self.city = {}
        self.est = {}
        self.links = {}
        self.prod = []
        self.fabricante = ['https://www.lojasguapore.com.br/fabricante/arquitetizze', 'https://www.lojasguapore.com.br/fabricante/artyflex', 'https://www.lojasguapore.com.br/fabricante/astra', 'https://www.lojasguapore.com.br/fabricante/avant', 'https://www.lojasguapore.com.br/fabricante/bel-lazer', 'https://www.lojasguapore.com.br/fabricante/bella-janela', 'https://www.lojasguapore.com.br/fabricante/black-decker', 'https://www.lojasguapore.com.br/fabricante/boxer', 'https://www.lojasguapore.com.br/fabricante/bronzearte', 'https://www.lojasguapore.com.br/fabricante/celite', 'https://www.lojasguapore.com.br/fabricante/ceusa', 'https://www.lojasguapore.com.br/fabricante/chamalux', 'https://www.lojasguapore.com.br/fabricante/chandelie', 'https://www.lojasguapore.com.br/fabricante/cortag', 'https://www.lojasguapore.com.br/fabricante/cromalux', 'https://www.lojasguapore.com.br/fabricante/csm', 'https://www.lojasguapore.com.br/fabricante/cumulus', 'https://www.lojasguapore.com.br/fabricante/deca', 'https://www.lojasguapore.com.br/fabricante/docol', 'https://www.lojasguapore.com.br/fabricante/durafloor', 'https://www.lojasguapore.com.br/fabricante/eglo', 'https://www.lojasguapore.com.br/fabricante/europa', 'https://www.lojasguapore.com.br/fabricante/evolux', 'https://www.lojasguapore.com.br/fabricante/fabrimar', 'https://www.lojasguapore.com.br/fabricante/fischer', 'https://www.lojasguapore.com.br/fabricante/fogatti', 'https://www.lojasguapore.com.br/fabricante/franke', 'https://www.lojasguapore.com.br/fabricante/gart', 'https://www.lojasguapore.com.br/fabricante/gravia',
                           'https://www.lojasguapore.com.br/fabricante/grudado', 'https://www.lojasguapore.com.br/fabricante/hydra', 'https://www.lojasguapore.com.br/fabricante/ibbl', 'https://www.lojasguapore.com.br/fabricante/incepa', 'https://www.lojasguapore.com.br/fabricante/jacuzzi', 'https://www.lojasguapore.com.br/fabricante/jatoba', 'https://www.lojasguapore.com.br/fabricante/komeco', 'https://www.lojasguapore.com.br/fabricante/laufen', 'https://www.lojasguapore.com.br/fabricante/lorenzetti', 'https://www.lojasguapore.com.br/fabricante/made-marcs', 'https://www.lojasguapore.com.br/fabricante/meber', 'https://www.lojasguapore.com.br/fabricante/mekal', 'https://www.lojasguapore.com.br/fabricante/midea', 'https://www.lojasguapore.com.br/fabricante/mor', 'https://www.lojasguapore.com.br/fabricante/ourofino', 'https://www.lojasguapore.com.br/fabricante/ralo-linear', 'https://www.lojasguapore.com.br/fabricante/roca', 'https://www.lojasguapore.com.br/fabricante/safanelli', 'https://www.lojasguapore.com.br/fabricante/santa-luzia', 'https://www.lojasguapore.com.br/fabricante/sasazaki', 'https://www.lojasguapore.com.br/fabricante/stanley', 'https://www.lojasguapore.com.br/fabricante/suggar', 'https://www.lojasguapore.com.br/fabricante/tapetes-sao-carlos', 'https://www.lojasguapore.com.br/fabricante/tarkett', 'https://www.lojasguapore.com.br/fabricante/taschibra', 'https://www.lojasguapore.com.br/fabricante/tecno-mobili', 'https://www.lojasguapore.com.br/fabricante/tigre', 'https://www.lojasguapore.com.br/fabricante/tramontina', 'https://www.lojasguapore.com.br/fabricante/vulcan', 'https://www.lojasguapore.com.br/fabricante/wbertolo']
        self.QTD = ["5"]
        self.Piso = ["300", "30", "50"]
        self.CodRef = []
        self.arq = ["produtos-ceps"]
        self.SKU = {}
        self.EAN = {}

    def colect_links(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        session = requests.Session()

        for fabricante in self.fabricante:
            print(fabricante)
            r = session.get(fabricante, headers=headers)
            html = parser.fromstring(r.text)

            check = len(html.xpath("//div[@class='image404']"))

            if check != 1:
                link = html.xpath("//a[@class='spot-parte-um']/@href")

                numba = len(link) - 1
                if(numba > 0):
                    RND = randoms(numba)
                else:
                    RND = 0
                self.prod.append(fabricante)
                self.links[fabricante] = link[RND]
        print(self.links)

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
        self.links = {}
        self.prod = []
        print("LuLUMBA")
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.prod.append(row["Nome"])
                self.SKU[row["Nome"]] = row["SKU"]
                self.EAN[row["Nome"]] = row["EAN"]
                self.links[row["Nome"]] = row["Link"]

    def send_email(self):
        email = ''
        password = ''
        send_to_email = 'crawler@lojasguapore.com.br'
        subject = 'Teste Frete'
        message = 'Planilha de Teste de frete em anexo'
        file_location = 'Fretes1.csv'

        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = send_to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        filename = os.path.basename(file_location)
        attachment = open(file_location, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit()


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

driver = webdriver.Chrome(
    'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe', chrome_options=chrome_options)

Produto = Product()
teste = []
Produto.CSVREADER("Ceps.csv")
try:
    for x in Produto.arq:
        Produto.CSVREADER2(x+".csv")
        print("LENDER")
        Produto.filename = x + Produto.filename
        for nome in Produto.prod:
            driver.get(Produto.links[nome])
            check = driver.find_elements_by_xpath("//div[@class='image404']")
            SKU = Produto.SKU[nome]
            EAN = Produto.EAN[nome]
            if(len(check) == 0):
                print(len(check))
                frete = driver.find_element_by_id('txtCalculaFreteProduto')
                for cep in Produto.CEP:
                    print(cep)
                    frete.click
                    time.sleep(1)
                    frete.send_keys(Keys.HOME)
                    frete.send_keys(cep)
                    time.sleep(1)
                    clica = driver.find_element_by_id('btnCalculaFreteProduto')
                    clica.send_keys(Keys.ENTER)

                    time.sleep(6)

                    price = driver.find_elements_by_xpath(
                        "//table[@class='resultado-frete']/tbody/tr")

                    error = driver.find_element_by_class_name("errosFrete")
                    error = error.get_attribute("style")
                    if not("display: block;" in error):
                        for x in price:
                            if("\n" in x.text):
                                transportadora, preco, prazo = x.text.split(
                                    "\n")
                                bleh = dict(Nome=nome, SKU=SKU, EAN=EAN, CEP=cep, Transportadora=transportadora,
                                            Preço=preco, Prazo=prazo)
                                teste.append(bleh)
                            else:
                                print("IRGI")
                    else:
                        bleh = dict(Nome=nome, SKU=SKU, EAN=EAN, CEP=cep, Transportadora="ERRO",
                                    Preço="ERRRO", Prazo="ERRO")
                        teste.append(bleh)
        with open(Produto.filename, 'w') as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=bleh.keys(), delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(teste)
except:
    with open(Produto.filename, 'w') as f:
        dict_writer = csv.DictWriter(
            f, fieldnames=bleh.keys(), delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(teste)


print(teste)

driver.quit()
