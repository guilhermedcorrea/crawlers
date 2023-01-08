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


def noblank(texto):
    if(texto != None):
        Noblank = " ".join(texto.split())
        return Noblank


def formatar(texto):
    texto = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]',
                   '', texto)
    texto = texto.strip(" ")
    texto = texto.strip(":: ")
    texto = texto.capitalize()
    unaccented_string = unidecode.unidecode(texto)
    return unaccented_string


class Organizer(object):
    def __init__(self, key):
        self.filename = "Bel lazer-Madeira.csv"
        self.Cods = ['Código', 'Codigo', 'Codigo do fornecedor', 'Codigo do fornecerdor', 'Gerais - Referência', ' • Referência',
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
        self.Clinks = {
            'Wap': 'https://busca.lojadomecanico.com.br/busca?q=wap'}
        self.Cats = ['Wap']
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None

    def timewarn(self):
        self.end_time = time.strftime("%b.%d-%X")
        print("Start : "+self.start_time + " End : "+self.end_time)

    def crawl(self):
        self.get_links()

    def crawl_to_file(self):
        self.crawl()

    def get_links(self):
        item_url_xpath = "//h2[@class='product-name']//a/@href"
        next_page_xpath = "//ul[@class='pagination']/li/a/@href"
        r = requests.get(self.start_url)
        html = parser.fromstring(r.text)

        for cats in self.Cats:
            print(self.Clinks[cats])

            r = requests.get(self.Clinks[cats])
            html = parser.fromstring(r.text)
            self.parse_links(html, item_url_xpath)
            try:
                next_page = html.xpath(next_page_xpath)
                next_page = next_page[len(next_page)-1]
            except IndexError as e:
                next_page = None

            old_page = ""

            while next_page:
                r = requests.get(next_page)
                html = parser.fromstring(r.text)
                self.parse_links(html, item_url_xpath)
                try:
                    next_page = html.xpath(next_page_xpath)
                    next_page = next_page[len(next_page)-1]
                    if(next_page == old_page):
                        next_page = None
                    old_page = next_page
                except IndexError as e:
                    next_page = None

            cats = "Mecanico-"+cats+".csv"
            cats = cats.replace("/", " e ")
            self.get_items(cats)

    def get_items(self, catname):
        self.items = []
        self.key = []
        print(self.links)
        for link in self.links:
            r = requests.get(link)
            html = parser.fromstring(r.text)
            print(str(r) + " : "+link)
            self.items.append(self.extract_item(html, link))
        self.save_items(catname)
        self.links = set()

    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    self.errors += 1
                else:
                    self.key.append(check)

    def extract_item(self, html, link):
        try:
            Nome = html.xpath("//h1[@class='product-name']")[0].text
        except IndexError as e:
            Nome = "Não Existe"

        try:
            CodRef = html.xpath(
                "//p[contains(text(),'Ref.:')]")[0].text.replace("Ref.: ", "")
        except IndexError as e:
            CodRef = "Não Existe"

        try:
            LMarca = html.xpath(
                "//div[@class='col-xs-12 col-sm-9 colzero']//strong//text()")
            IHA = len(LMarca) - 1
            Marca = LMarca[IHA].replace('\xa0', ' ')
        except IndexError as e:
            Marca = "Não Existe"

        try:
            De = html.xpath("//span[@class='preco-tabela']")[0].text
        except IndexError as e:
            De = "Not Found"

        try:
            Por = html.xpath("//span[@class='price']//text()")
        except:
            Por = "Não Existe"

        if(len(Por) > 3):
            fullPor = Por[0] + Por[1] + Por[2] + "," + Por[3]

        try:
            Desc = html.xpath(
                "//div[@class='col-xs-12 col-sm-9 colzero']//p[1]")[0].text
            if("• " in Desc or "- " in Desc):
                Desc = "Não Existe"
        except:
            Desc = "Não Existe"

        Prod_list = dict(CodRef=CodRef, Nome=Nome, Marca=Marca,
                         De=De, Por=fullPor, Descrição=Desc)

        Attr = html.xpath(
            "//div[@class='col-xs-12 col-sm-9 colzero']//p//text()")

        attrcont = 1
        CHEGA = 0
        conca = ""
        for check in Attr:
            if CHEGA < 1:
                check = check.strip("• ").strip("- ").strip(":: ").strip(" •")
                if len(check) > 1:
                    if "#" in check:
                        conca = formatar(check) + " , " + conca
                    elif 'Marca' in check:
                        CHEGA = 1
                    elif 'Técnicas' in check:
                        None
                    elif ':' in check:
                        ref, resp = check.split(':', 1)
                        Prod_list[formatar(ref)] = resp.replace(
                            '\xa0', ' ').strip(" ")
                    elif 'Tensão' in check and len(check) < 15:
                        Prod_list["Tensao"] = check.replace("Tensão ", "")
                    elif "Codigo" in check and len(check) < 20:
                        Prod_list["Codigo"] = check.replace(
                            "Codigo", "").replace("\xa0", "")
                    elif "Potência" in check and len(check) < 15:
                        Prod_list["Potencia"] = check.replace(
                            "Potência", "").strip(" ")
                    elif "Veja\n" in check or "*Imagens meramente ilustrativas" in check or "*Todas as informações divulgadas" in check:
                        None
                    else:
                        if(check == Prod_list["Descrição"]):
                            CHEGA = 0
                        else:
                            Prod_list["Atributo " +
                                      str(attrcont)] = check.replace('\xa0', ' ').strip(" ")
                            attrcont += 1

        if not conca == "":
            Prod_list["Atributo "+str(attrcont)] = conca

        IMGS = html.xpath("//ul[@class='img-produto-min']//img/@src")
        imgcont = 1
        for IMG in IMGS:
            Prod_list["Imagem " + str(imgcont)
                      ] = urlsplit(IMG)._replace(query="").geturl()
            imgcont += 1
        return Prod_list

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
        org = Organizer(self.key)
        fieldnames = org.Alinha()

        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


print("TIME TO START")
spider = EcommerceSpider(
    "https://www.lojadomecanico.com.br/mapa-do-site")
spider.crawl_to_file()

spider.timewarn()
