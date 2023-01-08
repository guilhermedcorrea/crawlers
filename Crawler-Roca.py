import lxml.html as parser
import requests
import csv
from urllib.parse import urlsplit, urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time

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


class EcommerceSpider(object):
    def __init__(self, start_url):
        self.links = []
        self.items = []
        self.start_url = start_url
        self.base_url = "http://www.br.roca.com"
        self.key = []
        self.errors = 0
        self.pages = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None

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

        page_url_xpath = "//li[contains(@class,'three')]//li/a[@href]"
        prodhtml_xpath = "//li[@class='product-mosaic-list']/a[@href]"

        driver = webdriver.Chrome()
        driver.get(self.start_url)

        wait = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "product-mosaic")))
        scrollpage(driver)

        pagehtml = driver.find_elements_by_xpath(page_url_xpath)

        for a in pagehtml:
            self.pages.append(a.get_attribute("href"))

        for page in self.pages:
            driver.get(page)
            wait
            scrollpage(driver)
            IsProduct = driver.find_elements_by_xpath(
                "//li[@class='product-mosaic-list']")

            if(len(IsProduct) < 1):
                print("Não È PRODUTO MALUCO "+page)
                print(IsProduct)
                pagehtml = driver.find_elements_by_xpath(
                    "//div[@class='product-mosaic clear']//li//a[@href]")
                for pag in pagehtml:
                    self.pages.append(pag.get_attribute("href"))

            else:
                print("È PRODUTO "+page)
                prodhtml = driver.find_elements_by_xpath(
                    "//li[@class='product-mosaic-list']/a[@href]")
                for prod in prodhtml:
                    self.links.append(prod.get_attribute("href"))

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
        try:
            CodRef = html.xpath("//span[@itemprop='serialNumber']")[0]
            CodRef = blank(CodRef.text)
        except IndexError as e:
            CodRef = "NotFound"

        try:
            Linha = html.xpath("//span[@itemprop='name']")[0]
            Linha = blank(Linha.text)
        except IndexError as e:
            Linha = "NotFound"

        try:
            Nome = html.xpath("//span[@itemprop='description']")[0]
            Nome = blank(Nome.text)
        except IndexError as e:
            Nome = "NotFound"

        try:
            video = html.xpath(
                "//div[@class='videoWrapper']/iframe/@src")
        except IndexError as e:
            video = "Not Found"

        Prod_List = dict(CodRef=CodRef, Linha=Linha, Nome=Nome, Video=video)

        try:
            dimname = html.xpath(
                "//div[@class='column2-data dimensions']//span[@itemprop='propertyName']")
        except IndexError as e:
            dimname = "NotFound"
        try:
            dimval = html.xpath(
                "//div[@class='column2-data dimensions']//span[@itemprop='propertyValue']")
        except IndexError as e:
            dimval = "NotFound"

        try:
            dimunit = html.xpath(
                "//div[@class='column2-data dimensions']//span[@itemprop='unitText']")
            for x, y, z in zip(dimname, dimval, dimunit):
                dimn = blank(x.text).replace(":", "")
                dimv = blank(y.text) + " " + blank(z.text)
                Prod_List[dimn] = dimv
        except IndexError as e:
            dimunit = "NotFound"

        try:
            caracteristicas = html.xpath(
                "//div[@class='mobile-four twelve columns column2-data features-list data-column']/ul/li")
            for a in caracteristicas:
                caran = a[0][0].text.replace(":", "").replace(
                    "\n", "").replace("\t", "")
                try:
                    carav = a[1][0].text.replace(":", "").replace(
                        "\n", "").replace("\t", "")
                except IndexError as e:
                    carav = a[0][0].text.replace(":", "").replace(
                        "\n", "").replace("\t", "")
                Prod_List[caran] = carav
        except IndexError as e:
            caracteristicas = "NotFound"

        try:
            colecdesc = html.xpath(
                "//div[@class='six columns left-five']/p[1]")[0]
            colecdesc = blank(colecdesc.text)
        except IndexError as e:
            colecdesc = "NotFound"

        try:
            ficha = html.xpath("//li[@class='download-pdf']/a/@href")[0]
        except IndexError as e:
            ficha = "NotFound"

        try:
            alldim = html.xpath("//li[@class='popup-measures']/a/@href")[0]
        except IndexError as e:
            alldim = "Not Found"

        Prod_List["Descrição Coleção"] = colecdesc

        Prod_List["Ficha Técnica"] = self.base_url + str(ficha)
        Prod_List["Desenho Técnico"] = self.base_url + str(alldim)

        try:
            complemento = html.xpath("//li[@class='forty']//a/@href")
        except IndexError as e:
            complemento = "Not Found"

        contador = 1

        for b in complemento:
            Prod_List["Complemento "+str(contador)] = self.base_url + str(b)
            contador += 1

        try:
            contimg = 1
            images = html.xpath(
                "//div[@class='swiper-wrapper featured-product popup-gallery']//img/@src")
            for image in images:
                Prod_List["Imagem "+str(contimg)] = self.base_url + str(image)
                contimg += 1
        except IndexError as e:
            images = "Not Found"

        return Prod_List

    def parse_links(self, html, item_url_xpath):
        new_links = html.xpath(item_url_xpath)
        new_links = [self.prepare_url(l) for l in new_links]
        self.links = self.links.union(set(new_links))

    def set_base_url(self):
        self.base_url = urlsplit(self.start_url)._replace(
            path="", query="").geturl()

    def prepare_url(self, complement):
        url = self.base_url + complement
        return url

    def save_items(self, filename):
        self.create_dict()
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(f, fieldnames=self.key, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


spider = EcommerceSpider(
    "http://www.br.roca.com/catalogo/produtos/#!")
spider.crawl_to_file("Roca2.csv")
spider.timewarn()
