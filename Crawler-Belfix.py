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


brands = ["bLACK dECKER"]

ULR = "https://www.madeiramadeira.com.br/busca?q="
FILENAME = "Belfix-ALL.csv"


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


def clear(texto):
    texto = texto.replace("\r", "").replace("\n", "").replace("\x94", "").replace(
        "\t", "").replace("\xa0", "").strip("•").replace("\x81", "").strip(".").strip(" ")
    return texto


class Organizer(object):
    def __init__(self, key):
        self.filename = "Bel lazer-Madeira.csv"
        self.Cods = ['Código', 'Gerais - Referência', 'Ref', ' • Referência',
                     'Referência', 'Referencia', ' Referência', 'Cod_Secundario', 'CodRef', 'Codref', 'Código de barras', 'EAN', 'Ean', 'Código De Barras']
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
        self.catlinks = ['https://www.belfix.com.br/produtos/cat/84/Ferramentas', 'https://www.belfix.com.br/produtos/cat/22/Casa-e-Jardim', 'https://www.belfix.com.br/produtos/cat/23/Piscina-e-Inflaveis',
                         'https://www.belfix.com.br/produtos/cat/24/Brinquedos', 'https://www.belfix.com.br/produtos/cat/26/Esporte', 'https://www.belfix.com.br/produtos/cat/27/Praia-Camping', 'https://www.belfix.com.br/produtos/cat/29/Marcas-licenciadas']
        self.start_time = time.time()
        self.testerror = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

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
        item_url_xpath = "//div[@id='content']//div[@class='produto']/a/@href"

        for links in self.catlinks:
            r = requests.get(links, headers=self.header)
            r.encoding = 'utf-8'
            html = parser.fromstring(r.text)
            self.parse_links(html, item_url_xpath)

    def get_items(self):
        with open("CORRIGIR.csv", 'w', encoding="utf-8") as f:
            dict_writer = csv.writer(f, delimiter=';')
            dict_writer.writerows(self.testerror)

        for link in self.links:
            r = requests.get(link, headers=self.header)
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
            name = html.xpath(
                "//*[@id='dados_produtos']/h2")[0].text
            EspList["Nome"] = name
            #name = blank(name.text)
        except IndexError as e:
            # print("name not found at page %s" % link)
            name = "Not found"

        try:
            Imgs = html.xpath("//div[@id='galeria_produto']/div/a/img/@src")
            imgcont = 1
            for img in Imgs:
                EspList["Imagem " + str(imgcont)] = img
                imgcont += 1
        except IndexError as e:
            Imgs = "Not Found"

        try:
            check = html.xpath("//div[@id='dados_produtos']/ul")[0]
        except IndexError as e:
            check = []

        if len(check) > 0:
            print("Tipo 1")
            Atributos = html.xpath(
                "//div[@id='content']//div[@id='dados_produtos']/ul/li/span//text()")
            refcont = 1
            cont = 1
            cont_conteudo = 1
            for x in Atributos:
                x = x.replace("\xa0", "").strip(" ")
                a = x[0:1]
                if x == None or x == "":
                    None
                elif a.isdigit():
                    EspList["Conteudo " + str(cont_conteudo)] = x
                    cont_conteudo += 1
                elif "Ref" in x:
                    EspList["Referencia "+str(refcont)] = x.strip("Ref. ")
                    refcont += 1
                elif ":" in x:
                    a, b = x.split(":", 1)
                    EspList[clear(a)] = clear(b)
                elif "Peso" in x:
                    EspList["Peso"] = clear(x.replace(
                        "Peso", ""))
                else:
                    EspList["Atributo "+str(cont)] = clear(x)
                    cont += 1
        else:

            check2 = html.xpath(
                "//div[@id='content']//div[@id='dados_produtos']/p/span")
            refcont = 1
            cont = 1
            cont_conteudo = 1
            qtdcont = 0
            QTD = len(check2)
            if QTD > 2:
                print("Tipo 2")
                Atributos = html.xpath(
                    "//div[@id='content']//div[@id='dados_produtos']/p//text()")
                concat = ""
                for x in Atributos:
                    if not x == None:  # print(a + " " + str(a.isdigit()))
                        x = x.replace("\xa0", "")
                        if x == "\r\n\t":
                            a = concat[0:2]
                            if concat == "":
                                None
                            elif a.isdigit():
                                EspList["Conteudo " +
                                        str(cont_conteudo)] = concat
                                cont_conteudo += 1
                            elif "Ref" in concat:
                                EspList["Referencia " +
                                        str(refcont)] = concat.strip("Ref. ").strip("-").strip(" ")
                                refcont += 1
                            elif ":" in concat:
                                a, b = concat.replace("\xa0", "").split(":", 1)
                                EspList[clear(a)] = clear(b)
                            else:
                                EspList["Atributo "+str(cont)] = clear(concat)
                                cont += 1
                            concat = ""
                        else:
                            concat += x
                        if qtdcont == (len(Atributos)-1) and concat != "":
                            a = concat[0:2]
                            if concat == "":
                                None
                            elif a.isdigit():
                                EspList["Conteudo " +
                                        str(cont_conteudo)] = concat
                                cont_conteudo += 1
                            elif "Ref" in concat:
                                EspList["Referencia " +
                                        str(refcont)] = concat.strip("Ref. ").strip("-").strip(" ")
                                refcont += 1
                            elif ":" in concat:
                                a, b = concat.replace("\xa0", "").split(":", 1)
                                EspList[clear(a)] = clear(b)
                            elif "Peso" in x:
                                EspList["Peso"] = clear(x.replace(
                                    "Peso", ""))
                            else:
                                EspList["Atributo "+str(cont)] = clear(concat)
                                cont += 1
                            concat = ""
                        qtdcont += 1

            else:
                print("Tipo 3")
                Atributos = html.xpath(
                    "//div[@id='content']//div[@id='dados_produtos']/p")
                for x in Atributos:
                    if x.text == None:
                        None
                    elif "Ref" in x.text:
                        EspList["Referencia " +
                                str(refcont)] = clear(x.text.strip("Ref. "))
                        refcont += 1
                    elif ":" in x.text:
                        a, b = x.text.replace("\xa0", "").split(":", 1)
                        EspList[clear(a)] = clear(b)
                    elif "Peso" in x.text:
                        EspList["Peso"] = clear(x.text.replace(
                            "Peso", ""))
                    else:
                        EspList["Atributo "+str(cont)] = clear(x.text)
                        cont += 1
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
        print(self.items)
        org = Organizer(self.key)
        fieldnames = org.Alinha()
        print(fieldnames)
        with open(filename, 'w', encoding="utf-8") as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


spider = EcommerceSpider(ULR)
spider.crawl_to_file(FILENAME)

spider.timewarn()
