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


FILENAME = "Naymulti.csv"


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
        self.key = ["Material: ", "Material:"]
        self.remove = ["Descrição 2", "Categoria", "Descrição2",
                       "SKU", "cat", "DescInfo", "Foto", "VIXI"]
        self.removed = []
        self.errors = 0
        self.prelinks = {}
        self.start_time = time.time()
        self.testerror = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.file = "nay.csv"

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

    def extract_item(self, html, link, ID):
        EspList = {}
        try:
            nome = html.xpath("//h1[@class='product-name']")[0].text
        except IndexError as e:
            nome = "Não Encontrado"
        try:
            marca = html.xpath(
                "//span[@class='dados-valor brand']/a/strong")[0].text
        except IndexError as e:
            marca = "Não Encontrado"
        try:
            linha = html.xpath("//strong[@class='dados-valor']")[0].text
        except IndexError as e:
            linha = "Não Encontrado"

        EspList = dict(Nome=nome, Marca=marca, Linha=linha, ID=ID)

        atr = html.xpath("//div[@id='descricao']//span//text()")
        concat = ""
        flag = 0
        cont = 0
        prox = 0

        check = len(html.xpath(
            "//div[@id='descricao']/div/div/p/span/span/span[@style='font-size:12px;']"))
        for elem in atr:
            if("Material: " in elem):
                print(link)
            if(check > 0):
                elem = elem.replace("\r\n\xa0", "")
                if("\xa0" in elem and ":"in elem):
                    ref = elem.replace("\xa0", "").strip(": ")
                    prox = 1
                elif("\xa0" in elem):
                    EspList[ref] = elem.replace("\r\n", "").replace("\xa0", "")
                elif(prox == 1):
                    EspList[ref] = elem.replace("\r\n", "").replace("\xa0", "")
                    prox = 0
                elif(":" in elem):
                    ref = elem.replace("\r\n", "").replace("\xa0", "")
            else:
                if("\r\n" in elem and ":" in elem):
                    elem = elem.replace("\r\n", "").replace("\xa0", "")
                    x, y = elem.split(":", 1)
                    EspList[x.strip(": ")] = y
                    concat = ""
                elif "\r\n" in elem:
                    concat += elem.replace("\r\n", "") + " | "
                elif(flag == 1):
                    EspList[ref] = concat.replace(
                        "\xa0", "").replace("\r\n", "")
                    ref = elem
                    concat = ""
                elif(":" in elem):
                    ref = elem.strip(": ")
                    flag = 1
                cont += 1
                if(cont == len(atr)):
                    EspList[ref] = concat.replace(
                        "\xa0", "").replace("\r\n", "")

        imgs = html.xpath("//span[@class='produto-imagem-miniatura']/a/@href")
        imgcont = 1

        for img in imgs:
            EspList["Imagem "+str(imgcont)] = img
            imgcont += 1

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

    def JSON_CREATE(self, dic):
        JSON = json.dumps(dic, ensure_ascii=False)
        div = "<div class='especif'>"+JSON+"</div>"
        return div

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
        fieldnames.extend(("Material: ", ' Proteção duradoura contra Ácaros por toda vida útil do Tapete;',
                           'Comprimento: ', ' O tapete\xa0faz parte da linha de\xa0produtos São Carlos\xa0uma empresa especializada em produzir tapetes para todos os ambientes domésticos ,uma empresa que atua no mercado oferecendo produtos diferenciados e de alta qualidade', ' Conforto no Uso, Evita Riscos nos Pisos de Madeira ou Laminados;', ' UV- Oferece Maior Resistência ao Desbotamento Provocado Pela Ação da Luz;', 'Largura: ', ' Polipropileno Fio Roselan;', ' Evita Riscos Nos Pisos de Madeira ou Laminados;', ' Antideslizante evita que o tapete deslize em pisos lisos;'))
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


print("LETS GET IT STARTED")

spider = EcommerceSpider("Não Tem")
spider.crawl_to_file(FILENAME)

spider.timewarn()
