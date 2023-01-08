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
        self.items = []
        self.start_url = start_url
        self.base_url = "http://www.br.roca.com"
        self.name = []
        self.price = []
        self.errors = 0
        self.pages = []
        self.start_time = time.time()
        self.CodRef = ["7894200071167"]
        self.links = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None

    def timewarn(self):
        self.end_time = time.strftime("%b.%d-%X")
        print("Start : "+self.start_time + " End : "+self.end_time)

    def crawl(self, driver):
        self.get_links(driver)

    def crawl_to_file(self, filename):
        driver = webdriver.Chrome(
            'C:\Temp\TRAMPO\TEMP\SVN\Projetos\Python\ChromeDriver\chromedriver.exe')
        self.crawl(driver)
        self.save_items(filename)

    def get_links(self, driver):
        print("here iam")
        driver.get('https://www.google.com/shopping')
        for ID in self.CodRef:
            input_element = driver.find_element_by_name("q")
            input_element.clear()
            input_element.send_keys(ID)
            input_element.submit()
            time.sleep(5)

            pagecheck = len(driver.find_elements_by_xpath(
                "//div[@class='sh-dgr__content']"))

            if pagecheck == 0:
                try:
                    link = driver.find_elements_by_xpath(
                        "//div[@class='eIuuYe']//a[@href]")
                    link = link[0].get_attribute("href")
                    driver.get(link)
                    time.sleep(5)
                except IndexError as e:
                    link = "Not Found"

            else:
                print("ELSE")
                try:
                    link = driver.find_elements_by_xpath(
                        "//div[@class='sh-dgr__content']/a[@href]")
                    link = link[0].get_attribute("href")
                    driver.get(link)
                    time.sleep(5)
                except IndexError as e:
                    link = "Not Found"

                # Filtra para a pagina com mais infos

            try:
                print("ABSOLUITE")
                time.sleep(5)
                absolutelink = driver.find_elements_by_xpath(
                    "//a[@class='pag-detail-link']")
                time.sleep(5)
                print(absolutelink)
                absolutelink = absolutelink[0].get_attribute("href")
                print(absolutelink)
                driver.get(absolutelink)
                self.extract_item(driver, ID)
                self.links.append(absolutelink)
            except IndexError as e:
                absolutelink = "Not Found"

    def extract_item(self, driver, ID):
        print("IHASAMA")
        scrollpage(driver)
        names = driver.find_elements_by_xpath(
            "//span[@class='os-seller-name-primary']/a")

        self.name = []
        self.pric = []

        for nam in names:
            self.name.append(nam.text)

        prices = driver.find_elements_by_xpath(
            "//span[@class='tiOgyd']")

        for pric in prices:
            self.price.append(pric.text)

            # IHA = verificador de next page
        IHA = 0

        while IHA == 0:
            test = driver.find_elements_by_xpath(
                "//div[contains(@class ,'jfk-button-disabled') and @id='online-next-btn']")
            test = len(test)
            print("-------------------------------------------")
            if test < 1:
                driver.find_element_by_id('online-next-btn').click()
                scrollpage(driver)
                names2 = driver.find_elements_by_xpath(
                    "//span[@class='os-seller-name-primary']/a")

                for nam2 in names2:
                    self.name.append(nam2.text)

                prices2 = driver.find_elements_by_xpath(
                    "//span[@class='tiOgyd']")

                for pric2 in prices2:
                    self.price.append(pric2.text)
                time.sleep(2)
            else:
                IHA = 1
                print("ACABOU")

        lastcont = 0
        while lastcont < len(self.name):
            bleh = dict(
                CODREF=ID, Player=self.name[lastcont], Price=self.price[lastcont])
            self.items.append(bleh)
            lastcont += 1

    def parse_links(self, html, item_url_xpath):
        new_links = html.xpath(item_url_xpath)
        new_links = [self.prepare_url(l) for l in new_links]
        self.links = self.links.union(set(new_links))

    def set_base_url(self):
        self.base_url = urlsplit(self.start_url)._replace(
            path="", query="").geturl()

    def prepare_url(self, complement):
        url = urljoin(self.base_url)
        return urlsplit(url).geturl()

    def save_items(self, filename):
        fieldnames = ["CODREF", "Player", "Price"]
        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


spider = EcommerceSpider(
    "http://www.br.roca.com/catalogo/produtos/#!")
spider.crawl_to_file("GShop.csv")
spider.timewarn()
