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


FILENAME = "Cadastro Doural.csv"


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
        self.filename = "S-Doural.csv"
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
        self.links = {}
        self.CodRef = []
        self.items = []
        self.start_url = start_url
        self.set_base_url()
        self.key = []
        self.errors = 0
        self.prelinks = {}
        self.start_time = time.time()
        self.testerror = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.file = "Doural.csv"

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
        self.CSVREADER()

    def get_items(self):
        for ID in self.CodRef:
            r = requests.get(self.links[ID])
            html = parser.fromstring(r.text)
            print(str(r) + " : " + self.links[ID])
            self.items.append(self.extract_item(html, self.links[ID], ID))

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

    def extract_item(self, html, link, ID):
        EspList = {}
        try:
            nome = html.xpath("//div[contains(@class,'productName')]")[0].text
        except IndexError as e:
            nome = "Não Encontrado"
        try:
            desc = html.xpath("//div[@class='productDescription']")[0].text
        except IndexError as e:
            desc = "Não Encontrado"

        atr = html.xpath("//div[@id='caracteristicas']/table//tr")
        imgs = html.xpath("//ul[@class='thumbs']/li/a/img/@src")
        imgcont = 1
        EspList = dict(Nome=nome, Descrição=desc, CodRef=ID)

        for img in imgs:
            EspList["Imagem "+str(imgcont)] = img.replace("-80-80", "-800-800")
            imgcont += 1

        for x in atr:
            if("Especificação Técnica" not in x[0].text):
                EspList[x[0].text] = x[1].text

        especif = html.xpath(
            "//td[@class='value-field Especificacao-Tecnica']//text()")
        control = 0
        cont = 1
        for x in especif:
            if(":" in x):
                a, b = x.replace("\r", "").strip(
                    '"').strip("-").strip(" ").split(":", 1)
                EspList[a] = b.strip('"').strip("-").strip(" ")
            elif x == "\r":
                None
            elif control == 0:
                ref = x.replace("\r", "").strip('"')
                control = 1
            elif control == 1:
                EspList[ref] = x
                control = 0
            else:
                EspList["Atributo "+str(cont)] = x
                cont += 1

        teste = dict(EspList)
        teste = self.clearshit(teste)
        EspList["JSON"] = self.JSON_CREATE(teste)

        return EspList

    def clearshit(self, dic):
        for x in dic.keys():
            if x in self.remove:
                self.removed.append(x)
            if "Image" in x:
                self.removed.append(x)

        for a in self.removed:
            dic.pop(a, None)

        return dic

    def parse_links(self, html, item_url_xpath, ID):
        new_links = html.xpath(item_url_xpath)[1]
        self.links[ID] = self.prepare_url(new_links)
        print(self.links[ID])

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

spider = EcommerceSpider("Não Tem")
spider.crawl_to_file(FILENAME)

spider.timewarn()
