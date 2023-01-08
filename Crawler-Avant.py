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


filee = "Avant"
base = "http://avantlux.com.br/linha-de-produtos/todos-os-produtos/"
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
        self.links = ['http://avantlux.com.br/produto/kit-trilho-elegance/', 'http://avantlux.com.br/produto/trilho-elegance/', 'http://avantlux.com.br/produto/cage/', 'http://avantlux.com.br/produto/kavas/', 'http://avantlux.com.br/produto/spear/', 'http://avantlux.com.br/produto/nature/', 'http://avantlux.com.br/produto/pendente-lephare/', 'http://avantlux.com.br/produto/lephare/', 'http://avantlux.com.br/produto/bell/', 'http://avantlux.com.br/produto/pendente-bell/', 'http://avantlux.com.br/produto/tennessee/', 'http://avantlux.com.br/produto/baccino/', 'http://avantlux.com.br/produto/pendente-oka/', 'http://avantlux.com.br/produto/hash/', 'http://avantlux.com.br/produto/hash-2/', 'http://avantlux.com.br/produto/hash-3/', 'http://avantlux.com.br/produto/hash-4/', 'http://avantlux.com.br/produto/stove/', 'http://avantlux.com.br/produto/touch-light-signature/', 'http://avantlux.com.br/produto/touch-light-pocket/', 'http://avantlux.com.br/produto/lampiao/', 'http://avantlux.com.br/produto/luz-noturna-led/', 'http://avantlux.com.br/produto/lanterna/', 'http://avantlux.com.br/produto/lanterna-5w/', 'http://avantlux.com.br/produto/plafon-supimpa/', 'http://avantlux.com.br/produto/disco-supimpa/', 'http://avantlux.com.br/produto/arandela-supimpa/', 'http://avantlux.com.br/produto/luminaria-supimpa/', 'http://avantlux.com.br/produto/luminaria-de-mesa-supimpa/', 'http://avantlux.com.br/produto/pendente-supimpa/', 'http://avantlux.com.br/produto/spot-hummer/', 'http://avantlux.com.br/produto/spot-supimpa-3w/', 'http://avantlux.com.br/produto/spot-supimpa/', 'http://avantlux.com.br/produto/spot-supimpa-7w/', 'http://avantlux.com.br/produto/espeto-hummer-ip65/', 'http://avantlux.com.br/produto/luminaria-hummer-plus-ip65/', 'http://avantlux.com.br/produto/arandela-hummer-ip65/', 'http://avantlux.com.br/produto/light-engine/', 'http://avantlux.com.br/produto/luminaria-elegance/', 'http://avantlux.com.br/produto/luminaria-link-ho/', 'http://avantlux.com.br/produto/luminaria-link/', 'http://avantlux.com.br/produto/balizador-elegance/', 'http://avantlux.com.br/produto/balizador-elegance-4x4/', 'http://avantlux.com.br/produto/refletor-ip65/', 'http://avantlux.com.br/produto/painel-pop-embutir/', 'http://avantlux.com.br/produto/painel-pop-sobrepor/', 'http://avantlux.com.br/produto/painel-fit-embutir/', 'http://avantlux.com.br/produto/painel-fit-sobrepor/', 'http://avantlux.com.br/produto/painel-modular/', 'http://avantlux.com.br/produto/luz-noturna/', 'http://avantlux.com.br/produto/arandela-elegance/', 'http://avantlux.com.br/produto/luminaria-emergencia-smart/', 'http://avantlux.com.br/produto/luminaria-emergencia-pilha/', 'http://avantlux.com.br/produto/luminaria-emergencia-bloco/', 'http://avantlux.com.br/produto/fita-interna-ip20/', 'http://avantlux.com.br/produto/fita-externa-ip65/', 'http://avantlux.com.br/produto/high-bay-moon/', 'http://avantlux.com.br/produto/benjamin-cores/', 'http://avantlux.com.br/produto/benjamin-metalico/', 'http://avantlux.com.br/produto/pendente-farm/', 'http://avantlux.com.br/produto/pendente-capella/', 'http://avantlux.com.br/produto/pendente-canopus/', 'http://avantlux.com.br/produto/pendente-havai/', 'http://avantlux.com.br/produto/pendente-chamonix/',
                      'http://avantlux.com.br/produto/pendente-genebra/', 'http://avantlux.com.br/produto/pendente-zurique/', 'http://avantlux.com.br/produto/pendente-algebar/', 'http://avantlux.com.br/produto/pendente-bellatrix/', 'http://avantlux.com.br/produto/pendente-betel/', 'http://avantlux.com.br/produto/pendente-anfora/', 'http://avantlux.com.br/produto/borgonha/', 'http://avantlux.com.br/produto/pendente-fraconia/', 'http://avantlux.com.br/produto/pendente-flaschen/', 'http://avantlux.com.br/produto/pendente-martulus/', 'http://avantlux.com.br/produto/pendente-yalova/', 'http://avantlux.com.br/produto/pendente-urano/', 'http://avantlux.com.br/produto/pendente-veneza/', 'http://avantlux.com.br/produto/pendente-adana/', 'http://avantlux.com.br/produto/pendente-manisa/', 'http://avantlux.com.br/produto/pendente-ankara/', 'http://avantlux.com.br/produto/pendente-istambul/', 'http://avantlux.com.br/produto/pendente-rize/', 'http://avantlux.com.br/produto/pendente-arizona/', 'http://avantlux.com.br/produto/pendente-adhara/', 'http://avantlux.com.br/produto/aldebaran/', 'http://avantlux.com.br/produto/pendente-dolium/', 'http://avantlux.com.br/produto/pendente-electra/', 'http://avantlux.com.br/produto/pendente-kaus/', 'http://avantlux.com.br/produto/pendente-kras/', 'http://avantlux.com.br/produto/pendente-rana/', 'http://avantlux.com.br/produto/pendente-farwest/', 'http://avantlux.com.br/produto/pendente-menkar/', 'http://avantlux.com.br/produto/pendente-mira/', 'http://avantlux.com.br/produto/pendente-terra/', 'http://avantlux.com.br/produto/pendente-texas/', 'http://avantlux.com.br/produto/pendente-barcelona/', 'http://avantlux.com.br/produto/pendente-ibiza/', 'http://avantlux.com.br/produto/arandela-ibiza/', 'http://avantlux.com.br/produto/pendente-dijon/', 'http://avantlux.com.br/produto/pendente-moscou/', 'http://avantlux.com.br/produto/pendente-aston/', 'http://avantlux.com.br/produto/pendente-nice/', 'http://avantlux.com.br/produto/pendente-paris/', 'http://avantlux.com.br/produto/arandela-cristal/', 'http://avantlux.com.br/produto/pendente-polaris/', 'http://avantlux.com.br/produto/pendente-espelho/', 'http://avantlux.com.br/produto/pera-led/', 'http://avantlux.com.br/produto/pera-12v/', 'http://avantlux.com.br/produto/bulbo/', 'http://avantlux.com.br/produto/dicroica/', 'http://avantlux.com.br/produto/tubular-t8/', 'http://avantlux.com.br/produto/lampada-bolinha-led/', 'http://avantlux.com.br/produto/lampada-vela-led/', 'http://avantlux.com.br/produto/lampada-par20-led/', 'http://avantlux.com.br/produto/lampada-par30/', 'http://avantlux.com.br/produto/lampada-par38-led/', 'http://avantlux.com.br/produto/lampada-led-retro-globo-e-bolinha/', 'http://avantlux.com.br/produto/retro-copia/', 'http://avantlux.com.br/produto/retro-tubular/', 'http://avantlux.com.br/produto/retro-luxping-g9/', 'http://avantlux.com.br/produto/retro-vela/', 'http://avantlux.com.br/produto/lampada-cfli-3u/', 'http://avantlux.com.br/produto/lampada-cfli-espiral/', 'http://avantlux.com.br/produto/lampada-bulbo-halogena/', 'http://avantlux.com.br/produto/lampada-vapor-de-sodio-tubular/', 'http://avantlux.com.br/produto/multi-vapor-metalico/', 'http://avantlux.com.br/produto/vapor-de-mercurio/']

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
            nome = html.xpath(
                "//h1[@class='product_title entry-title']")[0].text
        except IndexError as e:
            nome = no

        try:
            desc = html.xpath(
                "//div[@class='woocommerce-product-details__short-description']//p")
            fulldesc = ""
            for x in desc:
                if(x.text != None):
                    if(len(x.text) > 1):
                        fulldesc += x.text + " <br> "
                    if("Ficha Técnica" in x.text):
                        print("IHAA")

        except IndexError as e:
            desc = no
        EspList = dict(Nome=nome, Descrição=fulldesc)

        attr = html.xpath("//table[@class='shop_attributes']//tr")

        for att in attr:
            ref = att[0].text
            val = att[1][0].text
            EspList[ref] = val

        imgs = html.xpath(
            "//figure[@class='woocommerce-product-gallery__wrapper']//img/@src")
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
