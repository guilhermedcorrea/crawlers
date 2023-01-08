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


filee = "Incepa"
base = "http://www.banheirosincepa.com.br/"
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
        self.links = ['http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5010i9cr3', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5011i9cr3', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5012i9cr3', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5005iccrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5006iccrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5007iccrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5008iccrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registo-base-fabrimar-12-e-34-avant-cromado-b5016iccrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5008i2cr0', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5009i2cr0', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5005i6crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5006i6crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5007i6cr0', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5008i6cr0', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5000i3crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5001i3crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5009i3crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5010i3crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5003i4crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5004i4crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5013i4crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5014i4crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5009i9cr3', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-celite-12-34-1-platinum-b5005idcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-celite-12-34-1-recta-cromado-b5005ifcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-celite-114-112-platinum-b5007idcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-celite-114-112-recta-cromado-b5008ifcr0', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-celite-114-e-112-new-cromado-b5008igcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-base-reforma-12341-smart-n-cromado-b5005ikcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-base-reforma-114-112-smart-n-cromado-b5008ikcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-base-reforma-1-eco-cromado-b5002iocr3', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-base-reforma-114112-eco-cromado-b5003iocr3', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-base-fabrimar-12-e-34-suite-cromado-b5011i3crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-base-fabrimar-12-e-34-zip-cromado-b5016i9cr3', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-base-12341-smart-n-cromado-b5004ikcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-base-114-112-smart-n-cromado-b5007ikcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5006i2crb', 'http://www.banheirosincepa.com.br/produtos/acabamento-de-registro-b5007i2crb', 'http://www.banheirosincepa.com.br/produtos/assento-original-termof-sc-neo-rose-3369830880100', 'http://www.banheirosincepa.com.br/produtos/assento-original-term-sc-boss-rose-3899830880100', 'http://www.banheirosincepa.com.br/produtos/assento-infantil-08981', 'http://www.banheirosincepa.com.br/produtos/assento-first-pp-9929810010300', 'http://www.banheirosincepa.com.br/produtos/assento-eco-90981_1', 'http://www.banheirosincepa.com.br/produtos/assento-eco-90981_1', 'http://www.banheirosincepa.com.br/produtos/assento-boss-softclose-89988', 'http://www.banheirosincepa.com.br/produtos/assento-31981', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-reforma-12-34-e-1-platinum-b5004idcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-reforma-12-34-e-1-new-cromado-b5006igcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-reforma-12-34-1-recta-cromado-b5006ifcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-reforma-114-112-recta-cromado-b5009ifcr0', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-reforma-114-e-112-platinum-b5006idcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-reforma-114-e-112-new-cromado-b5009igcrb', 'http://www.banheirosincepa.com.br/produtos/acabamento-registro-base-celite-12-34-e-1-new-cromado-b5005igcrb', 'http://www.banheirosincepa.com.br/produtos/bacia-convencional-boss-rose-1893010880100', 'http://www.banheirosincepa.com.br/produtos/bacia-convencional-25301', 'http://www.banheirosincepa.com.br/produtos/bacia-convencional-37301', 'http://www.banheirosincepa.com.br/produtos/bacia-convencional-89301', 'http://www.banheirosincepa.com.br/produtos/bacia-convencional-11301', 'http://www.banheirosincepa.com.br/produtos/bacia-convencional-46303', 'http://www.banheirosincepa.com.br/produtos/bacia-convencional-31309', 'http://www.banheirosincepa.com.br/produtos/bacia-convencional-17301', 'http://www.banheirosincepa.com.br/produtos/bacia-convencional-31310', 'http://www.banheirosincepa.com.br/produtos/bacia-convencional-50305', 'http://www.banheirosincepa.com.br/produtos/bacia-com-caixa-e-assento-50355', 'http://www.banheirosincepa.com.br/produtos/assento-universal-90981', 'http://www.banheirosincepa.com.br/produtos/assento-universal-90981_0', 'http://www.banheirosincepa.com.br/produtos/assento-termofixo-softclose-36983', 'http://www.banheirosincepa.com.br/produtos/assento-softclose-00988', 'http://www.banheirosincepa.com.br/produtos/bacia-para-caixa-boss-gris-1893510070100', 'http://www.banheirosincepa.com.br/produtos/bacia-para-caixa-boss-champagne-1893510660100', 'http://www.banheirosincepa.com.br/produtos/bacia-p-caixa-caixa-e-assento-36351', 'http://www.banheirosincepa.com.br/produtos/bacia-p-caixa-caixa-e-assento-25351', 'http://www.banheirosincepa.com.br/produtos/bacia-p-caixa-caixa-e-assento-37351', 'http://www.banheirosincepa.com.br/produtos/bacia-p-caixa-caixa-e-assento-89351', 'http://www.banheirosincepa.com.br/produtos/bacia-p-caixa-caixa-e-assento-11351', 'http://www.banheirosincepa.com.br/produtos/bacia-p-caixa-caixa-e-assento-46353', 'http://www.banheirosincepa.com.br/produtos/bacia-p-caixa-caixa-e-assento-31359', 'http://www.banheirosincepa.com.br/produtos/bacia-p-caixa-caixa-e-assento-17351', 'http://www.banheirosincepa.com.br/produtos/bacia-p-caixa-caixa-e-assento-31360', 'http://www.banheirosincepa.com.br/produtos/bacia-p-caixa-saida-horizontal-11357', 'http://www.banheirosincepa.com.br/produtos/bacia-neo-com-caixa-e-assento-1367920102100', 'http://www.banheirosincepa.com.br/produtos/bacia-infantil-para-caixa-caixa-e-assento-08255', 'http://www.banheirosincepa.com.br/produtos/bacia-infantil-convencional-08254', 'http://www.banheirosincepa.com.br/produtos/cabide-b8000i3cr0', 'http://www.banheirosincepa.com.br/produtos/cabide-b8000i4cr0', 'http://www.banheirosincepa.com.br/produtos/bide-3-furos-c-ducha-25400', 'http://www.banheirosincepa.com.br/produtos/bide-3-furos-c-ducha-11430', 'http://www.banheirosincepa.com.br/produtos/barra-de-apoio-para-lavatorio-b5005i1cr0', 'http://www.banheirosincepa.com.br/produtos/barra-de-apoio-em-l-b5004i1cr0', 'http://www.banheirosincepa.com.br/produtos/barra-de-apoio-articulada-b5006i1cr0', 'http://www.banheirosincepa.com.br/produtos/barra-de-apoio-b5000i1cr0', 'http://www.banheirosincepa.com.br/produtos/barra-de-apoio-b5001i1cr0', 'http://www.banheirosincepa.com.br/produtos/barra-de-apoio-b5002i1cr0', 'http://www.banheirosincepa.com.br/produtos/barra-de-apoio-b5003i1cr0', 'http://www.banheirosincepa.com.br/produtos/bacia-para-caixa-neo-rimless-rose-1363640880100', 'http://www.banheirosincepa.com.br/produtos/bacia-para-caixa-first-rimless-1933640010100', 'http://www.banheirosincepa.com.br/produtos/bacia-para-caixa-boss-rose-1893510880100', 'http://www.banheirosincepa.com.br/produtos/bacia-para-caixa-boss-noir-1893510100100', 'http://www.banheirosincepa.com.br/produtos/coluna-p-lavatorio-11201', 'http://www.banheirosincepa.com.br/produtos/chuveiro-thema-b5000i4crb', 'http://www.banheirosincepa.com.br/produtos/chuveiro-thema-b5002i4crb', 'http://www.banheirosincepa.com.br/produtos/chuveiro-neo-b5000i2cr0', 'http://www.banheirosincepa.com.br/produtos/chuveiro-manual-thema-b5001i4crb', 'http://www.banheirosincepa.com.br/produtos/chuveiro-boss-b5000i6cr0', 'http://www.banheirosincepa.com.br/produtos/caixa-para-acoplar-first-1505600015100', 'http://www.banheirosincepa.com.br/produtos/caixa-p-6-litros-zip-br-1555700xx2100', 'http://www.banheirosincepa.com.br/produtos/caixa-p-36-litros-zip-br-1555700xx5100', 'http://www.banheirosincepa.com.br/produtos/caixa-ecoflush-36-lts-tp-neo-rose-1365700885100', 'http://www.banheirosincepa.com.br/produtos/caixa-ecoflush-36-lts-boss-rose-1895700885100', 'http://www.banheirosincepa.com.br/produtos/cabide-duplo-b8001i2cr0', 'http://www.banheirosincepa.com.br/produtos/cabide-duplo-b8001i4cr0', 'http://www.banheirosincepa.com.br/produtos/cabide-com-2-ganchos-72624', 'http://www.banheirosincepa.com.br/produtos/cabide-b8000i2cr0', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-curve-1-85074', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-36085', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-25077', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-37073', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-89073', 'http://www.banheirosincepa.com.br/produtos/cuba-apoio-retangular-600x415-platinum-p8-rose-1450750881100', 'http://www.banheirosincepa.com.br/produtos/cuba-apoio-retangular-450x420-platinum-p6-rose-1450730881100', 'http://www.banheirosincepa.com.br/produtos/cuba-apoio-redonda-390-platinum-p2-rose-1450980887100', 'http://www.banheirosincepa.com.br/produtos/cuba-apoio-quadrada-350x350-platinum-p4-rose-1450670889100', 'http://www.banheirosincepa.com.br/produtos/cuba-apoio-350-platinum-p1-rose-1450970887100', 'http://www.banheirosincepa.com.br/produtos/conjunto-5-pecas-72615', 'http://www.banheirosincepa.com.br/produtos/coluna-suspensa-25202', 'http://www.banheirosincepa.com.br/produtos/coluna-suspensa-89202', 'http://www.banheirosincepa.com.br/produtos/coluna-para-tanque-51203', 'http://www.banheirosincepa.com.br/produtos/coluna-p-lavatorio-25201', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p3-45099_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p3-45099_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p3-45099_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p2-45098', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p2-45098_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p2-45098_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p2-45098_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p1-45097', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p1-45097_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p1-45097_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p1-45097_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-inverno-40047', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-indian-63174', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-gran-pacific-63274', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-curve-2-85073', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p7-45074_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p7-45074_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p6-45073', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p6-45073_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p6-45073_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p6-45073_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p5-45061', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p5-45061_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p5-45061_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p5-45061_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p4-45067', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p4-45067_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p4-45067_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p4-45067_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p3-45099', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q4-85061_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q4-85061_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q1-85067', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q1-85067_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q1-85067_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q1-85067_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-provare-77076', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-pacific-63067', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-pacific-63068', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p8-45075', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p8-45075_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p8-45075_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p8-45075_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p7-45074', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-p7-45074_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-qr7-22073', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-qr3-85075', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-qr1-85069', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q9-19049', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q6-carrara-1850680893100', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q6-85068', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q6-85068_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q6-85068_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q6-85068_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q5-85049', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q5-85049_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q5-85049_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q5-85049_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q4-85061', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-q4-85061_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-semiencaixe-q2-85025_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-semiencaixe-q2-85025_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-semiencaixe-q2-85025_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-semiencaixe-pacific-63027', 'http://www.banheirosincepa.com.br/produtos/cuba-de-semiencaixe-pacific-63028', 'http://www.banheirosincepa.com.br/produtos/cuba-de-semiencaixe-curve-5-85028', 'http://www.banheirosincepa.com.br/produtos/cuba-de-semiencaixe-89025', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-sentire-77068', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-r5-14085', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-r3-85085', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-r1-85097', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-r1-85097_07', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-r1-85097_10', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-r1-85097_66', 'http://www.banheirosincepa.com.br/produtos/cuba-de-apoio-r0-1850990017100', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-b5013i9cr3', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-b5005i2crb', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-b5004iccrb', 'http://www.banheirosincepa.com.br/produtos/cuba-retangular-10135', 'http://www.banheirosincepa.com.br/produtos/cuba-redonda-de-apoio-r2-85098', 'http://www.banheirosincepa.com.br/produtos/cuba-redonda-10151', 'http://www.banheirosincepa.com.br/produtos/cuba-redonda-10160', 'http://www.banheirosincepa.com.br/produtos/cuba-oval-10145', 'http://www.banheirosincepa.com.br/produtos/cuba-de-sobreporembutir-q3-85050', 'http://www.banheirosincepa.com.br/produtos/cuba-de-sobrepor-apoio-q7-85045', 'http://www.banheirosincepa.com.br/produtos/cuba-de-sobrepor-q8-85133', 'http://www.banheirosincepa.com.br/produtos/cuba-de-sobrepor-outono-40015', 'http://www.banheirosincepa.com.br/produtos/cuba-de-sobrepor-37016', 'http://www.banheirosincepa.com.br/produtos/cuba-de-semiencaixe-sentire-77027', 'http://www.banheirosincepa.com.br/produtos/cuba-de-semiencaixe-q2-85025', 'http://www.banheirosincepa.com.br/produtos/espelho-com-base-54x58-cm-b60004m170', 'http://www.banheirosincepa.com.br/produtos/espelho-com-base-38x58-cm-b60003m170', 'http://www.banheirosincepa.com.br/produtos/espelheira-com-porta-38x58-cm-b60000m170', 'http://www.banheirosincepa.com.br/produtos/espelheira-com-porta-38x58-cm-b60001m170', 'http://www.banheirosincepa.com.br/produtos/espelheira-com-porta-38x58-cm-b60002m170', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-sem-derivacao-smart-n-cromado-b5003ikcrb', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-sem-derivacao-eco-cromado-b5006iocr3', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-com-derivacao-smart-n-cromado-b5002ikcrb', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-com-derivacao-recta-cromado-b5004ifcrb', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-com-derivacao-platinum-cromado-b5003idcrb', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-com-derivacao-new-cromado-b5004igcrb', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-b5002i6crb', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-b5004i3crb', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-b5007i4crb', 'http://www.banheirosincepa.com.br/produtos/ducha-higienica-b5006i9cr3', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-63x46-cm-b60017m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-63x46-cm-b60018m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-53x39-cm-b60006m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-53x39-cm-b60007m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-53x39-cm-b60008m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-53x39-cm-b60015m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-53x39-cm-b60016m130', 'http://www.banheirosincepa.com.br/produtos/gab-loft-gavpta-50x38-brbrr1-b60049m140', 'http://www.banheirosincepa.com.br/produtos/flexivel-400-mm-aco-inox-b5008r0cr3', 'http://www.banheirosincepa.com.br/produtos/espelho-com-base-luminaria-80x58-cm-b60016m170', 'http://www.banheirosincepa.com.br/produtos/espelho-com-base-luminaria-65x58-cm-b60015m170', 'http://www.banheirosincepa.com.br/produtos/espelho-com-base-luminaria-54x58-cm-b60014m170', 'http://www.banheirosincepa.com.br/produtos/espelho-com-base-luminaria-38x58-cm-b60013m170', 'http://www.banheirosincepa.com.br/produtos/espelho-com-base-80x58-cm-b60006m170', 'http://www.banheirosincepa.com.br/produtos/espelho-com-base-65x58-cm-b60005m170', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-55x43-cm-b60014m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-55x43-cm-b60015m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-45x43-cm-b60000m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-45x43-cm-b60001m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-45x43-cm-b60002m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-45x43-cm-b60012m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-45x43-cm-b60013m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-80x46-cm-b60012m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-80x46-cm-b60013m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-80x46-cm-b60014m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-80x46-cm-b60019m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-80x46-cm-b60020m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-63x46-cm-b60009m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-63x46-cm-b60010m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-de-apoio-com-gaveta-e-basculante-63x46-cm-b60011m130', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-espelho-e-prateleira-b60005m240', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-espelho-e-prateleira-b60004m240', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-portas-e-lavatorio-60x34-cm-b60009m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-portas-e-lavatorio-60x34-cm-b60010m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-portas-e-lavatorio-60x34-cm-b60011m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-portas-e-lavatorio-60x34-cm-b60018m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-portas-e-lavatorio-60x34-cm-b60019m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-65x43-cm-b60006m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-65x43-cm-b60007m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-65x43-cm-b60008m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-65x43-cm-b60016m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-65x43-cm-b60017m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-55x43-cm-b60003m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-55x43-cm-b60004m150', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-com-gaveta-e-lavatorio-55x43-cm-b60005m150', 'http://www.banheirosincepa.com.br/produtos/kit-gabinete-cuba-e-espelho-b60000m250', 'http://www.banheirosincepa.com.br/produtos/kit-gabinete-cuba-e-espelho-b60001m250', 'http://www.banheirosincepa.com.br/produtos/kit-first-bacia-com-caixa-acoplada-e-itens-de-instalacao-1937230010100', 'http://www.banheirosincepa.com.br/produtos/kit-avant-bacia-com-caixa-acoplada-e-itens-de-instalacao-1177230010100', 'http://www.banheirosincepa.com.br/produtos/kit-avant-gab-gavpta-60x34-weweespelho-b60017m250', 'http://www.banheirosincepa.com.br/produtos/kit-avant-gab-gavpta-60x34-webrespelho-b60016m240', 'http://www.banheirosincepa.com.br/produtos/kit-avant-gab-gavpta-60x34-brbrespelho-b60015m240', 'http://www.banheirosincepa.com.br/produtos/kit-avant-gab-1-pta-60x34-weweespelho-b60014m240', 'http://www.banheirosincepa.com.br/produtos/kit-avant-gab-1-pta-60x34-webrespelho-b60013m240', 'http://www.banheirosincepa.com.br/produtos/kit-avant-gab-1-pta-60x34-brbrespelho-b60012m240', 'http://www.banheirosincepa.com.br/produtos/kit-art-bacia-com-caixa-acoplada-e-itens-de-instalacao-1507230010100', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-espelho-e-prateleira-b60000m240', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-espelho-e-prateleira-b60002m240', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-espelho-e-prateleira-b60001m240', 'http://www.banheirosincepa.com.br/produtos/gabinete-integrado-espelho-e-prateleira-b60003m240', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-80x38-weweq6-b60059m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-80x38-webrq6-b60061m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-80x38-brbrq6-b60058m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-60x38-wewer1-b60055m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-60x38-weweq6-b60051m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-60x38-webrr1-b60057m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-60x38-webrq6-b60053m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-60x38-brbrr1-b60054m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-60x38-brbrq6-b60050m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-50x38-wewer1-b60047m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-50x38-webrr1-b60049m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-gavpta-50x38-brbrr1-b60046m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-2pta-50x38-wewer1-b60043m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-2pta-50x38-webrr1-b60045m140', 'http://www.banheirosincepa.com.br/produtos/kit-loft-gab-2pta-50x38-brbrr1-b60042m140', 'http://www.banheirosincepa.com.br/produtos/lavatorio-com-coluna-50001_50201', 'http://www.banheirosincepa.com.br/produtos/lav-suspenso-p-380x280-fasl-in-br-1330390013100', 'http://www.banheirosincepa.com.br/produtos/lav-suspenso-m-465x340-fasl-in-br-1270370013100', 'http://www.banheirosincepa.com.br/produtos/kit-zip-gab-2-pta-40x22-brweesp-b60001m250', 'http://www.banheirosincepa.com.br/produtos/kit-zip-gab-2-pta-40x22-brbresp-b60000m250', 'http://www.banheirosincepa.com.br/produtos/kit-thema-gab-gavpta-80x38-wewecuba-b60005m290', 'http://www.banheirosincepa.com.br/produtos/kit-thema-gab-gavpta-80x38-webrwcuba-b60007m290', 'http://www.banheirosincepa.com.br/produtos/kit-thema-gab-gavpta-80x38-webrbcuba-b60006m290', 'http://www.banheirosincepa.com.br/produtos/kit-thema-gab-gavpta-80x38-brbrcuba-b60004m290', 'http://www.banheirosincepa.com.br/produtos/kit-thema-gab-gavpta-60x38-wewecuba-b60001m290', 'http://www.banheirosincepa.com.br/produtos/kit-thema-gab-gavpta-60x38-webrw-cuba-b60002m290', 'http://www.banheirosincepa.com.br/produtos/kit-thema-gab-gavpta-60x38-webrb-cuba-b60003m290', 'http://www.banheirosincepa.com.br/produtos/kit-thema-gab-gavpta-60x38-brbrcuba-b60000m290', 'http://www.banheirosincepa.com.br/produtos/kit-loft-r1-cuba-torneira-1857250012100', 'http://www.banheirosincepa.com.br/produtos/kit-loft-q1-cuba-torneira-1857250010100', 'http://www.banheirosincepa.com.br/produtos/lavatorio-suspenso-p-33039', 'http://www.banheirosincepa.com.br/produtos/lavatorio-suspenso-m-27037', 'http://www.banheirosincepa.com.br/produtos/lavatorio-suspenso-first-1930360011100', 'http://www.banheirosincepa.com.br/produtos/lavatorio-suspenso-eco-04036', 'http://www.banheirosincepa.com.br/produtos/lavatorio-suspenso-de-canto-p-04014', 'http://www.banheirosincepa.com.br/produtos/lavatorio-suspenso-de-canto-m', 'http://www.banheirosincepa.com.br/produtos/lavatorio-suspenso-11038', 'http://www.banheirosincepa.com.br/produtos/lavatorio-p-coluna-25006', 'http://www.banheirosincepa.com.br/produtos/lavatorio-p-coluna-37001', 'http://www.banheirosincepa.com.br/produtos/lavatorio-p-coluna-89001', 'http://www.banheirosincepa.com.br/produtos/lavatorio-p-coluna-11006', 'http://www.banheirosincepa.com.br/produtos/lavatorio-p-coluna-46007', 'http://www.banheirosincepa.com.br/produtos/lavatorio-com-coluna-suspensa-31055', 'http://www.banheirosincepa.com.br/produtos/lavatorio-com-coluna-suspensa-17001', 'http://www.banheirosincepa.com.br/produtos/lavatorio-com-coluna-17001-17201', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5009i6crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5012i6crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5002i3crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5005i3crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5005i4crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5008i4crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5007i9crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5014i9crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5003iccrb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5009iccrb', 'http://www.banheirosincepa.com.br/produtos/misturador-cozinha-parede-bica-movel-com-arejador-articulado-smart-n-cromado-b5010ikcrb', 'http://www.banheirosincepa.com.br/produtos/misturador-cozinha-mesa-bica-movel-com-arejador-articulado-smart-n-cromado-b5009ikcrb', 'http://www.banheirosincepa.com.br/produtos/mictorio-vip-08283', 'http://www.banheirosincepa.com.br/produtos/mictorio-c-sifao-eco-incepa-br-1082850xx0100', 'http://www.banheirosincepa.com.br/produtos/loft-q6-cuba-torneira-1857250011100', 'http://www.banheirosincepa.com.br/produtos/modulo-de-coluna-23x75-cm-b60009m170', 'http://www.banheirosincepa.com.br/produtos/modulo-de-coluna-23x75-cm-b60008m170', 'http://www.banheirosincepa.com.br/produtos/modulo-de-coluna-23x75-cm-b60017m170', 'http://www.banheirosincepa.com.br/produtos/modulo-de-coluna-23x75-cm-b60018m170', 'http://www.banheirosincepa.com.br/produtos/misturador-lavatorio-parede-embutir-com-valvula-recta-cromado-b5001ifcrb', 'http://www.banheirosincepa.com.br/produtos/misturador-lavatorio-mesa-3-furos-bica-alta-com-valvula-smart-n-cromado-b5000ikcrb', 'http://www.banheirosincepa.com.br/produtos/misturador-lavatorio-mesa-3-furos-bica-alta-com-valvula-recta-cromado-b5000ifcrb', 'http://www.banheirosincepa.com.br/produtos/misturador-lavatorio-mesa-3-furos-bica-alta-com-valvula-new-cromado-b5000igcrb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-parede-b5002i2crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-parede-b5011i6crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-parede-b5006i3crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-parede-b5009i4crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-parede-b5015i9crb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-parede-b5010iccrb', 'http://www.banheirosincepa.com.br/produtos/misturador-de-mesa-b5001i2crb', 'http://www.banheirosincepa.com.br/produtos/monocomando-de-mesa-b5006ibcr0', 'http://www.banheirosincepa.com.br/produtos/monocomando-cozinha-mesa-bica-flexivel-vermelho-incepa-colors-cromado-b5000iecr0', 'http://www.banheirosincepa.com.br/produtos/monocomando-cozinha-mesa-bica-flexivel-preto-incepa-colors-cromado-b5001iecr0', 'http://www.banheirosincepa.com.br/produtos/modulo-de-extensao-pta-avant-wewe-b60010m240', 'http://www.banheirosincepa.com.br/produtos/modulo-de-extensao-pta-avant-webr-b60011m240', 'http://www.banheirosincepa.com.br/produtos/modulo-de-extensao-pta-avant-brbr-b60009m240', 'http://www.banheirosincepa.com.br/produtos/modulo-de-extensao-gav-avant-wewe-b60007m240', 'http://www.banheirosincepa.com.br/produtos/modulo-de-extensao-gav-avant-webr-b60008m240', 'http://www.banheirosincepa.com.br/produtos/modulo-de-extensao-gav-avant-brbr-b60006m240', 'http://www.banheirosincepa.com.br/produtos/modulo-de-coluna-28x150-cm-b60010m170', 'http://www.banheirosincepa.com.br/produtos/modulo-de-coluna-28x150-cm-b60011m170', 'http://www.banheirosincepa.com.br/produtos/modulo-de-coluna-28x150-cm-b60012m170', 'http://www.banheirosincepa.com.br/produtos/modulo-de-coluna-28x150-cm-b60019m170', 'http://www.banheirosincepa.com.br/produtos/modulo-de-coluna-28x150-cm-b60020m170', 'http://www.banheirosincepa.com.br/produtos/modulo-de-coluna-23x75cm-b60007m170', 'http://www.banheirosincepa.com.br/produtos/papeleira-com-rolete-72620', 'http://www.banheirosincepa.com.br/produtos/papeleira-b8003i2cr0', 'http://www.banheirosincepa.com.br/produtos/papeleira-b8002i3cr0', 'http://www.banheirosincepa.com.br/produtos/papeleira-b8003i4cr0', 'http://www.banheirosincepa.com.br/produtos/oval-pequena-10119', 'http://www.banheirosincepa.com.br/produtos/oval-pequena-10148', 'http://www.banheirosincepa.com.br/produtos/oval-10116', 'http://www.banheirosincepa.com.br/produtos/oval-76117', 'http://www.banheirosincepa.com.br/produtos/oval-76146', 'http://www.banheirosincepa.com.br/produtos/monocomando-para-bide-b5002ibcr0', 'http://www.banheirosincepa.com.br/produtos/monocomando-para-banheira-ou-chuveiro-b5004ibcr0', 'http://www.banheirosincepa.com.br/produtos/monocomando-para-banheira-e-chuveiro-b5003ibcr0', 'http://www.banheirosincepa.com.br/produtos/monocomando-de-mesa-b5000ibcr0', 'http://www.banheirosincepa.com.br/produtos/monocomando-de-mesa-b5001ibcr0', 'http://www.banheirosincepa.com.br/produtos/monocomando-de-mesa-b5005ibcr0', 'http://www.banheirosincepa.com.br/produtos/sifao-para-tanque-b5001r0crb', 'http://www.banheirosincepa.com.br/produtos/sifao-para-lavatorio-b5000r0crb', 'http://www.banheirosincepa.com.br/produtos/sifao-para-cozinha-b5002r0crb', 'http://www.banheirosincepa.com.br/produtos/saboneteira-pequena-72622', 'http://www.banheirosincepa.com.br/produtos/saboneteira-de-vidro-b8004i3cr0', 'http://www.banheirosincepa.com.br/produtos/saboneteira-b8002i2cr0', 'http://www.banheirosincepa.com.br/produtos/saboneteira-b8002i4cr0', 'http://www.banheirosincepa.com.br/produtos/saboneteira-72621', 'http://www.banheirosincepa.com.br/produtos/retangular-76107', 'http://www.banheirosincepa.com.br/produtos/retangular-10136', 'http://www.banheirosincepa.com.br/produtos/redonda-pequena-10229', 'http://www.banheirosincepa.com.br/produtos/redonda-10129', 'http://www.banheirosincepa.com.br/produtos/redonda-10159', 'http://www.banheirosincepa.com.br/produtos/prateleira-de-vidro-b8001i3cr0', 'http://www.banheirosincepa.com.br/produtos/porta-toalha-com-bastao-72623', 'http://www.banheirosincepa.com.br/produtos/toalheiro-para-cuba-de-semiencaixe-pacific-63903_0', 'http://www.banheirosincepa.com.br/produtos/toalheiro-barra-b8005i2cr0', 'http://www.banheirosincepa.com.br/produtos/toalheiro-barra-b8005i3cr0', 'http://www.banheirosincepa.com.br/produtos/toalheiro-barra-b8005i4cr0', 'http://www.banheirosincepa.com.br/produtos/toalheiro-anel-b8004i2cr0', 'http://www.banheirosincepa.com.br/produtos/toalheiro-anel-b8003i3cr0', 'http://www.banheirosincepa.com.br/produtos/toalheiro-anel-b8004i4cr0', 'http://www.banheirosincepa.com.br/produtos/thema-cuba-torneira-1257250010100', 'http://www.banheirosincepa.com.br/produtos/tanque-pp-suspenso-1512670013100', 'http://www.banheirosincepa.com.br/produtos/tanque-pp-com-gabinete-b60001m370', 'http://www.banheirosincepa.com.br/produtos/tanque-p-suspenso-51263', 'http://www.banheirosincepa.com.br/produtos/tanque-m-51265', 'http://www.banheirosincepa.com.br/produtos/tanque-gg-51262', 'http://www.banheirosincepa.com.br/produtos/tanque-g-builders-51264', 'http://www.banheirosincepa.com.br/produtos/tanque-g-51266', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5012i4crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5000i9cr3', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5003i9cr3', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5008i9cr3', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5000i8crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5001iccrb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5002iccrb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5011iccrb', 'http://www.banheirosincepa.com.br/produtos/torneira-cozinha-parede-smart-n-cromado-b5012ikcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-cozinha-parede-eco-cromado-b5005iocr3', 'http://www.banheirosincepa.com.br/produtos/torneira-cozinha-parede-com-arejador-articulado-new-cromado-b5011igcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-cozinha-mesa-smart-n-cromado-b5011ikcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-cozinha-mesa-eco-cromado-b5004iocr3', 'http://www.banheirosincepa.com.br/produtos/torneira-cozinha-mesa-bica-alta-com-arejador-articulado-new-cromado-b5010igcrb', 'http://www.banheirosincepa.com.br/produtos/toalheiro-para-cuba-de-semiencaixe-sentire-77903', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5002i9cr3', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5004i9cr3', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5005i9cr3', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5001i8crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5012iccrb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5013iccrb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5014iccrb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5015iccrb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5004i2crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5001i6crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5003i6crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5003i3crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5007i3crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5006i4crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-mesa-b5010i4crb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-mesa-bica-alta-smart-n-cromado-b5001ikcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-mesa-bica-alta-recta-cromado-b5002ifcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-mesa-bica-alta-platinum-cromado-b5001idcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-mesa-bica-alta-new-cromado-b5001igcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-mesa-bica-alta-eco-cromado-b5000iocr3', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-mesa-bica-alta-design-cromado-b5000ihcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-tanquejardim-70-mm-parede-com-bico-plastico-eco-cromado-b5010iocr3', 'http://www.banheirosincepa.com.br/produtos/torneira-de-tanquejardim-1300-mm-parede-com-bico-plastico-eco-cromado-b5012iocr3', 'http://www.banheirosincepa.com.br/produtos/torneira-de-tanquejardim-100-mm-parede-com-bico-plastico-eco-cromado-b5011iocr3', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5003i2crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5004i6crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5010i6crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5008i3crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5011i4crb', 'http://www.banheirosincepa.com.br/produtos/torneira-de-parede-b5001i9cr3', 'http://www.banheirosincepa.com.br/produtos/valvula-lavatorio-78-universal-cromado-tampa-plastica-branca-incepa-b5013iacr3', 'http://www.banheirosincepa.com.br/produtos/valvula-lavatorio-78-sem-ladrao-cromado-tampa-plastica-branca-b5003iacr3', 'http://www.banheirosincepa.com.br/produtos/valvula-de-mictorio-b5002i8crb', 'http://www.banheirosincepa.com.br/produtos/valvula-de-escoamento-para-tanque-b5004iacr3', 'http://www.banheirosincepa.com.br/produtos/valvula-cozinha-412x112-com-cesta-metal-cromado-b5006iacrb', 'http://www.banheirosincepa.com.br/produtos/valvula-cozinha-312x112-com-cesta-metal-incepa-b5005iacrb', 'http://www.banheirosincepa.com.br/produtos/torneira-para-tanque-e-maquina-de-lavar-eco-cromado-b5009iocr3', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-parede-recta-cromado-b5003ifcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-parede-platinum-cromado-b5000idcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-parede-new-cromado-b5003igcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-parede-cromado-b5002ihcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-mesa-bica-baixa-platinum-cromado-b5002idcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-mesa-bica-baixa-new-cromado-b5002igcrb', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-mesa-bica-baixa-eco-cromado-b5001iocr3', 'http://www.banheirosincepa.com.br/produtos/torneira-lavatorio-mesa-bica-baixa-design-cromado-b5001ihcrb']

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
                "//h1[@class='product']")[0].text.replace("\n", "").replace("\t", "")
        except IndexError as e:
            nome = no

        try:
            sku = html.xpath(
                "//div[@class='code']")[0].text.replace("\n", "").replace("\t", "").replace("Cód.", "").strip(" ")
        except IndexError as e:
            sku = no

        cat = html.xpath("//ul[@class='breadcrumb']/li/a")
        fullcat = ""
        for x in cat:
            x = blank(x.text.replace("\n", "").replace("\t", ""))
            fullcat += x + " > "

        EspList = dict(Nome=nome, SKU=sku, Categoria=fullcat)

        ref = html.xpath("//div[contains(@class,'box')]/h6/strong")
        val = html.xpath("//div[contains(@class,'box')]/span")
        cont = 0

        for x in ref:
            EspList[formatar(x.text)] = val[cont].text
            cont += 1


        imgs = html.xpath("//ul[@class='lista-de-imagens']//img/@src")

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
