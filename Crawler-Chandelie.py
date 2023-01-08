import lxml.html as parser
import requests
import csv
import time
import re
import unidecode
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


B_ULR = "https://www.madeiramadeira.com.br/busca?q="


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
        self.filename = "Chadelie 3.csv"
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
        self.links = set()
        self.items = []
        self.start_url = start_url
        self.set_base_url()
        self.key = []
        self.errors = 0
        self.start_time = time.time()
        self.testerror = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.catlinks = ['https://chandelie.com.br/categoria-produto/pendentes/louis-pendentes/', 'https://chandelie.com.br/categoria-produto/nova-colecao/bello/', 'https://chandelie.com.br/categoria-produto/nova-colecao/mykonos/', 'https://chandelie.com.br/categoria-produto/arandelas/loki/', 'https://chandelie.com.br/categoria-produto/arandelas/bruxelas/', 'https://chandelie.com.br/categoria-produto/plafons/corallo-plafons/', 'https://chandelie.com.br/categoria-produto/pendentes/broom-pendentes/', 'https://chandelie.com.br/categoria-produto/pendentes/londres/', 'https://chandelie.com.br/categoria-produto/pendentes/nuremberg/', 'https://chandelie.com.br/categoria-produto/nova-colecao/cristalli/', 'https://chandelie.com.br/categoria-produto/arandelas/orbital-arandelas/', 'https://chandelie.com.br/categoria-produto/lustres/atenas/', 'https://chandelie.com.br/categoria-produto/plafons/monterey/', 'https://chandelie.com.br/categoria-produto/nova-colecao/kiezza/', 'https://chandelie.com.br/categoria-produto/arandelas/lescaut/', 'https://chandelie.com.br/categoria-produto/pendentes/kiezza-pendentes/',
                         'https://chandelie.com.br/categoria-produto/nova-colecao/corallo/', 'https://chandelie.com.br/categoria-produto/arandelas/darling-arandelas/', 'https://chandelie.com.br/categoria-produto/arandelas/copenhage/', 'https://chandelie.com.br/categoria-produto/arandelas/dueto/', 'https://chandelie.com.br/categoria-produto/abajour/los-angeles/', 'https://chandelie.com.br/categoria-produto/pendentes/nova-delhi/', 'https://chandelie.com.br/categoria-produto/pendentes/pylon-pendentes/', 'https://chandelie.com.br/categoria-produto/pendentes/flat-pendentes/', 'https://chandelie.com.br/categoria-produto/nova-colecao/diva/', 'https://chandelie.com.br/categoria-produto/lustres/chamonix/', 'https://chandelie.com.br/categoria-produto/pendentes/mykonos-pendentes/', 'https://chandelie.com.br/categoria-produto/pendentes/spazio-pendentes/', 'https://chandelie.com.br/categoria-produto/pendentes/xangai/', 'https://chandelie.com.br/categoria-produto/pendentes/cristalli-pendentes/', 'https://chandelie.com.br/categoria-produto/plafons/atenas-plafons/']

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
        for link in self.catlinks:
            item_url_xpath = "//a[@class='woocommerce-LoopProduct-link woocommerce-loop-product__link']/@href"
            next_page_xpath = "//a[@class = 'next page-numbers']/@href"
            r = requests.get(link)
            r.encoding = 'utf-8'
            html = parser.fromstring(r.text)
            self.parse_links(html, item_url_xpath)
            try:
                next_page = html.xpath(next_page_xpath)[0]
            except IndexError as e:
                next_page = None
            while next_page:
                r = requests.get(urljoin(self.base_url, next_page))
                r.encoding = 'utf-8'
                html = parser.fromstring(r.text)
                self.parse_links(html, item_url_xpath)
                try:
                    next_page = html.xpath(next_page_xpath)[0]
                except IndexError as e:
                    next_page = None

    def get_items(self):
        with open("CORRIGIR.csv", 'w', encoding="utf-8") as f:
            dict_writer = csv.writer(f, delimiter=';')
            dict_writer.writerows(self.testerror)

        for link in self.links:
            r = requests.get(link)
            r.encoding = 'utf-8'
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

    def extract_item(self, html, link):
        EspList = {}
        try:
            Nome = html.xpath("//div[@class='lec_gold']")[0].text
        except IndexError as e:
            Nome = "Not Found"
        try:
            sku = html.xpath("//span[@class='sku']")[0].text
        except IndexError as e:
            sku = "Not Found"
        Categoria = html.xpath("//span[@class='posted_in']//text()")
        conCAT = ""
        for texto in Categoria:
            conCAT += texto

        TAG = html.xpath("//span[@class='tagged_as']//text()")
        conTAG = ""

        for texto in TAG:
            conTAG += texto

        EspList = dict(Nome=Nome, SKU=sku, Categoria=conCAT, Tags=conTAG)

        Desc = html.xpath(
            "//div[@class='woocommerce-product-details__short-description']//p")

        for element in Desc:
            if ":" in element.text:
                x, y = element.text.split(":", 1)
                EspList[x] = y

        IMG = html.xpath(
            "//div[@class='woocommerce-product-gallery__image']/a/img")
        imgcont = 1
        cont = 1
        for imgs in IMG:
            src = imgs.attrib["src"]
            EspList["Imagem "+str(imgcont)] = src
            checkattr = html.xpath(
                "//div[@class='woocommerce-product-gallery__image']/a/img/@srcset")
            if(len(checkattr) > 0):
                complemento = imgs.attrib["srcset"].split(",")
                for x in complemento:
                    EspList["Imagem "+str(imgcont) +
                            " Complemento "+str(cont)] = x
                    cont += 1
                imgcont += 1

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
        with open(org.filename, 'w', encoding="utf-8") as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


print("LETS GET IT STARTED")


spider = EcommerceSpider(B_ULR)
spider.crawl_to_file("AA")

spider.timewarn()
