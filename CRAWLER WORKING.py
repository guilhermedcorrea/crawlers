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

    def crawl(self):
        self.get_links()
        self.get_items()

    def crawl_to_file(self, filename):
        self.crawl()
        self.save_items(filename)

    def get_links(self):
        item_url_xpath = "//div[@class='product__image']/a/@href"
        next_page_xpath = "//ul[@class='pagination']/li[position()=6]/a/@href"
        r = requests.get(self.start_url)
        html = parser.fromstring(r.text)
        self.parse_links(html, item_url_xpath)
        next_page = html.xpath(next_page_xpath)[0]
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
            r = requests.get(link)
            html = parser.fromstring(r.text)
            self.items.append(self.extract_item(html, link))

    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    print("Duplicado")
                else:
                    self.key.append(check)

    def extract_item(self, html, link):
        try:
            name = html.xpath(
                "//h1[@class='title is-medium product-title']")[0]
            name = blank(name.text)
        except IndexError as e:
            print("name not found at page %s" % link)
            name = "Not found"

        try:
            description = html.xpath(
                "// div[@class='product-description']/p[@class='description']")[0]
            description = blank(description.text)
        except IndexError as e:
            print("Name not found at page %s" % link)
            description = "Not found"

        try:
            CodRef = html.xpath(
                "//span[2][@class='reference-block__item']")[0]
            CodRef = blank(CodRef.text)
        except IndexError as e:
            print("CodRef not found at page %s" % link)
            CodRef = "Not found"

        try:
            attribute = html.xpath(
                "//div[1][@id='product-attributes-tab-information']/table/tbody")
        except IndexError as e:
            print("Attributos não encontrados na pagina $s" % link)

        EspList = {}

        EspList = dict(Name=name, CodRef=CodRef, Description=description)

        for x in attribute[0]:
            if(x[1].text != None):
                EspList[x[0][0].text] = blank(x[1].text)
            else:
                EspList[x[0][0].text] = 0
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
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(f, fieldnames=self.key, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


spider = EcommerceSpider("https://www.madeiramadeira.com.br/busca?q=Taschibra")
spider.crawl_to_file("taschibra.csv")
print(spider.key)
print(spider.items)
