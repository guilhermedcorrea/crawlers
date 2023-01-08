import lxml.html as parser
import requests
import csv
import time
import re
import unidecode
import json
from lxml import etree
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


filee = "GAAM"

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
        self.links = ['https://www.gaamstore.com.br/Look/5/Kit-Estantes.aspx ', 'https://www.gaamstore.com.br/Look/5/Kit-Estantes.aspx ', 'https://www.gaamstore.com.br/Look/4/Conjunto-de-ModuloPrateleira.aspx ', 'https://www.gaamstore.com.br/modulo-inteligente-wenguewengue-141/p ', 'https://www.gaamstore.com.br/prateleira-400-multiuso-com-suporte-invisivel-133/p ', 'https://www.gaamstore.com.br/prateleira-600-multiuso-com-suporte-invisivel-134/p ', 'https://www.gaamstore.com.br/prateleira-800-multiuso-com-suporte-invisivel-135/p ', 'https://www.gaamstore.com.br/prateleira-1000-multiuso-com-suporte-invisivel-136/p ', 'https://www.gaamstore.com.br/estante-madeira-sarin-com-04-prateleiras-em-mdp-bp-15-mm-rovere-130/p ', 'https://www.gaamstore.com.br/estante-madeira-aludra-com-cabideiro-e-02-prateleiras-em-mdp-bp-15-mm-129/p ', 'https://www.gaamstore.com.br/modulo-aereo-250-multiuso-124/p ', 'https://www.gaamstore.com.br/modulo-aereo-400-multiuso-125/p ', 'https://www.gaamstore.com.br/modulo-aereo-600-multiuso-126/p ', 'https://www.gaamstore.com.br/modulo-aereo-800-multiuso-127/p ', 'https://www.gaamstore.com.br/prateleira-600-multiuso-com-suporte-de-aluminio-zincado-115/p ', 'https://www.gaamstore.com.br/prateleira-800-multiuso-com-suporte-de-aluminio-zincado-116/p ', 'https://www.gaamstore.com.br/prateleira-1000-multiuso-com-suporte-de-aluminio-zincado-117/p ', 'https://www.gaamstore.com.br/bandeja-pequena-42-x-160-x-280-branco-com-granito-verde-118/p ', 'https://www.gaamstore.com.br/bandeja-pequena-42-x-160-x-280-cinza-com-granito-verde-119/p ', 'https://www.gaamstore.com.br/bandeja-pequena-42-x-160-x-280-cobre-com-granito-natural-120/p ', 'https://www.gaamstore.com.br/bandeja-pequena-42-x-160-x-280-preto-com-granito-natural-121/p ', 'https://www.gaamstore.com.br/bandeja-media-42-x-200-x-280-cobre-com-granito-natural-92/p ', 'https://www.gaamstore.com.br/modulo-gaveta-600-hidrus-com-rodizio-brancobranco-73/p ', 'https://www.gaamstore.com.br/modulo-gaveta-600-hidrus-com-rodizio-ameixaameixa-74/p ', 'https://www.gaamstore.com.br/bandeja-grande-42-x-230-x-330-cinza-com-granito-verde-19/p ', 'https://www.gaamstore.com.br/bandeja-grande-42-x-230-x-330-preto-com-granito-natural-20/p ', 'https://www.gaamstore.com.br/bandeja-grande-42-x-230-x-330-cobre-com-granito-natural-21/p ', 'https://www.gaamstore.com.br/bandeja-media-42-x-200-x-280-branco-com-granito-verde-22/p ', 'https://www.gaamstore.com.br/bandeja-media-42-x-200-x-280-cinza-com-granito-verde-23/p ', 'https://www.gaamstore.com.br/bandeja-media-42-x-200-x-280-preto-com-granito-natural-24/p ', 'https://www.gaamstore.com.br/bandeja-grande-42-x-230-x-330-branco-com-granito-verde-18/p ', 'https://www.gaamstore.com.br/prateleira-400-multiuso-com-suporte-de-aluminio-zincado-11/p ', 'https://www.gaamstore.com.br/estante-madeira-polaris-com-04-prateleiras-13/p ', 'https://www.gaamstore.com.br/estante-madeira-adhara-com-05-prateleiras-7/p ', 'https://www.gaamstore.com.br/estante-madeira-mira-com-03-prateleiras-8/p ', 'https://www.gaamstore.com.br/estante-madeira-sarin-com-04-prateleiras-em-mdp-15-mm-9/p ', 'https://www.gaamstore.com.br/gabinete-700-safira-com-pe-grigiobranco-individual-220/p ', 'https://www.gaamstore.com.br/gabinete-700-safira-com-pe-ameixabranco-individual-218/p ', 'https://www.gaamstore.com.br/tampo-800-alba-com-cuba-embutida-verde-ubatuba-individual-215/p ', 'https://www.gaamstore.com.br/gabinete-800-alba-suspenso-ameixagrigio-individual-216/p ', 'https://www.gaamstore.com.br/Look/7/Conjunto-800-Alba-Suspenso-com-Espelheira-750-Safira.aspx ', 'https://www.gaamstore.com.br/Look/6/Conjunto-Pratice.aspx ', 'https://www.gaamstore.com.br/gabinete-de-coluna-470-pratice-com-rodizio-wenguerovere-214/p ', 'https://www.gaamstore.com.br/Look/3/Conjunto-810-Oroch.aspx ', 'https://www.gaamstore.com.br/balcao-desmontado-omega-1140-com-pe-brancobranco-209/p ', 'https://www.gaamstore.com.br/balcao-desmontado-omega-1440-com-pe-brancobranco-210/p ', 'https://www.gaamstore.com.br/balcao-desmontado-omega-1440-com-pe-wenguerovere-211/p ', 'https://www.gaamstore.com.br/balcao-desmontado-omega-1140-com-pe-wenguerovere-212/p ', 'https://www.gaamstore.com.br/Look/2/Gabinete-1000-Savana-com-Tampo-e-Espelheira.aspx ', 'https://www.gaamstore.com.br/gabinete-1000-savana-suspenso-branco-com-porta-vidro-branco-individual-202/p ', 'https://www.gaamstore.com.br/gabinete-1000-savana-suspenso-branco-com-porta-vidro-preto-individual-203/p ', 'https://www.gaamstore.com.br/gabinete-1000-savana-suspenso-ameixa-com-porta-vidro-branco-individual-204/p ', 'https://www.gaamstore.com.br/gabinete-1000-savana-suspenso-ameixa-com-porta-vidro-preto-individual-205/p ', 'https://www.gaamstore.com.br/bancada-1000-savana-verde-individual-200/p ', 'https://www.gaamstore.com.br/bancada-1000-savana-amarelo-individual-201/p ', 'https://www.gaamstore.com.br/tampo-multifuncional-725-x-410-x-20-individual-196/p ', 'https://www.gaamstore.com.br/gabinete-700-savana-suspenso-ameixaameixa-individual-197/p ', 'https://www.gaamstore.com.br/conjunto-600-pop-com-pe-brancobranco-com-pia-e-espelheira-191/p ', 'https://www.gaamstore.com.br/conjunto-600-pop-com-pe-brancopreto-com-pia-e-espelheira-192/p ', 'https://www.gaamstore.com.br/gabinete-700-safira-suspenso-brancobranco-individual-193/p ', 'https://www.gaamstore.com.br/gabinete-700-safira-suspenso-ameixabranco-individual-194/p ', 'https://www.gaamstore.com.br/tampo-multifuncional-725-x-410-x-20-travertino-individual-195/p ', 'https://www.gaamstore.com.br/quadro-espelho-900-x-700-x-20-octogonal-brancobranco-190/p ', 'https://www.gaamstore.com.br/espelheira-1000-x-450-multiuso-brancobranco-184/p ', 'https://www.gaamstore.com.br/espelheira-1000-x-550-multiuso-brancobranco-185/p ', 'https://www.gaamstore.com.br/espelheira-1000-x-750-multiuso-brancobranco-186/p ', 'https://www.gaamstore.com.br/espelheira-1000-x-450-light-brancobranco-187/p ', 'https://www.gaamstore.com.br/espelheira-1000-x-550-light-brancobranco-188/p ', 'https://www.gaamstore.com.br/espelheira-1000-x-750-light-brancobranco-189/p ', 'https://www.gaamstore.com.br/bancada-700-savana-verde-individual-140/p ', 'https://www.gaamstore.com.br/espelheira-750-safira-brancobranco-137/p ', 'https://www.gaamstore.com.br/espelheira-750-safira-grigiogrigio-138/p ', 'https://www.gaamstore.com.br/espelheira-750-safira-ameixaameixa-139/p ', 'https://www.gaamstore.com.br/conjunto-550-tokyo-suspenso-wenguerovere-com-cuba-e-quadro-espelho-131/p ', 'https://www.gaamstore.com.br/conjunto-550-tokyo-suspenso-rovererovere-com-cuba-e-quadro-espelho-132/p ', 'https://www.gaamstore.com.br/conjunto-500-paris-suspenso-wenguewengue-com-pia-e-quadro-espelho-128/p ', 'https://www.gaamstore.com.br/conjunto-500-paris-suspenso-wenguerovere-com-pia-e-quadro-espelho-122/p ', 'https://www.gaamstore.com.br/conjunto-500-paris-suspenso-roverewengue-com-pia-e-quadro-espelho-123/p ', 'https://www.gaamstore.com.br/gabinete-700-savana-suspenso-brancobranco-individual-113/p ', 'https://www.gaamstore.com.br/bancada-700-savana-travertino-individual-114/p ', 'https://www.gaamstore.com.br/quadro-espelho-1000-x-750-x-20-savana-brancobranco-107/p ', 'https://www.gaamstore.com.br/quadro-espelho-800-x-600-x-20-brancobranco-108/p ', 'https://www.gaamstore.com.br/quadro-espelho-513-x-410-x-20-brancobranco-109/p ', 'https://www.gaamstore.com.br/quadro-espelho-513-x-410-x-20-wenguewengue-110/p ', 'https://www.gaamstore.com.br/quadro-espelho-513-x-410-x-20-rovererovere-111/p ',
                      'https://www.gaamstore.com.br/valvula-pop-up-externa-silver-sem-ladrao-da-agua-100/p ', 'https://www.gaamstore.com.br/valvula-pop-up-externa-black-sem-ladrao-da-agua-101/p ', 'https://www.gaamstore.com.br/valvula-pop-up-externa-gold-sem-ladrao-da-agua-102/p ', 'https://www.gaamstore.com.br/valvula-pop-up-externa-rose-gold-matte-com-ladrao-da-agua-104/p ', 'https://www.gaamstore.com.br/conjunto-500-eros-suspenso-ameixagrigio-com-tampo-amarelo-e-quadro-espelho-bisote-105/p ', 'https://www.gaamstore.com.br/conjunto-500-eros-suspenso-rovererovere-com-tampo-verde-e-quadro-espelho-bisote-106/p ', 'https://www.gaamstore.com.br/valvula-de-escoamento-inox-e-abs-96/p ', 'https://www.gaamstore.com.br/valvula-de-escoamento-inox-e-abs-96/p ', 'https://www.gaamstore.com.br/lixeira-multiuso-retangular-06-litros-aco-escovado-com-tampa-preta-97/p ', 'https://www.gaamstore.com.br/lixeira-multiuso-retangular-06-litros-slim-preta-98/p ', 'https://www.gaamstore.com.br/gabinete-500-eros-suspenso-rovererovere-com-tampo-verde-99/p ', 'https://www.gaamstore.com.br/kit-balcao-tanque-ecco-30-litros-com-pe-rovererovere-e-tanque-branco-93/p ', 'https://www.gaamstore.com.br/kit-balcao-tanque-ecco-30-litros-com-pe-rovererovere-e-tanque-granitado-94/p ', 'https://www.gaamstore.com.br/valvula-pop-up-interna-sem-ladrao-da-agua-prata-95/p ', 'https://www.gaamstore.com.br/bancada-630-oroch-suspensa-135-x-630-x-410-91/p ', 'https://www.gaamstore.com.br/bancada-810-oroch-suspensa-135-x-810-x-410-90/p ', 'https://www.gaamstore.com.br/valvula-pop-up-externa-sem-ladrao-da-agua-prata-86/p ', 'https://www.gaamstore.com.br/kit-balcao-tanque-ecco-30-litros-com-pe-wenguewengue-e-tanque-branco-87/p ', 'https://www.gaamstore.com.br/kit-balcao-tanque-ecco-30-litros-com-pe-wenguewengue-e-tanque-granitado-88/p ', 'https://www.gaamstore.com.br/escova-para-vaso-sanitario-com-suporte-83/p ', 'https://www.gaamstore.com.br/lixeira-multiuso-05-litros-com-tampa-preta-84/p ', 'https://www.gaamstore.com.br/lixeira-multiuso-05-litros-com-tampa-vermelha-85/p ', 'https://www.gaamstore.com.br/gabinete-500-eros-suspenso-ameixagrigio-com-tampo-amarelo-82/p ', 'https://www.gaamstore.com.br/kit-acessorios-para-banheiro-diamante-75/p ', 'https://www.gaamstore.com.br/kit-acessorios-para-banheiro-silver-56/p ', 'https://www.gaamstore.com.br/espelheira-700-onix-brancobranco-16/p ', 'https://www.gaamstore.com.br/espelheira-700-onix-ameixaameixa-17/p ', 'https://www.gaamstore.com.br/espelheira-click-com-abertura-lateral-brancobranco-14/p ', 'https://www.gaamstore.com.br/espelheira-click-com-abertura-lateral-ameixaameixa-15/p ', 'https://www.gaamstore.com.br/Look/1/Gabinete-700-Savana-com-Tampo.aspx ', 'https://www.gaamstore.com.br/cuba-louca-oval-145-x-490-x-345-dourada-213/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-oval-145-x-490-x-345-dourada-213/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-170-x-420-x-420-branca-com-dourada-208/p?cc=51 ', 'https://www.gaamstore.com.br/valvula-pop-up-externa-silver-sem-ladrao-da-agua-100/p?cc=51 ', 'https://www.gaamstore.com.br/valvula-pop-up-externa-black-sem-ladrao-da-agua-101/p?cc=51 ', 'https://www.gaamstore.com.br/valvula-pop-up-externa-gold-sem-ladrao-da-agua-102/p?cc=51 ', 'https://www.gaamstore.com.br/valvula-pop-up-externa-rose-gold-matte-com-ladrao-da-agua-104/p?cc=51 ', 'https://www.gaamstore.com.br/valvula-de-escoamento-inox-e-abs-96/p?cc=51 ', 'https://www.gaamstore.com.br/valvula-pop-up-interna-sem-ladrao-da-agua-prata-95/p?cc=51 ', 'https://www.gaamstore.com.br/valvula-pop-up-externa-sem-ladrao-da-agua-prata-86/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-quadrada-150-x-415-x-415-branca-79/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-vidro-redonda-150-x-425-x-425-preta-mesclada-63/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-vidro-redonda-150-x-420-x-420-vermelha-mesclado-branco-64/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-vidro-redonda-150-x-425-x-425-preta-com-efeito-gotas-69/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-bari-retangular-110-x-496-x-387-branca-70/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-retangular-110-x-500-x-390-branca-71/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-quadrada-110-x-390-x-390-branca-72/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-retangular-140-x-570-x-460-branca-com-valvula-oculta-57/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-vidro-oval-retangular-130-x-470-x-300-white-58/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-vidro-oval-retangular-130-x-470-x-300-red-59/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-vidro-redonda-150-x-420-x-420-vermelha-madeirada-62/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-oval-retangular-135-x-610-x-410-branca-47/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-110-x-360-x-360-preta-com-acabamento-externo-frisado-48/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-quadrada-135-x-385-x-385-branca-com-borda-prata-49/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-vidro-redonda-130-x-385-x-385-white-50/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-vidro-redonda-130-x-385-x-385-red-51/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-vidro-redonda-130-x-385-x-385-clear-53/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-vidro-redonda-130-x-385-x-385-sandblast-54/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-150-x-400-x-400-branca-com-rosa-34/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-quadrada-125-x-430-x-430-branca-35/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-quadrada-125-x-430-x-430-branca-com-borda-dourada-36/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-140-x-460-x-460-branca-com-lilas-37/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-140-x-460-x-460-branca-com-marrom-38/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-quadrada-125-x-430-x-430-branca-com-borda-prata-39/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-retangular-130-x-480-x-380-branca-com-detalhe-rosa-40/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-150-x-430-x-430-rose-gold-matte-41/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-130-x-435-x-435-branca-42/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-195-x-490-x-470-branca-43/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-quadrada-160-x-435-x-435-branca-44/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-135-x-380-x-365-branca-com-borda-e-detalhe-prata-46/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-oval-retangular-150-x-590-x-410-marrom-mesclado-29/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-retangular-140-x-495-x-400-branca-mesclada-30/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-retangular-140-x-495-x-400-cinza-mesclada-31/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-155-x-310-x-310-prata-25/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-155-x-310-x-310-dourada-26/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-retangular-130-x-480-x-370-branca-27/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-quadrada-140-x-430-x-430-branca-12/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-150-x-405-x-405-dourada-4/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-150-x-405-x-405-prata-5/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-redonda-140-x-460-x-460-branca-com-cinza-6/p?cc=51 ', 'https://www.gaamstore.com.br/cuba-louca-quadrada-135-x-385-x-385-branca-com-borda-dourada-2/p?cc=51', 'https://www.gaamstore.com.br/cuba-louca-quadrada-160-x-470-x-470-branca-3/p?cc=51']

    def get_items(self):
        for link in self.links:
            r = requests.get(link, headers)
            r.encoding = 'latin-1'
            html = parser.fromstring(r.content)
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
        try:
            nome = html.xpath(
                "//h1[@id='productName']")[0].text.replace("\n", "").replace("\r", "").strip(" ")
        except IndexError as e:
            nome = "Not Found"
        try:
            sku = html.xpath(
                "//span[@itemprop='mpn']")[0].text.replace("\n", "").replace("\r", "").strip(" ")
        except IndexError as e:
            sku = "Not Found"
        EspList = dict(Nome=nome, Sku=sku)
        carac = html.xpath("//div[@id='specificationContent']//tr")
        for x in carac:
            EspList[x[0].text] = x[1].text
        desc = html.xpath("//div[@id='descriptionContent']//text()")
        cont = 1
        totaldesc = ""
        for x in desc:
            x = x.replace("\n", "").replace("\r", "").strip(" ")
            if(":" in x):
                a, b = x.split(":", 1)
                EspList[formatar(a)] = b
            elif("*" in x or "-" in x):
                EspList["Atributo "+str(cont)] = x.replace("*", "")
                cont += 1
            else:
                totaldesc += x + " <br> "

        imagem = html.xpath("//ul[@class='thumbs']//img/@src")
        imgcont = 1
        for img in imagem:
            if(".gif" in img):
                None
            else:
                EspList["Imagem "+str(imgcont)] = self.prepare_url(img)
                imgcont += 1
        EspList["Descrição"] = totaldesc

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
    "https://www.gaamstore.com.br/Look/5/Kit-Estantes.aspx")
spider.crawl_to_file(filee+".csv")

spider.timewarn()
