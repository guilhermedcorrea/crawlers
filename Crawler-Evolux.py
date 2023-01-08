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


filee = "Evolux"


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
        self.cats = ["https://www.linhaevolux.com.br/persianas-e-cortinas-de-rolo?O=OrderByPriceASC#16", "https://www.linhaevolux.com.br/cortinas#2",
                     "https://www.linhaevolux.com.br/decoracao#4", "https://www.linhaevolux.com.br/escadas#1", "https://www.linhaevolux.com.br/outros#1"]
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
        self.links = ['https://www.linhaevolux.com.br/violao-queens-preto-d137515eq/p','https://www.linhaevolux.com.br/alarme-residencial-ou-comercial-inteligente-seguro-facil-sf1007/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-160x160-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-120x160-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-100x220-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-100x220-preta/p','https://www.linhaevolux.com.br/persiana-vertical-renoir-220x240-tecido-branca-copy-300-/p','https://www.linhaevolux.com.br/persiana-rolo-screen-140x220-branca/p','https://www.linhaevolux.com.br/persiana-rolo-screen-100x220-champagne/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-100x220-chumbo/p','https://www.linhaevolux.com.br/https---www-linhaevolux-com-br-violao-queens-preto-d137516eq-p/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-180x160-branca/p','https://www.linhaevolux.com.br/violao-queens-bege-d137515/p','https://www.linhaevolux.com.br/http---www-linhaevolux-com-br-violao-queens-sunburst-d184518-p/p','https://www.linhaevolux.com.br/violao-queens-preto-d137516/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-100x160-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-160x160-branca/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-160-300cm-ponteira-esfera-ouro-velho/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-bola-prata/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-160-300cm-ponteira-coroa-preta/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-structured-180x220m-bege/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-220x220-branca/p','https://www.linhaevolux.com.br/persiana-vertical-renoir-180x240-tecido-bege/p','https://www.linhaevolux.com.br/persiana-rolo-toucher-140x140-branca/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-140x160-branca/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-160x160-marrom/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-180x220-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-wood-140x160-madeira-tabaco/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-160x220-branca/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-100x220-caramelo/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-140x160-linho/p','https://www.linhaevolux.com.br/persiana-painel-japones-innove-3vias-180x260-branco/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-180x220-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-off-080x130-bege/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-120x160-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-off-080x130-chumbo/p','https://www.linhaevolux.com.br/persiana-horizontal-wood-100x220-madeira-tabaco/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-structured-140x160m-bege/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-140x160-creme/p','https://www.linhaevolux.com.br/persiana-solid-50-persiana-madeira-50mm-120x235-carvalho/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-esfera-ouro-velho/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-140x160-chocolate/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-structured-160x160m-bege/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-120x160-branca/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-structured-220x220m-branca/p','https://www.linhaevolux.com.br/lugar-americano-para-mesa-chemin-30x45-bambu-bege/p','https://www.linhaevolux.com.br/persiana-vertical-renoir-180x240-tecido-branca/p','https://www.linhaevolux.com.br/lanterna-decorativa-33cm-cinza/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-structured-220x220m-bege/p','https://www.linhaevolux.com.br/lanterna-decorativa-43cm-preta/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-cilindrica-ouro-velho/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-bola-preta/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-160-300cm-ponteira-cilindrica-preta/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-ellegance-preta/p','https://www.linhaevolux.com.br/persiana-rolo-screen-140x160-champagne/p','https://www.linhaevolux.com.br/persiana-horizontal-off-060x130-chumbo/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-140x160-bege/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120m-210m-ponteira-esfera-preta/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-120x160-marrom/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-ellegance-ouro-velho/p','https://www.linhaevolux.com.br/lanterna-decorativa-50cm-branca/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-120x160-caramelo/p','https://www.linhaevolux.com.br/lanterna-decorativa-21cm-preta/p','https://www.linhaevolux.com.br/lugar-americano-para-mesa-chemin-30x45-bambu-vermelho/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-120x160-chocolate/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-180x220-caramelo/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-140x160-preta/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-ellegance-tabaco/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-160x160-prata/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-160x220-preta/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-140x220-marrom/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-structured-140x160m-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-wood-060x160-madeira-tabaco/p','https://www.linhaevolux.com.br/persiana-horizontal-off-100x130-chumbo/p','https://www.linhaevolux.com.br/lugar-americano-para-mesa-chemin-30x45-bambu-preto/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-160x220-bege/p','https://www.linhaevolux.com.br/persiana-solid-50-persiana-madeira-50mm-120x235-avela/p','https://www.linhaevolux.com.br/lanterna-decorativa-40cm-cromada/p','https://www.linhaevolux.com.br/lugar-americano-para-mesa-chemin-30x45-bambu-verde/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-100x160-preta/p','https://www.linhaevolux.com.br/persiana-painel-japones-innove-4vias-240x260-branco/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-coroa-preta/p','https://www.linhaevolux.com.br/lanterna-decorativa-455cm-preta/p','https://www.linhaevolux.com.br/persiana-painel-japones-innove-3vias-180x260-bege/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-100x220-bege/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-160x160-branca/p','https://www.linhaevolux.com.br/persiana-rolo-screen-120x160-champagne/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-180x220-branca/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-220x220-marrom/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-160x160-creme/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-180x220-marrom/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-160x220-creme/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-140x160-marrom/p','https://www.linhaevolux.com.br/persiana-tissel-persiana-rolo-140x160-cm-vanila/p','https://www.linhaevolux.com.br/persiana-rolo-toucher-160x140-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-off-140x130-chumbo/p','https://www.linhaevolux.com.br/persiana-rolo-toucher-120x140-bege/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-160x220-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-160x160-bege/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-100x220-preta/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-structured-180x220m-branca/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-vertical-180x240-branca/p','https://www.linhaevolux.com.br/persiana-rolo-screen-160x160-champagne/p','https://www.linhaevolux.com.br/lugar-americano-para-mesa-chemin-30x45-bambu-branco/p','https://www.linhaevolux.com.br/persiana-horizontal-off-066x130-branca/p','https://www.linhaevolux.com.br/persiana-rolo-toucher-120x140-branca/p','https://www.linhaevolux.com.br/lanterna-decorativa-45cm-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-100x220-branca/p','https://www.linhaevolux.com.br/persiana-rolo-toucher-160x140-bege/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-140x220-bege/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-180x220-linho/p','https://www.linhaevolux.com.br/persiana-rolo-screen-120x160-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-100x160-branca/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-140x160-bege/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-cilindrica-preta/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-220x220-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-off-060x130-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-100x220-bege/p','https://www.linhaevolux.com.br/persiana-rolo-screen-140x160-branca/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-160x220-linho/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-100x220-branca/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-160x160-caramelo/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-120x160-creme/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-140x160-branca/p','https://www.linhaevolux.com.br/persiana-rolo-toucher-140x140-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-100x160-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-160x160-chumbo/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-120x160-bege/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-160x220-caramelo/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-a-210-ponteira-coroa-cromada/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-ellegance-branca/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-bola-ouro-velho/p','https://www.linhaevolux.com.br/persiana-solid-50-persiana-madeira-50mm-140x235-avela/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-bola-tabaco/p','https://www.linhaevolux.com.br/balanca-mecanica-branca/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210m-ponteira-coroa-ouro-velho/p','https://www.linhaevolux.com.br/persiana-horizontal-off-120x130-bege/p','https://www.linhaevolux.com.br/lugar-americano-para-mesa-chemin-30x45-azul-bambu/p','https://www.linhaevolux.com.br/persiana-spring-persiana-rolo-140x160-cm-vanila/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-120x160-branca/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-100x220-marrom/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-160x220-chocolate/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-100x220-linho/p','https://www.linhaevolux.com.br/persiana-vertical-renoir-220x240-tecido-bege/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-120x160-preta/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-120x160-linho/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-120x160-prata/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-160x160-linho/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-100x160-prata/p','https://www.linhaevolux.com.br/persiana-solid-50-persiana-madeira-50mm-100x235-carvalho/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-100x160-marrom/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-ellegance-prata/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-160-300cm-ponteira-esfera-preta/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-structured-120x160m-bege/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-structured-120x160m-branca/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-structured-160x160m-branca/p','https://www.linhaevolux.com.br/persiana-rolo-blackout-nouvel-160x160-chocolate/p','https://www.linhaevolux.com.br/persiana-solid-50-persiana-madeira-50mm-100x235-avela/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-140x160-prata/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-100x220-branca/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-160x160-branca/p','https://www.linhaevolux.com.br/persiana-solid-50-persiana-madeira-50mm-140x235-carvalho/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-160x220-marrom/p','https://www.linhaevolux.com.br/persiana-rolo-screen-120x220-champagne/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-220x220-linho/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-220x220-preta/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-160x160-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-120x160-preta/p','https://www.linhaevolux.com.br/persiana-solid-50-persiana-madeira-50mm-160x235-avela/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-220x220-caramelo/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-horizontal-140x160-caramelo/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-180x160-bege/p','https://www.linhaevolux.com.br/persiana-rolo-screen-140x220-champagne/p','https://www.linhaevolux.com.br/persiana-soft-rolo-linho-100x160-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-off-080x130-branca/p','https://www.linhaevolux.com.br/espelho-decorativo-3-ouro-envelhecido/p','https://www.linhaevolux.com.br/espelho-decorativo4-branco/p','https://www.linhaevolux.com.br/espelho-decorativo5-preto/p','https://www.linhaevolux.com.br/espelho-decorativo6-branco/p','https://www.linhaevolux.com.br/espelho-decorativo7-preto/p','https://www.linhaevolux.com.br/espelho-decorativo8-branco/p','https://www.linhaevolux.com.br/espelho--decorativo9-ouro-velho/p','https://www.linhaevolux.com.br/espelho--decorativo10-branco/p','https://www.linhaevolux.com.br/espelho-decorativo11-branco/p','https://www.linhaevolux.com.br/espelho-decorativo-12-preto/p','https://www.linhaevolux.com.br/espelho-decorativo13-prata-envelhecido/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-160x160-preta/p','https://www.linhaevolux.com.br/persiana-rolo-screen-100x220-branca/p','https://www.linhaevolux.com.br/persiana-rolo-screen-120x220-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-120x160-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-off-120x130-chumbo/p','https://www.linhaevolux.com.br/persiana-horizontal-off-080x130-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-off-100x130-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-off-120x130-preta/p','https://www.linhaevolux.com.br/persiana-solid-50-persiana-madeira-50mm-160x235-carvalho/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-100x160-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-160x160-branca/p','https://www.linhaevolux.com.br/persiana-painel-japones-innove-4vias-240x260-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-100x160-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-140x160-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-100x160-chumbo/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-120x160-chumbo/p','https://www.linhaevolux.com.br/persiana-horizontal-off-160x130-chumbo/p','https://www.linhaevolux.com.br/persiana-horizontal-off-060x130-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-wood-100x220-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-off-140x130-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-off-120x130-branca/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-120-210-ponteira-bola-branca/p','https://www.linhaevolux.com.br/kit-varao-para-cortina-extensivo-160-300cm-ponteira-cilindrica-cromada/p','https://www.linhaevolux.com.br/persiana-horizontal-wood-120x160m-branca/p','https://www.linhaevolux.com.br/persiana-tissel-persiana-rolo-160x160-vanila/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-160x160-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-wood--100x160m--branca/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-100x220-prata/p','https://www.linhaevolux.com.br/persiana-horizontal-royal-120x160-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-off-160x130-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-140x160-chumbo/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-180x160-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-off-100x130-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-off-140x130-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-off-160x130-bege/p','https://www.linhaevolux.com.br/persiana-horizontal-wood-180x160-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-140x160-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-120x160-branca/p','https://www.linhaevolux.com.br/persiana-rolo-screen-160x160-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-off-100x130-branca/p','https://www.linhaevolux.com.br/persiana-rolo-screen-160x220-branca/p','https://www.linhaevolux.com.br/persiana-rolo-screen-180x220-branca/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-agille-d184685/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-agille-d184686/p','https://www.linhaevolux.com.br/papel-de-parede-vinilico-10mx53cm-folhagem-35205/p','https://www.linhaevolux.com.br/papel-de-parede-vinilico-10mx53cm-listrado-33f405/p','https://www.linhaevolux.com.br/papel-de-parede-vinilico-10mx53cm-listrado-36304/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-marrom-texturizado/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-palha-damasco/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-classic-2-d184823/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-classic-2-d184679/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-classic-2-d184682/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-classic-2-d184677/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-classic-2-d184678/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-dourado-floral/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-950x53-floral-bege/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-ondulado-prata/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-bege-geometrico/p','https://www.linhaevolux.com.br/cola-em-po-para-papel-de-parede-evolux-50/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-agille-d184684/p','https://www.linhaevolux.com.br/papel-de-parede-vinilico-10mx53cm-listrado-azul/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-950x53-branco-hexagono/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-champagne-damasco-marrom/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-classic-2-d184676/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-bege-preto-geometrico/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-classic-2-d184680/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-classic-2-d184681/p','https://www.linhaevolux.com.br/cola-em-po-para-papel-de-parede-evolux-30/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-floral-champagne/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-champagne-marsala-damasco/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-950x53-bege-texturizado/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-floral-35406/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-950x53-bege-floral/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-quadradinhos-champagne/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-damasco-azul/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-arabesco-caqui/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-floral-bege-dourado/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-classic-2-d184675/p','https://www.linhaevolux.com.br/papel-de-parede-vinilico-10mx53cm-folhagem-36203/p','https://www.linhaevolux.com.br/papel-de-parede-vinilico-10mx53cm-listrado-36305/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-950x53-branco-floral/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-tijolos-bege/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-950x53-bege-listado/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-950x53-floral-avela/p','https://www.linhaevolux.com.br/kit-5-plafons-led-embutir-redondo-18w-luz-branca-d184563/p','https://www.linhaevolux.com.br/kit-5-plafons-led-embutir-redondo-12w-luz-branca-d1845625/p','https://www.linhaevolux.com.br/kit-tela-mosquiteira-ajustavel-com-velcro-160x160m-para-janelas/p','https://www.linhaevolux.com.br/kit-10-plafons-led-embutir-redondo-12w-luz-branca-d18456210/p','https://www.linhaevolux.com.br/kit-10-plafons-led-embutir-redondo-18w-luz-branca-d18456310/p','https://www.linhaevolux.com.br/abajur-mesa-04-branco/p','https://www.linhaevolux.com.br/abajur-mesa-07-branco/p','https://www.linhaevolux.com.br/abajur-mesa-05-preto/p','https://www.linhaevolux.com.br/abajur-mesa-09-preto/p','https://www.linhaevolux.com.br/abajur-mesa-08-branco/p','https://www.linhaevolux.com.br/abajur-mesa-02-branco/p','https://www.linhaevolux.com.br/abajur-mesa-06-preto/p','https://www.linhaevolux.com.br/espelho-decorativo2-branco/p','https://www.linhaevolux.com.br/abajur-mesa-03-branco/p','https://www.linhaevolux.com.br/abajur-mesa-01-cinza/p','https://www.linhaevolux.com.br/escada-domesticas-aluminio-4-degraus-tools-004/p','https://www.linhaevolux.com.br/banqueta-escada-aluminio-3-degraus-tools-003/p','https://www.linhaevolux.com.br/bancada-dobravel-portatil-d181624/p','https://www.linhaevolux.com.br/escada-domesticas-aluminio-6-degraus-tools-006/p','https://www.linhaevolux.com.br/bancada-dobravel-portatil-d181625/p','https://www.linhaevolux.com.br/escada-domesticas-aluminio-3-degraus-tools-003/p','https://www.linhaevolux.com.br/bandeja-para-escada-multifuncional-d180360---evolux-tools/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-140x160-preta/p','https://www.linhaevolux.com.br/papel-de-parede-evolux-10x53-bege-linho/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-160x160-preta/p','https://www.linhaevolux.com.br/persiana-rolo-screen-180x220-champagne/p','https://www.linhaevolux.com.br/persiana-horizontal-off-140x130-preta/p','https://www.linhaevolux.com.br/persiana-horizontal-off-160x130-preta/p','https://www.linhaevolux.com.br/persiana-rolo-screen-220x220-branca/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-180x160-chumbo/p','https://www.linhaevolux.com.br/persiana-horizontal-premier-100x220-bege/p','https://www.linhaevolux.com.br/banqueta-escada-aluminio-2-degraus-tools-002/p','https://www.linhaevolux.com.br/lanterna-decorativa-25cm-branca/p','https://www.linhaevolux.com.br/persiana-rolo-rainbow-vertical-220x240-branca/p']

    def get_links2(self):
        colect = "//a[@class='product-image']/@href"
        for link in self.cats:
            a, b = link.split("#", 1)
            cont = int(b)
            while(cont > 0):
                link = a + "#" + str(cont)
                r = requests.get(link)
                print(link)
                html = parser.fromstring(r.text)
                cont -= 1
                self.parse_links(html, colect)

    def get_items(self):
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

    def JSON_CREATE(self, dic):
        JSON = json.dumps(dic, ensure_ascii=False)
        div = "<div class='especif'>"+JSON+"</div>"
        return div

    def clearshit(self, dic):
        for x in dic.keys():
            if x in self.remove:
                self.removed.append(x)
            if "Image" in x:
                self.removed.append(x)

        for a in self.removed:
            dic.pop(a, None)

        return dic

    def extract_item(self, html, link):
        EspList = {}
        teste = []
        check = len(html.xpath("//div[@class='title']/h1"))
        if(check == 0):
            try:
                nome = html.xpath(
                    "//div[@class='product-name hidden-xs']/h1/div")[0].text
            except IndexError as e:
                nome = "Not Found"

            try:
                cod = html.xpath("//div[@class='skuReference']")[0].text
            except IndexError as e:
                cod = "Not Found"

            try:
                de = html.xpath("//strong[@class='skuBestPrice']")[0].text
            except IndexError as e:
                de = "Not Found"

            try:
                por = html.xpath("//strong[@class='skuListPrice']")[0].text
            except IndexError as e:
                por = "Not Found"

            desc = html.xpath("//div[@class='productDescription']/text()")
            totaldesc = ""
            for x in desc:
                totaldesc += x + "<br>"

            EspList = dict(Nome=nome, Codigo=cod, PreçoDe=de,
                        PreçoPor=por, Descrição=totaldesc)

            attr = html.xpath("//div[@id='caracteristicas']//tr")
            for att in attr:
                EspList[att[0].text] = att[1].text

            imgs = html.xpath("//ul[@class='thumbs']/li//img/@src")

            imgcont = 1
            for img in imgs:
                img = img.replace("-55-55", "-800-800")
                img = urlsplit(img)._replace(query="").geturl()
                EspList["Imagem "+str(imgcont)] = img
                imgcont += 1
                try:
                    EAN = re.search("\d\d\d\d\d\d\d\d\d\d\d\d\d", img)
                    if EAN == None:
                        EAN = "Not Found"
                    else:
                        EAN = EAN.group(0)
                    teste.append(EAN)
                except IndexError as e:
                    EAN = "Not Found"

            contador = {x: teste.count(x) for x in set(teste)}
            maximum = max(contador, key=contador.get)

            EspList["EAN"] = maximum

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
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


print("LETS GET IT STARTED")


spider = EcommerceSpider("https://www.padovani.com.br/")
spider.crawl_to_file(filee+".csv")

spider.timewarn()
