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


ULR = "http://www.komeco.com.br/produtos-e-acessorios/linha/aquecedor-de-agua-a-gas/categoria/digital/"
FILENAME = "Komeco.csv"
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
        self.links = ['http://www.komeco.com.br/produtos-e-acessorios/5/nova-inverter.html', 'http://www.komeco.com.br/produtos-e-acessorios/45/eco.html', 'http://www.komeco.com.br/produtos-e-acessorios/7/piso-teto-r-410a.html', 'http://www.komeco.com.br/produtos-e-acessorios/9/cassete.html', 'http://www.komeco.com.br/produtos-e-acessorios/10/cortina-de-ar.html', 'http://www.komeco.com.br/produtos-e-acessorios/47/solucoes-em-climatizacao.html', 'http://www.komeco.com.br/produtos-e-acessorios/48/solucoes-em-climatizacao-skcv.html', 'http://www.komeco.com.br/produtos-e-acessorios/23/ko-07b.html', 'http://www.komeco.com.br/produtos-e-acessorios/57/ko-07b.html', 'http://www.komeco.com.br/produtos-e-acessorios/31/coletor-solar.html', 'http://www.komeco.com.br/produtos-e-acessorios/46/coletor-solar-tubo-a-vacuo.html', 'http://www.komeco.com.br/produtos-e-acessorios/32/coletor-de-piscina.html', 'http://www.komeco.com.br/produtos-e-acessorios/33/reservatorio-termico.html', 'http://www.komeco.com.br/produtos-e-acessorios/51/reservatorio-termico-ppr.html', 'http://www.komeco.com.br/produtos-e-acessorios/41/grandes-obras.html', 'http://www.komeco.com.br/produtos-e-acessorios/24/tp-820.html', 'http://www.komeco.com.br/produtos-e-acessorios/26/tqc-200.html',
                      'http://www.komeco.com.br/produtos-e-acessorios/28/tp-40.html', 'http://www.komeco.com.br/produtos-e-acessorios/29/tp-80.html', 'http://www.komeco.com.br/produtos-e-acessorios/30/tp-40-thermo.html', 'http://www.komeco.com.br/produtos-e-acessorios/11/umidificador-de-ar.html', 'http://www.komeco.com.br/produtos-e-acessorios/12/desumidificador-de-ar.html', 'http://www.komeco.com.br/produtos-e-acessorios/52/ko-07m-bp.html', 'http://www.komeco.com.br/produtos-e-acessorios/16/ko-12m.html', 'http://www.komeco.com.br/produtos-e-acessorios/53/ko-15ddi-prime.html', 'http://www.komeco.com.br/produtos-e-acessorios/58/ko-35ddi-prime.html', 'http://www.komeco.com.br/produtos-e-acessorios/55/ko-20ddi-prime.html', 'http://www.komeco.com.br/produtos-e-acessorios/56/ko-25ddi.html', 'http://www.komeco.com.br/produtos-e-acessorios/17/ko-15ddi.html', 'http://www.komeco.com.br/produtos-e-acessorios/18/ko-20ddi.html', 'http://www.komeco.com.br/produtos-e-acessorios/19/ko-22ddi.html', 'http://www.komeco.com.br/produtos-e-acessorios/20/ko-31ddi.html', 'http://www.komeco.com.br/produtos-e-acessorios/21/ko-43ddi.html', 'http://www.komeco.com.br/produtos-e-acessorios/13/ko-15ffi.html', 'http://www.komeco.com.br/produtos-e-acessorios/14/ko-20ffi.html']

    def get_items(self):
        for link in self.links:
            r = requests.get(link, headers=headers)
            html = parser.fromstring(r.text)
            print(str(r) + " : " + link)
            check = len(html.xpath("//table[@id='example']/thead/tr/th"))
            if(check > 1):
                check = check - 1

            flag = 0
            print(check)
            while(flag != check):
                dic, flag = self.extract_item(html, flag)
                self.items.append(dic)

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

    def extract_item(self, html, flag):
        flag += 1
        try:
            nome = html.xpath(
                "//div[@class='content headerHero frameBox ']/div[@class='fLeft']/h1")[0].text
        except IndexError as e:
            nome = "Not Found"

        try:
            manual = html.xpath("//a[@class='icone__PDF']/@href")[0]
            manual = self.prepare_url(manual)
        except IndexError as e:
            manual = "Not Found"

        EspList = dict(Nome=nome, Manual=manual)

        try:
            cats = html.xpath(
                "//nav[@class='flex rowNoWrap flexStart']//text()")
            fullcat = ""
            for x in cats:
                x = x.replace("\n", "").replace("\t", "")
                if(len(x) > 0):
                    fullcat += x + " > "
            EspList["Categoria"] = fullcat
        except IndexError as e:
            cats = "Not Found"

        desc = html.xpath("//div[@class='content gcBox']//text()")
        fulldesc = ""
        for x in desc:
            x = x.replace("\t", "").replace("\n", "").replace("\r", "")
            if(len(x) > 0):
                fulldesc += x + "<br>"

        EspList["Descrição"] = fulldesc

        try:
            video = html.xpath(
                "//div[@class='container_video cover']/div/a/@href")[0]
        except IndexError as e:
            video = "Not Found"

        EspList["Video"] = video

        imagem = html.xpath(
            "//ul[@class='slideBox slideBoxProdutos']/li/div/img/@src")
        imgcont = 1
        for x in imagem:
            EspList["Imagem "+str(imgcont)
                    ] = self.prepare_url(x)
            imgcont += 1

        carac = html.xpath(
            "//div[@class='col_2_3 fLeft lista_caracteristicas']//ul/li")
        cont = 1

        for x in carac:
            EspList[x[1].text] = x[0].attrib['src']
            EspList["Atributo "+str(cont)] = x[1].text
            cont += 1

        especif = html.xpath("//table[@id='example']/tbody/tr")

        for x in especif:
            EspList[x[0].text] = x[flag].text

        try:
            code = html.xpath("//table[@id='example']/thead//th")[flag].text
        except IndexError as e:
            code = "Not Found"

        EspList["Code"] = code

        return EspList, flag

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
