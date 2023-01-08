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


filee = "Docol"
base = "https://www.docol.com.br"
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
                       "SKU", "cat", "DescInfo", "Foto", "VIXI","DescriçãoLinha"]
        self.removed = []
        self.errors = 0
        self.start_time = time.time()
        self.testerror = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.cats = ["https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-antivandalismo","https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-antivandalismo-salvagua","https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-benefit","https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-classica","https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-classica-salvagua","https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-especial","https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-especial-salvagua","https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-linha-industrial","https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-salvagua-box","https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-sensor","https://www.docol.com.br/pt/linha/acabamento-para-valvula-de-descarga-square-salvagua","https://www.docol.com.br/pt/linha/acabamentos-para-valvula-de-descarga-luxus","https://www.docol.com.br/pt/linha/alcas-de-apoio","https://www.docol.com.br/pt/linha/alta-seguranca","https://www.docol.com.br/pt/linha/antivandalismo","https://www.docol.com.br/pt/linha/arabella","https://www.docol.com.br/pt/linha/arejador-economico","https://www.docol.com.br/pt/linha/argon","https://www.docol.com.br/pt/linha/argon-1","https://www.docol.com.br/pt/linha/banqueta-articulavel","https://www.docol.com.br/pt/linha/barra-de-apoio","https://www.docol.com.br/pt/linha/base-monocomando","https://www.docol.com.br/pt/linha/bellar","https://www.docol.com.br/pt/linha/bicas-docolmatic","https://www.docol.com.br/pt/linha/bicas-para-banheira","https://www.docol.com.br/pt/linha/bistro","https://www.docol.com.br/pt/linha/bistro-tech","https://www.docol.com.br/pt/linha/blend-flex","https://www.docol.com.br/pt/linha/blink","https://www.docol.com.br/pt/linha/bonnaducha","https://www.docol.com.br/pt/linha/bossanova","https://www.docol.com.br/pt/linha/breezy","https://www.docol.com.br/pt/linha/caixa-embutida","https://www.docol.com.br/pt/linha/chess","https://www.docol.com.br/pt/linha/chess-1","https://www.docol.com.br/pt/linha/ciclo-fixo","https://www.docol.com.br/pt/linha/complementos-1","https://www.docol.com.br/pt/linha/degusto","https://www.docol.com.br/pt/linha/desviador-para-chuveiro-especial","https://www.docol.com.br/pt/linha/dispensador-de-sabao-docolpresence","https://www.docol.com.br/pt/linha/dispensador-eletronico-de-sabao","https://www.docol.com.br/pt/linha/dispensador-para-sabonete-detergente-pressmatic","https://www.docol.com.br/pt/linha/dix","https://www.docol.com.br/pt/linha/doc","https://www.docol.com.br/pt/linha/doc-1","https://www.docol.com.br/pt/linha/docolbase-ceramico-dbc-1-2-volta","https://www.docol.com.br/pt/linha/docolchoice","https://www.docol.com.br/pt/linha/docolcity-1","https://www.docol.com.br/pt/linha/docolcity","https://www.docol.com.br/pt/linha/docolcozy","https://www.docol.com.br/pt/linha/docoleden","https://www.docol.com.br/pt/linha/docoleletric-embutida","https://www.docol.com.br/pt/linha/docoleletric-formatta","https://www.docol.com.br/pt/linha/docoleletric-torneira","https://www.docol.com.br/pt/linha/docoleletric-zenit","https://www.docol.com.br/pt/linha/docolflat","https://www.docol.com.br/pt/linha/docolgalaxi","https://www.docol.com.br/pt/linha/docolheaven","https://www.docol.com.br/pt/linha/docolidea","https://www.docol.com.br/pt/linha/docolkaila","https://www.docol.com.br/pt/linha/docolkaila-1","https://www.docol.com.br/pt/linha/docolmassima","https://www.docol.com.br/pt/linha/docolozonio","https://www.docol.com.br/pt/linha/docolprimor","https://www.docol.com.br/pt/linha/docolprimor-1","https://www.docol.com.br/pt/linha/docolresort","https://www.docol.com.br/pt/linha/docolspice","https://www.docol.com.br/pt/linha/docolspice-1","https://www.docol.com.br/pt/linha/docolstillo-1","https://www.docol.com.br/pt/linha/docoltronic-embutida","https://www.docol.com.br/pt/linha/docoltronic-formatta","https://www.docol.com.br/pt/linha/docoltronic-torneira","https://www.docol.com.br/pt/linha/docoltronic-zenit","https://www.docol.com.br/pt/linha/docolvitalis","https://www.docol.com.br/pt/linha/docolvitta","https://www.docol.com.br/pt/linha/ducha-higienica-especial-para-docolbase","https://www.docol.com.br/pt/linha/ducha-higienica-luxo-para-docolbase","https://www.docol.com.br/pt/linha/edge","https://www.docol.com.br/pt/linha/edge-1","https://www.docol.com.br/pt/linha/evoluto","https://www.docol.com.br/pt/linha/fiji","https://www.docol.com.br/pt/linha/fixador-antivandalismo","https://www.docol.com.br/pt/linha/gali","https://www.docol.com.br/pt/linha/gali-1","https://www.docol.com.br/pt/linha/genius-flex","https://www.docol.com.br/pt/linha/hope","https://www.docol.com.br/pt/linha/hotel","https://www.docol.com.br/pt/linha/invicta","https://www.docol.com.br/pt/linha/invicta-1","https://www.docol.com.br/pt/linha/itapema-bella-1","https://www.docol.com.br/pt/linha/itapema-bella","https://www.docol.com.br/pt/linha/joelhos-para-ligacao","https://www.docol.com.br/pt/linha/kit-misturador-para-chuveiro-com-joelho","https://www.docol.com.br/pt/linha/kit-misturador-para-chuveiro-roscavel","https://www.docol.com.br/pt/linha/kit-misturador-para-chuveiro-soldavel","https://www.docol.com.br/pt/linha/kit-misturador-para-ducha-higienica-ou-lavatorio-de-parede","https://www.docol.com.br/pt/linha/kit-suporte-monocomando-chuveiro-e-ban-chu","https://www.docol.com.br/pt/linha/lift","https://www.docol.com.br/pt/linha/lift-1","https://www.docol.com.br/pt/linha/lift-2","https://www.docol.com.br/pt/linha/ligacao-flexivel","https://www.docol.com.br/pt/linha/linha-industrial","https://www.docol.com.br/pt/linha/linha-industrial-1","https://www.docol.com.br/pt/linha/liss","https://www.docol.com.br/pt/linha/loggica-2","https://www.docol.com.br/pt/linha/loggica","https://www.docol.com.br/pt/linha/loggica-3","https://www.docol.com.br/pt/linha/loggica-1","https://www.docol.com.br/pt/linha/malta","https://www.docol.com.br/pt/linha/mangiare","https://www.docol.com.br/pt/linha/mangiare-tech","https://www.docol.com.br/pt/linha/minima","https://www.docol.com.br/pt/linha/misturador-docolbase-ppr-basetec","https://www.docol.com.br/pt/linha/misturador-termostatico","https://www.docol.com.br/pt/linha/misturadores-docolbase","https://www.docol.com.br/pt/linha/mix-match","https://www.docol.com.br/pt/linha/monet-1","https://www.docol.com.br/pt/linha/monet","https://www.docol.com.br/pt/linha/new-edge","https://www.docol.com.br/pt/linha/next","https://www.docol.com.br/pt/linha/nexus","https://www.docol.com.br/pt/linha/nova-pertutti","https://www.docol.com.br/pt/linha/nova-pertutti-1","https://www.docol.com.br/pt/linha/novita","https://www.docol.com.br/pt/linha/oasis-flex","https://www.docol.com.br/pt/linha/orbit","https://www.docol.com.br/pt/linha/parafusos-de-fixacao","https://www.docol.com.br/pt/linha/pedalmatic","https://www.docol.com.br/pt/linha/pematic","https://www.docol.com.br/pt/linha/pertutti-1","https://www.docol.com.br/pt/linha/pertutti","https://www.docol.com.br/pt/linha/pressmatic-antivandalismo","https://www.docol.com.br/pt/linha/pressmatic-chuveiros","https://www.docol.com.br/pt/linha/pressmatic-mictorios","https://www.docol.com.br/pt/linha/pressmatic-misturadores","https://www.docol.com.br/pt/linha/pressmatic-torneiras","https://www.docol.com.br/pt/linha/prime","https://www.docol.com.br/pt/linha/produtos-sugeridos-para-leed-1","https://www.docol.com.br/pt/linha/produtos-sugeridos-para-leed-6","https://www.docol.com.br/pt/linha/produtos-sugeridos-para-leed-2","https://www.docol.com.br/pt/linha/produtos-sugeridos-para-leed-5","https://www.docol.com.br/pt/linha/provence","https://www.docol.com.br/pt/linha/quad","https://www.docol.com.br/pt/linha/registro-de-gaveta-abnt","https://www.docol.com.br/pt/linha/registro-de-gaveta-docolbase","https://www.docol.com.br/pt/linha/registro-de-gaveta-europa","https://www.docol.com.br/pt/linha/registro-de-gaveta-industrial","https://www.docol.com.br/pt/linha/registro-de-pressao-1-400","https://www.docol.com.br/pt/linha/registro-de-pressao-docolbase","https://www.docol.com.br/pt/linha/registro-docolbase-basetec-pvc","https://www.docol.com.br/pt/linha/registro-docolbase-ppr-basetec","https://www.docol.com.br/pt/linha/registro-regulador-de-vazao","https://www.docol.com.br/pt/linha/registro-tipo-gaveta-docolbase-ppr-basetec","https://www.docol.com.br/pt/linha/registro-tipo-gaveta-docolbase-pvc-basetec","https://www.docol.com.br/pt/linha/registros-de-acionamento-restrito","https://www.docol.com.br/pt/linha/registros-docolmodular","https://www.docol.com.br/pt/linha/riva-1","https://www.docol.com.br/pt/linha/riva","https://www.docol.com.br/pt/linha/sifao-para-cozinha","https://www.docol.com.br/pt/linha/sifao-para-lavatorio","https://www.docol.com.br/pt/linha/sifao-para-tanque","https://www.docol.com.br/pt/linha/sifao-universal","https://www.docol.com.br/pt/linha/single","https://www.docol.com.br/pt/linha/skyline","https://www.docol.com.br/pt/linha/skyline-1","https://www.docol.com.br/pt/linha/solly","https://www.docol.com.br/pt/linha/square-1","https://www.docol.com.br/pt/linha/square","https://www.docol.com.br/pt/linha/square-2","https://www.docol.com.br/pt/linha/te-curto","https://www.docol.com.br/pt/linha/te-longo","https://www.docol.com.br/pt/linha/technoshower","https://www.docol.com.br/pt/linha/top","https://www.docol.com.br/pt/linha/torneira-boia-reforcada","https://www.docol.com.br/pt/linha/torneira-com-alavanca","https://www.docol.com.br/pt/linha/torneira-embutida-docolpresence","https://www.docol.com.br/pt/linha/torneira-pressmatic-benefit","https://www.docol.com.br/pt/linha/torneiras-de-acionamento-restrito","https://www.docol.com.br/pt/linha/torneiras-multiuso","https://www.docol.com.br/pt/linha/tradicional","https://www.docol.com.br/pt/linha/travessas-de-fixacao","https://www.docol.com.br/pt/linha/trio-1","https://www.docol.com.br/pt/linha/trio","https://www.docol.com.br/pt/linha/trip","https://www.docol.com.br/pt/linha/triplus-1","https://www.docol.com.br/pt/linha/triplus","https://www.docol.com.br/pt/linha/tubo-com-suporte-joelho-monocomando-para-chuveiro","https://www.docol.com.br/pt/linha/tubo-de-ligacao-para-bacia","https://www.docol.com.br/pt/linha/uno-1","https://www.docol.com.br/pt/linha/uno","https://www.docol.com.br/pt/linha/uno-2","https://www.docol.com.br/pt/linha/valencia-com-barra","https://www.docol.com.br/pt/linha/valvula-angular-para-hidrante","https://www.docol.com.br/pt/linha/valvula-antiretrossifonagem","https://www.docol.com.br/pt/linha/valvula-de-escoamento-de-cozinha","https://www.docol.com.br/pt/linha/valvula-de-esfera-com-alavanca-azul","https://www.docol.com.br/pt/linha/valvula-de-esfera-com-alavanca-vermelha","https://www.docol.com.br/pt/linha/valvula-de-retencao-horizontal","https://www.docol.com.br/pt/linha/valvula-de-retencao-universal","https://www.docol.com.br/pt/linha/valvula-de-retencao-vertical","https://www.docol.com.br/pt/linha/valvula-de-saida-d-agua-universal-para-lavatorio","https://www.docol.com.br/pt/linha/valvula-de-succao","https://www.docol.com.br/pt/linha/valvulas-de-descarga-docolbase","https://www.docol.com.br/pt/linha/vougan","https://www.docol.com.br/pt/linha/vougan-1"]
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
        for link in self.cats:
            item_url_xpath = "//a[@class='produto-imagem']/@href"
            next_page_xpath = "//a[@class='pagination-btn pagination-next']/@href"
            r = requests.get(link)
            html = parser.fromstring(r.text)
            self.parse_links(html, item_url_xpath)
            print(str(r) + " : " + link)
            try:
                next_page = html.xpath(next_page_xpath)[0]
            except IndexError as e:
                next_page = None
            while next_page:
                r = requests.get(link+next_page)
                html = parser.fromstring(r.text)
                self.parse_links(html, item_url_xpath)
                print(str(r) + " : " + link+next_page)
                try:
                    next_page = html.xpath(next_page_xpath)[0]
                except IndexError as e:
                    next_page = None
        print(len(self.links))


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
        no = "Not Found"

        try:
            nome = html.xpath(
                "//section[@class='produto-detalhe clearfix']//h3")[0].text
        except IndexError as e:
            nome = no

        try:
            sku = html.xpath("//span[@class='produto-cod']")[0].text
        except IndexError as e:
            sku = no

        try:
            linha = html.xpath("//*[@class='linha-nome']")[0].text
        except IndexError as e:
            linha = no

        try:
            DescLinha = html.xpath("//div[@class='box produto-linha']/p")[0].text
        except IndexError as e:
            DescLinha = no

        EspList = dict(Nome=nome, SKU=sku, Linha=linha, DescriçãoLinha=DescLinha)

        att = html.xpath("//div[@id='informacao-tecnica']//li")
        attcont = 1

        for x in att:
            if(x.text != None):
                if ":" in x.text:
                    y, z = x.text.split(":", 1)
                    EspList[y] = z
                else:
                    EspList["Atributo "+str(attcont)] = x.text
                    attcont += 1

        img = html.xpath("//ul[@id='thumblist']/li/a")
        imgcont = 1

        vcont = 1

        for x in img:
            try:
                a, b = x.attrib["rel"].split("largeimage: ", 1)
                b = b.strip("\'}").replace("/images/../uploads",
                                        "https://www.docol.com.br/uploads")
                EspList["Imagem "+str(imgcont)] = b
                imgcont += 1
            except KeyError as e:
                EspList["Video "+str(vcont)] = x.attrib["href"]
                vcont += 1

        downloads = html.xpath("//li[@class='icon-baixar']/a/@href")
        dcont = 1

        for x in downloads:
            EspList["Download "+str(dcont)] = x.replace("/images/../uploads",
                                                        "https://www.docol.com.br/uploads")
            dcont += 1

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
    "https://www.docol.com.br/")
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
