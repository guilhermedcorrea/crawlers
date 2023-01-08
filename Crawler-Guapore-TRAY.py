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

# BASE TUTORIAL        : https://medium.com/@henriquecoura_87435/webscraping-com-python-extraindo-dados-de-um-ecommerce-89c16b622f69
# DICIONARIO DE LISTAS : https://stackoverflow.com/questions/1024847/add-new-keys-to-a-dictionary
# Dicionario de listas : https://docs.python.org/2/tutorial/datastructures.html
# CSV STUFF            : https://www.programiz.com/python-programming/working-csv-files#quotes-files
# CSV STUFF            : https://realpython.com/python-csv/
# Sintax for writerows : https://stackoverflow.com/questions/15129567/csv-writer-writing-each-character-of-word-in-separate-column-cell/27065792#27065792
# Remove Blank Stuff   : https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string-in-python
# BASE PRODUCT URL     : https://www.madeiramadeira.com.br/guarda-roupa-casal-com-espelho-3-portas-de-correr-ravena-rufato-196037.html
# Best Compare ( IN )  : https://stackoverflow.com/questions/35302215/python-in-operator
# Fastest check value  : https://stackoverflow.com/questions/7571635/fastest-way-to-check-if-a-value-exist-in-a-list


ULR = "https://www.lojasguapore.com.br/"
FILENAME = "Tramontina-Fix.csv"

generico = "AAQUI VAI A DESCRIÇÂO"


def blank(texto):
    if(texto != None):
        Noblank = " ".join(texto.split())
        return Noblank


def formatar(texto):
    texto = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]',
                   '', texto)
    texto = texto.strip(" ")
    texto = texto.capitalize()
    unaccented_string = unidecode.unidecode(texto)
    return unaccented_string


class Organizer(object):
    def __init__(self, key):
        self.filename = "Bel lazer-Madeira.csv"
        self.Cods = ['Código', 'Gerais - Referência', ' • Referência',
                     'Referência', ' Referência', 'Cod_Secundario', 'CodRef', 'Codref', 'Código de barras', 'EAN', 'Ean', 'Código De Barras']
        self.basic = ['Nome', 'Name', 'Descrição', "DescInfo",
                      'Marca', 'Categoria', 'De', 'Por']
        self.key = key

    def Alinha(self):
        Basic = [s for s in self.key if s in self.basic]
        Cods = [s for s in self.key if s in self.Cods]
        Img = [s for s in self.key if "Imagem" in s]
        Img.sort()
        Attr = [s for s in self.key if "Attributo" in s]
        Attr.sort()
        FULL = []

        for x in Basic:
            FULL.append(x.strip(" "))
        for x in Cods:
            FULL.append(x.strip(" "))
        for x in Img:
            FULL.append(x.strip(" "))
        for x in Attr:
            FULL.append(x.strip(" "))

        resto = set(self.key) - set(FULL)
        resto = list(resto)
        resto.sort()

        for x in resto:
            FULL.append(x.strip(" "))
        return FULL


class EcommerceSpider(object):
    def __init__(self, start_url):
        self.links = {}
        self.items = []
        self.start_url = start_url
        self.set_base_url()
        self.key = []
        self.remove = ["Descrição 2", "Categoria", "Descrição2",
                       "SKU", "cat", "DescInfo", "Foto", "VIXI"]
        self.removed = []
        self.sku = []
        self.errors = 0
        self.testerror = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.filename = "URLS.csv"

    def clearshit(self, dic):
        for x in dic.keys():
            if x in self.remove:
                self.removed.append(x)

        for a in self.removed:
            dic.pop(a, None)

        return dic

    def timewarn(self):
        self.end_time = time.strftime("%b.%d-%X")
        print("Start : "+self.start_time + " End : "+self.end_time)

    def crawl(self):
        self.get_links()
        self.get_items()

    def crawl_to_file(self, filename):
        self.crawl()
        self.save_items(filename)

    def get_links(self):
        self.CSVREADER()

    def get_items(self):
        driver = webdriver.Chrome()
        for sku in self.sku:
            print(self.links[sku])
            driver.get(self.links[sku])
            self.items.append(self.extract_item(driver, sku))

    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    self.errors += 1
                else:
                    self.key.append(check)

    def CSVREADER(self):
        with open(self.filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.sku.append(row["SKU"])
                self.links[row["SKU"]] = row["URL"]

    def JSON_CREATE(self, dic):
        JSON = json.dumps(dic, ensure_ascii=False)
        div = "<div class='especif'>"+JSON+"</div>"
        return div

    def extract_item(self,  driver, SKU):
        EspList = {}

        try:
            nome = driver.find_elements_by_xpath(
                "//div[@class='product__name']")[0].text
        except IndexError as e:
            nome = "Not Found"

        try:
            fullcat = ""
            cat = driver.find_elements_by_xpath(
                "//div[@id='fbits-breadcrumb']//span[@itemprop='name']")
            for x in cat:
                fullcat += x.text + " > "
        except IndexError as e:
            fullcat = "Not Found"

        descinfo = 1
        try:
            desc = blank(driver.find_elements_by_xpath(
                "//div[@class='desc']")[0].text.replace("Descrição", "").strip(" "))
            if(desc == nome.strip(" ")):
                descinfo = 0

        except IndexError as e:
            desc = "Not Found"

        try:
            marca = driver.find_elements_by_xpath(
                "//span[@class='marca']")[0].text
        except IndexError as e:
            marca = "Not Found"

        try:
            foto = driver.find_elements_by_xpath(
                "//meta[@property='og:image']")[0].get_attribute("content")
            if(foto == "https://lojasguapore.fbitsstatic.net/img/p/produto-nao-possui-foto-no-momento/sem-foto.jpg?w=420&h=420&v=no-change"):
                foto = "NAO"
            else:
                foto = "SIM"
        except IndexError as e:
            foto = "Not Found"

        EspList = dict(Nome=nome, cat=fullcat, Descrição=generico, DescInfo=descinfo,
                       Foto=foto, SKU=SKU, Marca=marca)

        att = driver.find_elements_by_xpath(
            "//table[@class='esp']/tbody/tr/th")
        val = driver.find_elements_by_xpath(
            "//table[@class='esp']/tbody/tr/td")
        cont = 0

        if(len(att) == 0):
            EspList["VIXI"] = "Não TEM INFOS"

        for x in att:
            EspList[formatar(att[cont].text)] = val[cont].text
            cont += 1

        imgs = driver.find_elements_by_xpath("//div[@id='galeria']//img")
        imgcont = 1

        for img in imgs:
            EspList["Imagem "+str(imgcont)] = img.get_attribute(
                "src").replace("w=140&h=140", "w=900&h=900")
            imgcont += 1

        teste = dict(EspList)
        teste = self.clearshit(teste)
        EspList["JSON"] = self.JSON_CREATE(teste)

        return EspList

    def parse_links(self, html, item_url_xpath):
        new_links = html.xpath(item_url_xpath)
        new_links = [self.prepare_url(l) for l in new_links]
        self.links = self.links.union(set(new_links))
        self.testerror.append(new_links)

    def set_base_url(self):
        self.base_url = urlsplit(self.start_url)._replace(
            path="", query="").geturl()

    def prepare_url(self, url):
        url = urljoin(self.base_url, url)
        return urlsplit(url)._replace(query="").geturl()

    def save_items(self, filename):
        self.create_dict()
        print(self.key)
        org = Organizer(self.key)
        fieldnames = org.Alinha()
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)
            print(len(self.items))
            print(self.items)


print("LETS GET IT STARTED")
spider = EcommerceSpider(ULR)
try:
    spider.crawl_to_file(FILENAME)
except KeyboardInterrupt as e:
    spider.create_dict()
    org = Organizer(spider.key)
    fieldnames = org.Alinha()
    with open("CLOSED.csv", 'w', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(
            f, fieldnames=fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(spider.items)
