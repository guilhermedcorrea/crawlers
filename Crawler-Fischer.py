import lxml.html as parser
import requests
import csv
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
        self.links = set()
        self.items = []
        self.start_url = start_url
        self.set_base_url()
        self.key = []
        self.errors = 0
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None

    def crawl(self):
        self.get_links()
        self.get_items()

    def crawl_to_file(self, filename):
        self.crawl()
        self.save_items(filename)

    def timewarn(self):
        self.end_time = time.strftime("%b.%d-%X")
        print("Start : "+self.start_time + " End : "+self.end_time)

    def get_links(self):
        item_url_xpath = "//div[@class='imagem-produto-home']/a/@href"
        next_page_xpath = "//a[@class='next ']/@href"
        catlinks_xpath = "//ul[@class='cat']/li/a/@href"

        r = requests.get(self.start_url)
        html = parser.fromstring(r.text)

        self.parse_links(html, item_url_xpath)
        catlinks = html.xpath(catlinks_xpath)

        for category in catlinks:
            r = requests.get(category)
            html = parser.fromstring(r.text)
            self.parse_links(html, item_url_xpath)
            try:
                next_page = html.xpath(next_page_xpath)[0]
            except IndexError as e:
                next_page = None

            while next_page:
                r = requests.get(urljoin(self.base_url, next_page))
                html = parser.fromstring(r.text)
                self.parse_links(html, item_url_xpath)
                try:
                    next_page = html.xpath(next_page_xpath)[0]
                except IndexError as e:
                    next_page = None

    def get_items(self):
        for link in self.links:
            print(link)
            r = requests.get(link)
            html = parser.fromstring(r.text)
            print(r)
            self.items.append(self.extract_item(html, link))

    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    self.errors += 1
                else:
                    self.key.append(check)

    def extract_item(self, html, link):
        Prod_list = {}
        try:
            Nome = html.xpath("//div[@class='product-name']//h1")[0].text
        except IndexError as e:
            Nome = "Not Found"

        try:
            CodRef = html.xpath(
                "//div[@class='cod-estoque']/span[@class='cod']")[0].text
        except IndexError as e:
            CodRef = "Not Found"

        try:
            desc = html.xpath("//div[@class='short-description']/div/p/span")
            full_desc = ""
            for span in desc:
                full_desc += str(span.text)
        except IndexError as e:
            full_desc = "Not Found"

        try:
            detalhes = html.xpath("//div[@class='descricao']/p/span")
            det_list = []
            for det in detalhes:
                det_list.append(det.text)
        except IndexError as e:
            det_list = "Not Found"

        Prod_list = dict(Nome=Nome, CodRef=CodRef,
                         Descrição=full_desc, Detalhes=det_list)

        try:
            infos = html.xpath("//div[@class='info-tecnica']/ul/li/span")
            cont = 1

            for inf in infos:
                if(inf.text != None):
                    try:
                        Ref, Resp = inf.text.split(":", 1)
                        Prod_list[Ref] = Resp
                    except ValueError as e:
                        Prod_list["SemReferencia "+str(cont)] = inf.text
                        cont += 1

        except IndexError as e:
            infos = "Not Found"

        try:
            manuais = html.xpath("//div[@class='manuais']/ul/li/a/@href")
            mancont = 1

            for manual in manuais:
                Prod_list["Manual "+str(mancont)] = manual
                mancont += 1

        except IndexError as e:
            manuais = "Not Found"

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
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(f, fieldnames=self.key, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


spider = EcommerceSpider(
    "https://loja.fischer.com.br/eletroportateis/c")
spider.crawl_to_file("FischerNEW.csv")
