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
        FULL = [' Refil Girou, Trocou', ' Bandeja removível',
                ' Nanotecnologia', ' Ecocompressor', ' Refil Bacteriostático', ' Dimensão', ' Refrigeração', 'Volume Interno do Aparelho (L) ']

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
        self.links = ['https://www.ibbl.com.br/fr600-exclusive---filtro-purificador-ibbl-53041001_preto/p', 'https://www.ibbl.com.br/fr600-speciale---filtro-purificador-ibbl-52071001_prata/p', 'https://www.ibbl.com.br/smart-h2o-purificador-de-agua-ibbl-62071001_inox/p', 'https://www.ibbl.com.br/frq-600-expert---filtro-purificador-ibbl-55011001_branco/p', 'https://www.ibbl.com.br/fr600-expert---filtro-purificador-ibbl-54071001_prata/p', 'https://www.ibbl.com.br/immaginare---filtro-purificador-ibbl-48011001_branco/p', 'https://www.ibbl.com.br/mio---filtro-purificador-ibbl-56010001_branco/p', 'https://www.ibbl.com.br/pfn-2000---filtro-purificador-ibbl-38011001_branco/p', 'https://www.ibbl.com.br/bebedouro-ibbl-compact-preto-13041001_preto/p', 'https://www.ibbl.com.br/bebedouro-ibbl-gfn-11011001_branco/p', 'https://www.ibbl.com.br/bebedouro-ibbl-compact-bco-13011001_branco/p', 'https://www.ibbl.com.br/bebedouro-ibbl-compact-prata-13071001_prata/p', 'https://www.ibbl.com.br/bebedouro-ibbl-bag40c-inox-03031001_inox/p', 'https://www.ibbl.com.br/bebedouro-ibbl-bag40-inox-01031001_inox/p', 'https://www.ibbl.com.br/refil-ibbl-c-3-24010002_outro/p', 'https://www.ibbl.com.br/refil-ibbl-cz-7-24010005_outro/p', 'https://www.ibbl.com.br/refil-avanti-ibbl-24010004_outro/p', 'https://www.ibbl.com.br/refil-ibbl-c-5-24010003_outro/p', 'https://www.ibbl.com.br/refil-ibbl-pre-c-3-25010002_outro/p', 'https://www.ibbl.com.br/hot-dispenser-5-ou-chocolateira-ibbl-preto-22041001_preto/p', 'https://www.ibbl.com.br/refresqueira-ibbl-bbs2-17031001_inox/p', 'https://www.ibbl.com.br/fr600-exclusive---filtro-purificador-ibbl-53041001_preto/p', 'https://www.ibbl.com.br/fr600-speciale---filtro-purificador-ibbl-52071001_prata/p',
                      'https://www.ibbl.com.br/smart-h2o-purificador-de-agua-ibbl-62071001_inox/p', 'https://www.ibbl.com.br/frq-600-expert---filtro-purificador-ibbl-55011001_branco/p', 'https://www.ibbl.com.br/fr600-expert---filtro-purificador-ibbl-54071001_prata/p', 'https://www.ibbl.com.br/immaginare---filtro-purificador-ibbl-48011001_branco/p', 'https://www.ibbl.com.br/mio---filtro-purificador-ibbl-56010001_branco/p', 'https://www.ibbl.com.br/pfn-2000---filtro-purificador-ibbl-38011001_branco/p', 'https://www.ibbl.com.br/purificador-de-agua-pdf300-ibbl-60071001_prata/p', 'https://www.ibbl.com.br/purificador-de-agua-pdf300-2t-ibbl-61071001_prata/p', 'https://www.ibbl.com.br/purificador-de-agua-pdf100-ibbl-59071001_prata/p', 'https://www.ibbl.com.br/smart-h2o-purificador-de-agua-ibbl-62071001_inox/p', 'https://www.ibbl.com.br/bebedouro-ibbl-compact-bco-13011001_branco/p', 'https://www.ibbl.com.br/bebedouro-ibbl-compact-preto-13041001_preto/p', 'https://www.ibbl.com.br/bebedouro-ibbl-gfn-11011001_branco/p', 'https://www.ibbl.com.br/bebedouro-ibbl-compact-prata-13071001_prata/p', 'https://www.ibbl.com.br/bebedouro-ibbl-bag40-inox-01031001_inox/p', 'https://www.ibbl.com.br/bebedouro-ibbl-bag40c-inox-03031001_inox/p', 'https://www.ibbl.com.br/refil-ibbl-pre-c-3-25010002_outro/p', 'https://www.ibbl.com.br/refil-ibbl-c-5-24010003_outro/p', 'https://www.ibbl.com.br/refil-ibbl-cz-7-24010005_outro/p', 'https://www.ibbl.com.br/refil-avanti-ibbl-24010004_outro/p', 'https://www.ibbl.com.br/refil-ibbl-c-3-24010002_outro/p', 'https://www.ibbl.com.br/refresqueira-ibbl-bbs2-17031001_inox/p', 'https://www.ibbl.com.br/hot-dispenser-5-ou-chocolateira-ibbl-preto-22041001_preto/p']

    def get_items(self):
        driver = webdriver.Chrome()
        for link in self.links:
            driver.get(link)
            print(link)
            self.items.append(self.extract_item(driver))

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

    def extract_item(self, driver):
        EspList = {}
        no = "Not Found"

        try:
            nome = driver.find_elements_by_xpath(
                "//div[@class='x-name-product']")[0].text
        except IndexError as e:
            nome = no

        try:
            desc = driver.find_elements_by_xpath(
                "//div[@class='productDescription']")[0].text
        except IndexError as e:
            desc = no

        try:
            de = driver.find_elements_by_xpath(
                "//strong[@class='skuListPrice']")[0].text
        except IndexError as e:
            de = no

        try:
            por = driver.find_elements_by_xpath(
                "//strong[@class='skuBestPrice']")[0].text
        except IndexError as e:
            por = no

        EspList = dict(Nome=nome, Descrição=desc, Por=por, De=de)

        att = driver.find_elements_by_xpath(
            "//div[@id='mCSB_1_container']//span")
        cont = 1

        for x in att:
            if(":" in x.get_attribute('textContent')):
                y, z = x.get_attribute('textContent').split(":", 1)
                EspList[y] = z
            else:
                EspList["Atributo "+str(cont)] = x.get_attribute('textContent')

        att2 = driver.find_elements_by_xpath(
            "//div[@class='x-tab-table']//span")

        for x in att2:
            if(":" in x.get_attribute('textContent')):
                y, z = x.get_attribute('textContent').split(":", 1)
                EspList[y] = z
            else:
                EspList["Atributo "+str(cont)] = x.get_attribute('textContent')

        att3 = driver.find_elements_by_xpath("//div[@class='x-tab-table']//td")
        cont = 0

        for x in att3:
            if(cont % 2 == 0):
                ref = x.get_attribute('textContent')
            else:
                EspList[ref] = x.get_attribute('textContent')

            cont += 1

        img = driver.find_elements_by_xpath(
            "//ul[@class='thumbs slick-initialized slick-slider slick-dotted']//a//img")
        imgcont = 1
        for x in img:
            EspList["Imagem "+str(imgcont)] = x.get_attribute("src")
            imgcont += 1

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
