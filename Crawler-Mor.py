import lxml.html as parser
import requests
import csv
import time
import re
import unidecode
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


brands = ["bLACK dECKER"]

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
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.cats = ['https://www.lojamor.com.br/termicos', 'https://www.lojamor.com.br/verao',  'https://www.lojamor.com.br/churrasco', 'https://www.lojamor.com.br/cozinha', 'https://www.lojamor.com.br/utilidades', 'https://www.lojamor.com.br/lavanderia',
                     'https://www.lojamor.com.br/escadas', 'https://www.lojamor.com.br/moveis', 'https://www.lojamor.com.br/fitness', 'https://www.lojamor.com.br/esporte', 'https://www.lojamor.com.br/kids', 'https://www.lojamor.com.br/promocao']

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
        driver = webdriver.Chrome(
            'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe')
        for Cat in self.cats:
            driver.get(Cat)

            check = driver.find_elements_by_xpath(
                "//div[@class='listagem-loadMoreBtn' and contains(@style,'display: none')]")

            while(len(check) < 1):
                element = WebDriverWait(driver, 10).until_not(EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='listagem-loadMoreBtn loading']")))
                check = driver.find_elements_by_xpath(
                    "//div[@class='listagem-loadMoreBtn' and contains(@style,'display: none')]")
                if(len(check) < 1):
                    time.sleep(1.5)
                    input_element = driver.find_elements_by_xpath(
                        "//div[@class='listagem-loadMoreBtn']")[0]
                    input_element.click()

            new_links = driver.find_elements_by_xpath(
                "//a[@class='shelf-item__img-hover']")
            Href = []
            for link in new_links:
                Href.append(link.get_attribute("href"))

            self.parse_links(Href)
        driver.quit()

    def get_items(self):
        print(self.links)
        print(len(self.links))
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
                "//span[@class='product-name__name']/div")[0]
            name = blank(name.text)
        except IndexError as e:
            # print("name not found at page %s" % link)
            name = "Not found"

        try:
            CodRef = html.xpath(
                "//div[contains(@class,'productReference ')]")[0]
            CodRef = blank(CodRef.text)
        except IndexError as e:
            CodRef = "Not Found"

        try:
            Categoria = html.xpath("//div[@class='bread-crumb']//li/a")
            AllCat = ""
            for juntacat in Categoria:
                AllCat += " > " + juntacat.text
        except IndexError as e:
            Categoria = "Not Found"

        try:
            Por = html.xpath("//strong[@class='skuBestPrice']")[0].text
        except IndexError as e:
            Por = "Not Found"

        try:
            Desc = html.xpath("//div[@class='productDescription']")[0].text
        except IndexError as e:
            Desc = "Not Found"

        EspList = dict(Nome=name, CodRef=CodRef,
                       Categoria=AllCat, Por=Por, Descrição=Desc)

        try:
            Attr = html.xpath(
                "//div[@class='product-specification']//table//tr")
            for linha in Attr:
                EspList[linha[0].text] = linha[1].text
        except IndexError as e:
            Attr = "Not Found"

        try:
            Attr_Complement = html.xpath(
                "//div[@class='product-specification']//table//tr//td//text()")
            contador = 0
            watcher = []
            checkwatcher = {}
            prevcheck = ""
            for check in Attr_Complement:
                checkwatcher[check] = ""
                if(check in EspList.values()):
                    watcher.insert(contador, check)
                    contador += 1
                    prevcheck = check
                else:
                    checkwatcher[prevcheck] += check + " | "

            for teste in checkwatcher.keys():
                if(len(checkwatcher[teste]) > 2):
                    for iterator in EspList.keys():
                        if(teste == EspList[iterator]):
                            EspList[iterator] += " " + checkwatcher[teste]

        except IndexError as e:
            Attr_Complement = None

        try:
            DimCont = 1
            Dim = html.xpath(
                "//div[@id='div_Conteudo_DetalhesDoProduto_pnlDimensoes']//dd")
            for linha in Dim:
                EspList["Dimensão "+str(DimCont)] = str(linha.text) + \
                    str(linha[0].text) + " " + str(linha[1].text)
                DimCont += 1
        except IndexError as e:
            Dim = "Not Found"

        try:
            Imgs = html.xpath("//ul[@class='thumbs']//li/a/img/@src")
            ImgCont = 1
            for img in Imgs:
                EspList["Imagem "+str(ImgCont)] = img
                ImgCont += 1
        except IndexError as e:
            Imgs = "Not Found"
        return EspList

    def parse_links(self, new_links):
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
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


print("LETS GET IT STARTED")

try:
    spider = EcommerceSpider("https://www.lojamor.com.br/")

    FILENAME = "Mor.csv"
    spider.crawl_to_file(FILENAME)

    spider.timewarn()
except KeyboardInterrupt:
    spider.save_items(FILENAME)
