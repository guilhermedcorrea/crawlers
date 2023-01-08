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


ULR = "https://www.fogattionline.com.br/coifas-----2.xhtml"
FILENAME = "BLACKFogati.csv"
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
        None

    def get_items(self):
        for link in self.links:
            RND = randoms(10)
            time.sleep(RND)
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
        try:
            Nome = html.xpath(
                "//h1[@style='color:#5b5b5b;font-size:22px;']/span")[0].text
        except IndexError as e:
            Nome = "Not Found"

        EspList["Nome"] = Nome

        try:
            att = html.xpath("//div[@class='InfoProd']/text()")
            first = 0
            attcont = 1
            for x in att:
                x = x.replace("\r\n", "").strip(" ").replace(
                    "- ", "").replace("\t", "").replace("\xa0", "")
                if(len(x) > 0):
                    if(first == 0):
                        EspList["Descrição"] = x
                        first = 1
                    elif(":" in x):
                        ref, val = x.split(":", 1)
                        EspList[formatar(ref)] = val
                    else:
                        EspList["Atributo "+str(attcont)] = x
                        attcont += 1
        except IndexError as e:
            att = "Not Found"

        ean = html.xpath("//div[@class='InfoProd']//p/text()")
        eancont = 1
        for x in ean:
            try:
                EAN = re.search("\d\d\d\d\d\d\d\d\d\d\d\d\d", x)
                if EAN == None:
                    EAN = "Not Found"
                else:
                    EAN = EAN.group(0)
                    EspList["Ean "+str(eancont)] = x
                    eancont += 1

            except IndexError as e:
                EAN = "Not Found"

        table = html.xpath(
            "//p[@style='float:left; width:40%; text-align: right;line-height: 35px']/b")

        table_val = html.xpath(
            "//p[@style='float:left; width:50%;line-height: 35px']")
        cont = 0
        for x in table:
            if(table_val[cont].text != None):
                EspList[formatar(x.text)] = table_val[cont].text
            cont += 1

        imgs = html.xpath("//div[@class='FotoMenor some']/a/@href")
        imgcont = 1
        for img in imgs:
            img = self.prepare_url(img)
            EspList["Imagem "+str(imgcont)] = img
            imgcont += 1

        try:
            video = html.xpath(
                "//div[@style=' width:510px; float:left; height:540px;']/a/@onclick")[0].split("'")
            for x in video:
                if("youtube" in x):
                    EspList["Video"] = x
                    break
        except IndexError as e:
            video = "Not Found"

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
        with open(filename, 'w', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)
            print(self.links)


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
