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


brands = ["docol"]

B_ULR = "https://www.madeiramadeira.com.br/busca?q="
B_FILENAME = "-Madeira.csv"


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
        self.Cods = ['MPN_Google', 'Código', 'Gerais - Referência', ' • Referência',
                     'Referência', ' Referência', 'Cod_Secundario', 'CodRef', 'Codref', 'Código de barras', 'EAN', 'Ean', 'Código De Barras']
        self.basic = ['JSON', 'Nome', 'Name', 'Descrição',
                      'Marca', 'Categoria', 'Categoria_Google', 'Image_Google', 'SKU_Google', 'De', 'Por']
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

    def timewarn(self):
        self.end_time = time.strftime("%b.%d-%X")
        print("Start : "+self.start_time + " End : "+self.end_time)

    def JSON_CREATE(self, dic):
        JSON = json.dumps(dic, ensure_ascii=False)
        div = "<div class='especif'>"+JSON+"</div>"
        return div

    def crawl(self):
        self.get_links()
        self.get_items()

    def crawl_to_file(self, filename):
        self.crawl()
        self.save_items(filename)

    def get_links(self):
        item_url_xpath = "//div[@class='product__image']/a/@href"
        next_page_xpath = "//ul[@class='pagination']/li//a[@rel='next']/@href"
        r = requests.get(self.start_url)
        html = parser.fromstring(r.text)
        self.parse_links(html, item_url_xpath)
        print(str(r))
        try:
            next_page = html.xpath(next_page_xpath)[0]
        except IndexError as e:
            next_page = None
        while next_page:
            r = requests.get(urljoin(self.base_url, next_page))
            html = parser.fromstring(r.text)
            self.parse_links(html, item_url_xpath)
            print(str(r) + " : " + next_page)
            try:
                next_page = html.xpath(next_page_xpath)[0]
            except IndexError as e:
                next_page = None

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

    def extract_item(self, html, link):
        EspList = {}

        try:
            name = html.xpath(
                "//h1[@class='title is-medium product-title']")[0]
            name = blank(name.text)
        except IndexError as e:
            # print("name not found at page %s" % link)
            name = "Not found"
        try:
            De = html.xpath(
                "// div[@class='section-price']/p[@class='text is-darkless is-small']/del")[0].text
        except IndexError as e:
            De = "Not Found"

        try:
            Por = html.xpath(
                "//span[@class='incash-payment-info']//strong")[0].text
        except IndexError as e:
            Por = "Not Found"

        try:
            CodRef = html.xpath(
                "//span[2][@class='reference-block__item']")[0]
            CodRef = blank(CodRef.text)
        except IndexError as e:
            # print("CodRef not found at page %s" % link)
            CodRef = "Not found"

        try:
            attribute = html.xpath(
                "//div[1][@id='product-attributes-tab-information']/table/tbody")
        except IndexError as e:
            print("Attributos não encontrados na pagina $s" % link)

        try:
            Img = html.xpath("//div/@data-image-zoom")
        except IndexError as e:
            Img = "Not Found"

        EspList = dict(Name=name, CodRef=CodRef, De=De,
                       Por=Por)

        try:
            description = html.xpath(
                "//section[@class='section product__attributes is-compact is-hidden-mobile']//div[@class='product-description']/p[@class='description']/text()")
            contattr = 1
            if len(description) > 1:
                for attr in description:
                    if attr.count(":") > 1:
                        EspList["Attributo "+str(contattr)] = attr
                        contattr += 1
                    elif ':' in attr:
                        ref, val = attr.split(":")
                        EspList[formatar(ref)] = val
                    else:
                        EspList["Attributo "+str(contattr)] = attr
                        contattr += 1
                if(EspList.get("Código") != None):
                    if(len(EspList['Código']) > 0):
                        EspList['Código'] = re.sub(
                            "[^0-9]", "", EspList['Código'])
                    EspList["Descrição"] = " Not Found"
            else:
                description = blank(description[0])
                EspList["Descrição"] = description

        except IndexError as e:
            # print("Name not found at page %s" % link)
            description = "Not found"

        cont = 1
        for imagem in Img:
            Texto = "Imagem "+str(cont)
            EspList[Texto] = str(imagem)
            cont += 1

        try:
            for x in attribute[0]:
                if(x[1].text != None):
                    EspList[formatar(x[0][0].text)] = blank(x[1].text)
                else:
                    EspList[formatar(x[0][0].text)] = 0
        except IndexError as e:
            print(e)

        try:
            CatTree = html.xpath("//nav[@class='breadcrumb is-small']//li/a")
            Category = ""

            for tree in CatTree:
                Category = Category + " > " + blank(tree.text)

            EspList["Categoria"] = Category

        except IndexError as e:
            CatTree = "Not Found"

        try:
            CodRef_sec = blank(html.xpath(
                "//nav[@class='breadcrumb is-small']//li[@class='is-active']/a")[0].text)
            EspList["Cod_Secundario"] = CodRef_sec
        except IndexError as e:
            CodRef_sec = "Not Found"

        try:
            Json_madeira = html.xpath(
                "//script[@id='schema-google-merchant']")[0].text
            Json_madeira = json.loads(Json_madeira)

            EspList["SKU_Google"] = Json_madeira["sku"]
            EspList["MPN_Google"] = Json_madeira["mpn"]
            EspList["Image_Google"] = Json_madeira["image"]
            EspList["Categoria_Google"] = Json_madeira["category"]

        except IndexError as e:
            Json_madeira = "Not Found"

        EspList["JSON"] = self.JSON_CREATE(EspList)

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
        with open(filename, 'w', encoding="utf-8") as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


print("LETS GET IT STARTED")

for do in brands:
    spider = EcommerceSpider(B_ULR + do)

    FILENAME = do + B_FILENAME
    spider.crawl_to_file(FILENAME)

spider.timewarn()
