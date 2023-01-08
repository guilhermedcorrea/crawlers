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
import random

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


ULR = "https://www.formix3d.com.br/modelos"
FILENAME = "Formix.csv"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def blank(texto):
    if(texto != None):
        Noblank = " ".join(texto.split())
        return Noblank


def randoms(ranges):
    ranges = random.randint(1, ranges)
    return ranges


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
        self.links = [
            "https://www.fogattionline.com.br/coifa-de-parede-75cm--20.html"]
        self.items = []
        self.start_url = start_url
        self.set_base_url()
        self.key = []
        self.pre = ['https://www.fogattionline.com.br/coifas-----2.xhtml', 'https://www.fogattionline.com.br/coifa-ilha-retangular---52.xhtml', 'https://www.fogattionline.com.br/coifa-ilha-vidro-curvo--57.xhtml', 'https://www.fogattionline.com.br/coifa-de-parede-retangular--48.xhtml', 'https://www.fogattionline.com.br/depuradores-de-ar---76.xhtml', 'https://www.fogattionline.com.br/coifa-vidro-reto---70.xhtml', 'https://www.fogattionline.com.br/coifa-ilha-vidro-reto--60.xhtml', 'https://www.fogattionline.com.br/coifa-vidro-curvo---64.xhtml', 'https://www.fogattionline.com.br/cooktops-----3.xhtml', 'https://www.fogattionline.com.br/cooktop-----97.xhtml',
                    'https://www.fogattionline.com.br/fornos-eletricos----4.xhtml', 'https://www.fogattionline.com.br/fornos-----101.xhtml', 'https://www.fogattionline.com.br/super-fogo----27.xhtml', 'https://www.fogattionline.com.br/resistencia-eletrica----104.xhtml', 'https://www.fogattionline.com.br/micro-ondas-----42.xhtml', 'https://www.fogattionline.com.br/micro-ondas-de-embutir---43.xhtml', 'https://www.fogattionline.com.br/pecas-----78.xhtml', 'https://www.fogattionline.com.br/pecas-forno----85.xhtml', 'https://www.fogattionline.com.br/pecas-coifa----87.xhtml', 'https://www.fogattionline.com.br/pecas-cooktop----79.xhtml']
        self.remove = ["Descrição 2", "Categoria", "Descrição2",
                       "SKU", "cat", "DescInfo", "Foto", "VIXI"]
        self.removed = []
        self.sku = []
        self.errors = 0
        self.testerror = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.filename = "Guap1.csv"

    def clearshit(self, dic):
        for x in dic.keys():
            if x in self.remove:
                self.removed.append(x)
            if "Image" in x:
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
        self.links = ['https://www.formix3d.com.br/product-page/ref-029-sicilia', 'https://www.formix3d.com.br/product-page/ref-030-veneza', 'https://www.formix3d.com.br/product-page/ref-005-lampedusa', 'https://www.formix3d.com.br/product-page/ref-012-levanzo', 'https://www.formix3d.com.br/product-page/ref-023-salina', 'https://www.formix3d.com.br/product-page/ref-026-burano', 'https://www.formix3d.com.br/product-page/ref-042-garden', 'https://www.formix3d.com.br/product-page/ref-035-carrara', 'https://www.formix3d.com.br/product-page/ref-031-arezzo', 'https://www.formix3d.com.br/product-page/ref-033-perurgia', 'https://www.formix3d.com.br/product-page/ref-032-bari', 'https://www.formix3d.com.br/product-page/ref-039-crotone', 'https://www.formix3d.com.br/product-page/ref-021-giudecca', 'https://www.formix3d.com.br/product-page/ref-006-capri', 'https://www.formix3d.com.br/product-page/ref-043-siena', 'https://www.formix3d.com.br/product-page/ref-027-comacina', 'https://www.formix3d.com.br/product-page/ref-036-gela', 'https://www.formix3d.com.br/product-page/ref-003-%C3%A9gadi', 'https://www.formix3d.com.br/product-page/ref-004-linosa',
                      'https://www.formix3d.com.br/product-page/ref-009-giannutri', 'https://www.formix3d.com.br/product-page/ref-016-%C3%ADsquia', 'https://www.formix3d.com.br/product-page/ref-014-vivara', 'https://www.formix3d.com.br/product-page/ref-019-tavolara', 'https://www.formix3d.com.br/product-page/ref-020-tiberina', 'https://www.formix3d.com.br/product-page/ref-001-pel%C3%A1gia', 'https://www.formix3d.com.br/product-page/ref-007-marettimo', 'https://www.formix3d.com.br/product-page/ref-008-elba', 'https://www.formix3d.com.br/product-page/ref-010-torcello', 'https://www.formix3d.com.br/product-page/ref-011-cretaccio', 'https://www.formix3d.com.br/product-page/ref-015-tremiti', 'https://www.formix3d.com.br/product-page/ref-017-e%C3%B3lias', 'https://www.formix3d.com.br/product-page/ref-018-pontinas', 'https://www.formix3d.com.br/product-page/ref-022-murano', 'https://www.formix3d.com.br/product-page/ref-024-mazzorbo', 'https://www.formix3d.com.br/product-page/ref-025-lipara', 'https://www.formix3d.com.br/product-page/ref-028-ponza', 'https://www.formix3d.com.br/product-page/ref-037-savona', 'https://www.formix3d.com.br/product-page/ref-038-barletta']

    def get_items(self):
        for link in self.links:
            r = requests.get(link, headers=headers)
            html = parser.fromstring(r.text)
            print(str(r) + " : " + link)
            self.items.append(self.extract_item(html))

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
                self.sku.append(row["ID"])
                self.links[row["ID"]] = row["URL"]

    def JSON_CREATE(self, dic):
        JSON = json.dumps(dic, ensure_ascii=False)
        div = "<div class='especif'>"+JSON+"</div>"
        return div

    def extract_item(self,  html):
        EspList = {}

        nome = html.xpath("//h1[@data-hook='product-title']")[0].text
        EspList["Nome"] = nome

        attr = html.xpath("//pre[@class='_28cEs']//text()")
        cont = 1
        for att in attr:
            if(":" in att):
                att = att.replace("• ", "")
                a, b = att.split(":", 1)
                EspList[a] = b.strip(" ")
            else:
                EspList["Atributo "+str(cont)] = att
                cont += 1

        desc = html.xpath(
            "//div[@data-hook='info-section-description']/text()")

        for att in desc:
            att = att.replace("•", "").strip(" ")
            if(":" in att):
                a, b = att.split(":", 1)
                EspList[a] = b.strip(" ")
            else:
                EspList["Atributo "+str(cont)] = att
                cont += 1

        imgs = html.xpath("//a[@data-hook='magic-zoom-link']/@href")
        imgcont = 1

        for img in imgs:
            EspList["Imagem "+str(imgcont)] = img
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
