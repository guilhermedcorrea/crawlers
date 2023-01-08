import lxml.html as parser
import requests
import csv
import time
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


def blank(texto):
    if(texto != None):
        Noblank = " ".join(texto.split())
        return Noblank


class EcommerceSpider(object):
    def __init__(self, start_url):
        self.links = {}
        self.items = []
        self.start_url = start_url
        self.set_base_url()
        self.key = []
        self.errors = 0
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.testerror = []
        self.file = "leroy.csv"
        self.CodRef = []
        self.remove = ["Descrição 2", "Categoria", "Descrição2",
                       "SKU", "cat", "DescInfo", "Foto", "VIXI"]
        self.removed = []

    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    self.errors += 1
                else:
                    self.key.append(check)

    def CSVREADER(self):
        with open(self.file, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.CodRef.append(row["CODREF"])
                self.links[row["CODREF"]] = row["URL"]

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

    def timewarn(self):
        self.end_time = time.strftime("%b.%d-%X")
        print("Start : "+self.start_time + " End : "+self.end_time)

    def crawl(self):
        self.get_links()
        session = requests.Session()

        r = session.get(self.start_url)
        self.get_items(session)

    def GetCatLinks(self, html):
        SubCats = html.xpath(
            "//a[contains(@class ,'thumb-item margin-top')]")

        for href in SubCats:
            url = href.attrib["href"]
            url = urljoin(self.start_url, url)
            url = urlsplit(url)._replace(query="").geturl()
            self.Clinks[href.attrib["title"]] = url

        SubCats2 = html.xpath("//div[@class='thumb-item margin-top']/a")

        for href in SubCats2:
            url = href.attrib["href"]
            url = urljoin(self.start_url, url)
            url = urlsplit(url)._replace(query="").geturl()
            self.Clinks[href.attrib["title"]] = url

        for cnames in self.Clinks.keys():
            self.Cnames.append(cnames)

        self.Cnames = list(set(self.Cnames))

    def crawl_to_file(self, filename):
        self.crawl()
        self.save_items(filename)

    def get_links(self):
        self.CSVREADER()

    def get_items(self, session):
        for ID in self.CodRef:
            r = session.get(self.links[ID])
            html = parser.fromstring(r.text)
            print(str(r) + " : " + self.links[ID])
            self.items.append(self.extract_item(html, self.links[ID], ID))

    def extract_item(self, html, link):
        Prod_List = {}

        try:
            Nome = html.xpath(
                "//h1[@class='product-title align-left color-text product-description']")[0].text
            Nome = blank(Nome)
        except IndexError as e:
            Nome = "NotFound"

        try:
            Description = html.xpath(
                "//div[@class='product-text-description']/div[1]//p/text()")[0]
        except IndexError as e:
            Description = "Não Encontrado"

        try:
            CodRef = blank(html.xpath(
                "//div[@class='badge product-code']")[0].text)
        except IndexError as e:
            CodRef = "Not Found"

        Prod_List = dict(Nome=Nome, Descrição=Description, CodRef=CodRef)

        try:
            Attributos = html.xpath(
                "//div[@class='characteristics-container']//tr")
            for a in Attributos:
                Prod_List[a[0].text] = a[1].text
        except IndexError as e:
            Attributos = "Not Found"

        try:
            IMGS = html.xpath(
                "//div[@class='product-carousel']//div[@class='carousel']")[0]
            # div[@class='carousel-wrapper']/div")
        except IndexError as e:
            IMGS = "Not Found"

        JSONSTR = IMGS.attrib["data-items"]
        JSONSTR = json.loads(JSONSTR)
        imgcont = 1

        for x in JSONSTR:
            Prod_List["Imagem "+str(imgcont)] = x["url"]
            imgcont += 1

        try:
            mpn = html.xpath("//span[@itemprop='mpn']/@content")[0]
            Prod_List["MPN"] = mpn
        except IndexError as e:
            mpn = "Not Found"
            Prod_List["MPN"] = mpn

        try:
            brand = html.xpath("//span[@itemprop='brand']/@content")[0]
            Prod_List["Brand"] = brand
        except IndexError as e:
            brand = "Not Found"
            Prod_List["Brand"] = brand

        try:
            Desc2 = html.xpath("//span[@itemprop='description']/@content")[0]
            Prod_List["Descrição 2"] = Desc2
        except IndexError as e:
            Desc2 = "Not Found"
            Prod_List["Descrição 2"] = Desc2

        try:
            de = html.xpath("//span[@class='price-integer']")[0].text
            Prod_List["Preço"] = de
        except IndexError as e:
            de = "Not Found"
            Prod_List["Preço"] = de

        teste = dict(Prod_List)
        teste = self.clearshit(teste)
        Prod_List["JSON"] = self.JSON_CREATE(teste)

        return Prod_List

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
        with open(filename, 'w', encoding="utf-8") as f:
            dict_writer = csv.DictWriter(f, fieldnames=self.key, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)
        self.items = []
        self.links = set()


print("LETS GET IT STARTED")

spider = EcommerceSpider(
    "https://www.leroymerlin.com.br/localizacao/store/?local=campinas")

spider.crawl_to_file("Leroy CADASTRO.csv")

spider.timewarn()
