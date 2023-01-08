import lxml.html as parser
import requests
import csv
import time
import re
import unidecode
import json
from urllib.parse import urlsplit, urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

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


filee = "Durafloor"
base = "https://www.duratexmadeira.com.br"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


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


class Organizer(object):
    def __init__(self, key):
        self.filename = "Bel lazer-Madeira.csv"
        self.Cods = ['Código', 'Gerais - Referência', ' • Referência',
                     'Referência', ' Referência', 'Cod_Secundario', 'CodRef', 'Codref', 'Código de barras', 'EAN', 'Ean', 'Código De Barras']
        self.basic = ['Nome', 'Name', 'Descrição',
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
        self.links = set
        self.CodRef = []
        self.items = []
        self.start_url = start_url
        self.set_base_url()
        self.key = []
        self.remove = ["Descrição 2", "Categoria", "Descrição2",
                       "SKU", "cat", "DescInfo", "Foto", "VIXI"]
        self.removed = []
        self.errors = 0
        self.start_time = time.time()
        self.testerror = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.cats = []
        self.file = "obrafacil.csv"

    def timewarn(self):
        self.end_time = time.strftime("%b.%d-%X")
        print("Start : "+self.start_time + " End : "+self.end_time)

    def CSVREADER(self):
        with open(self.file, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.CodRef.append(row["CODREF"])
                self.links[row["CODREF"]] = row["URL"]

    def crawl(self):
        self.get_links()
        self.get_items()

    def crawl_to_file(self, filename):
        self.crawl()
        self.save_items(filename)

    def get_links(self):
        self.links = ["https://www.duratexmadeira.com.br/pisos/pisos-laminados/link/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/street/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/unique/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/studio/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/nature/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/new-way/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/acessorios-de-acabamento/perfil-mdf/mdf-perfil-piso-parede/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/acessorios-de-acabamento/perfil-mdf/mdf-frontal-de-escada/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/acessorios-de-acabamento/perfil-mdf/mdf-perfil-redutor/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/acessorios-de-acabamento/perfil-mdf/mdf-perfil-t/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/acessorios-de-instalacao/manta-reciclada/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/acessorios-de-instalacao/manta-durasilent/","https://www.duratexmadeira.com.br/pisos/pisos-laminados/acessorios-de-instalacao/manta-eco/","https://www.duratexmadeira.com.br/pisos-vinilicos-spc/linha-atelier/","https://www.duratexmadeira.com.br/pisos/pisos-vinilicos-lvt/inova/","https://www.duratexmadeira.com.br/pisos/pisos-vinilicos-lvt/idea/","https://www.duratexmadeira.com.br/pisos/pisos-vinilicos-lvt/loft/","https://www.duratexmadeira.com.br/pisos/pisos-vinilicos-lvt/art/","https://www.duratexmadeira.com.br/pisos/pisos-vinilicos-lvt/city/","https://www.duratexmadeira.com.br/pisos/pisos-vinilicos-lvt/urban/","https://www.duratexmadeira.com.br/rodapes/rodapes-para-todos-os-pisos/maxx/","https://www.duratexmadeira.com.br/rodapes/rodapes-para-todos-os-pisos/essencial/","https://www.duratexmadeira.com.br/rodapes/rodapes-para-todos-os-pisos/easy/","https://www.duratexmadeira.com.br/rodapes/rodapes-para-pisos-laminados/cantoneira/","https://www.duratexmadeira.com.br/rodapes/rodapes-para-pisos-laminados/rodape-fixo/","https://www.duratexmadeira.com.br/rodapes/rodapes-para-pisos-laminados/rodape-clean/"]

    def get_items(self):
        for link in self.links:
            r = requests.get(link)
            html = parser.fromstring(r.text)
            print(str(r) + " : " + link)
            self.items.append(self.extract_item(html, link))

    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    self.errors += 1
                else:
                    self.key.append(check)

    def JSON_CREATE(self, dic):
        JSON = json.dumps(dic, ensure_ascii=False)
        div = "<div class='especif'>"+JSON+"</div>"
        return div

    def clearshit(self, dic):
        for x in dic.keys():
            if x in self.remove:
                self.removed.append(x)
            if "Imagem" in x:
                self.removed.append(x)

        for a in self.removed:
            dic.pop(a, None)

        return dic

    def extract_item(self, html, link):
        EspList = {}
        N = "Not Found"

        try:
            linha = html.xpath("//h1[@class='title-page col-mb-12']")[0].text
        except IndexError as e:
            linha = N

        try:
            sub = html.xpath("//h2[@class='subtitle col-mb-12']")[0].text
        except IndexError as e:
            sub = N

        try:
            desc = html.xpath("//div[@class='the-content col-mb-12']/p")[0].text
        except IndexError as e:
            desc = N

        EspList = dict(Linha=linha, Subtitulo=sub, Descrição=desc)

        try:
            cor = html.xpath("//ul[@class='list-product']//span")
            corcont = 1
            for x in cor:
                EspList["Cor "+str(corcont)] = blank(x.text)
                print(x.text)
                corcont += 1
        except IndexError as e:
            cor = "N"


        try:
            indica = html.xpath(
                "//section[@class='indicacoes-contra container']//ul[1]/li")
            indcont = 1
            for x in indica:
                EspList["Indicações "+str(indcont)] = blank(x.text)
                indcont += 1
        except IndexError as e:
            indica = N

        try:
            beneficios = html.xpath("//ul[@class='list-benefit col-mb-12']//li/span")
            bencont = 1
            for x in beneficios:
                EspList["Beneficio "+str(bencont)] = blank(x.text)
                bencont += 1
        except IndexError as e:
            beneficios = N


        att = html.xpath("//p[@class='left']")
        val = html.xpath("//ul[@class='right']//li")
        cont = 0

        for x in att:
            EspList[x.text] = blank(val[cont].text)
            cont += 1

        teste = dict(EspList)
        teste = self.clearshit(teste)
        EspList["JSON"] = self.JSON_CREATE(teste)

        return EspList

    def parse_links(self, html, item_url_xpath):
        new_links = html.xpath(item_url_xpath)
        new_links = [self.prepare_url(l) for l in new_links]
        self.links = self.links.union(set(new_links))

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


print("LETS GET IT STARTED")


spider = EcommerceSpider(
    "http://www.banheirosincepa.com.br/produtos?pagina=32")
try:
    spider.crawl_to_file(filee+".csv")
except KeyboardInterrupt as e:
    spider.create_dict()
    org = Organizer(spider.key)
    fieldnames = org.Alinha()
    with open("CLOSED.csv", 'w', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(
            f, fieldnames=fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(spider.items)
