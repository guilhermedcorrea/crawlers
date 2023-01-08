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
        self.links = set()
        self.items = []
        self.start_url = start_url
        self.set_base_url()
        self.key = []
        self.errors = 0
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.testerror = []
        self.Clinks = {}
        self.Depnames = ['Banheiros']
        # , 'Cozinhas e Áreas de Serviço', 'Pisos e Revestimentos', 'Organização da Casa', 'Jardim e Varanda', 'Decoração', 'Tapetes', 'Iluminação', 'Climatização e Ventilação', 'Ferramentas', 'Ferragens',
                        #'Materiais de Construção', 'Materiais Elétricos', 'Materiais Hidráulicos', 'Madeiras', 'Portas, Janelas e Portões', 'Tintas e Acessórios', 'Segurança eComunicação', 'Manutenção e Limpeza da Casa', 'Eletroportáteis', 'Eletrodomésticos', 'Móveis']
    
        self.Departments = {'Banheiros': 'https://www.leroymerlin.com.br/banheiros', 'Cozinhas e Áreas de Serviço': 'https://www.leroymerlin.com.br/cozinhas-e-areas-de-servico', 'Pisos e Revestimentos': 'https://www.leroymerlin.com.br/pisos-e-revestimentos', 'Organização da Casa': 'https://www.leroymerlin.com.br/organizacao', 'Jardim e Varanda': 'https://www.leroymerlin.com.br/jardim-e-lazer', 'Decoração': 'https://www.leroymerlin.com.br/decoracao', 'Tapetes': 'https://www.leroymerlin.com.br/tapetes',
                            'Iluminação': 'https://www.leroymerlin.com.br/iluminacao', 'Climatização e Ventilação': 'https://www.leroymerlin.com.br/climatizacao-e-ventilacao', 'Ferramentas': 'https://www.leroymerlin.com.br/ferramentas', 'Ferragens': 'https://www.leroymerlin.com.br/ferragens', 'Materiais de Construção': 'https://www.leroymerlin.com.br/materiais-de-construcao', 'Materiais Elétricos': 'https://www.leroymerlin.com.br/materiais-eletricos', 'Materiais Hidráulicos': 'https://www.leroymerlin.com.br/materiais-hidraulicos', 'Madeiras': 'https://www.leroymerlin.com.br/marcenaria-e-madeiras', 'Portas, Janelas e Portões': 'https://www.leroymerlin.com.br/portas-janelas-e-portoes', 'Tintas e Acessórios': 'https://www.leroymerlin.com.br/tintas-e-acessorios', 'Segurança e Comunicação': 'https://www.leroymerlin.com.br/seguranca-e-comunicacao', 'Manutenção e Limpeza da Casa': 'https://www.leroymerlin.com.br/limpeza-e-manutencao', 'Eletroportáteis': 'https://www.leroymerlin.com.br/eletroportateis', 'Eletrodomésticos': 'https://www.leroymerlin.com.br/eletrodomesticos', 'Móveis': 'https://www.leroymerlin.com.br/moveis'}
        self.badies = []
        self.Cnames = []
	
    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    self.errors += 1
                else:
                    self.key.append(check)

    def timewarn(self):
        self.end_time = time.strftime("%b.%d-%X")
        print("Start : "+self.start_time + " End : "+self.end_time)
    
    def JSON_CREATE(self, dic):
        JSON = json.dumps(dic, ensure_ascii=False)
        div = "<div class='especif'>"+JSON+"</div>"
        return div

    def crawl(self):
        session = requests.Session()
        for Dep in self.Depnames:
            filename = "Leroy-"+Dep+".csv"
                    
            r = session.get(self.start_url)
            
            r = session.get(self.Departments[Dep])

            html = parser.fromstring(r.text)

            self.GetCatLinks(html)

            for cname in self.Cnames:
                r = session.get(self.Clinks[cname])
                html = parser.fromstring(r.text)

                checkprod = len(html.xpath(
                    "//div[@class='row product-list-filter margin-bottom-double align-center']"))

                if(checkprod > 0):
                    None
                else:
                    self.badies.append(cname)
                    self.GetCatLinks(html)

            self.Cnames = list(set(self.Cnames) - set(self.badies))

            for cat in self.Cnames:
                self.get_links(session,cat)
            
            self.Cnames = []
            self.get_items(session)
            self.save_items(filename)

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

    def crawl_to_file(self):
        self.crawl()
        
    def get_links(self,session,cname):
        item_url_xpath = "//div[@class='col-xs-6 col-sm-12 image-wrapper align-left']//a/@href"
        next_page_xpath = "//a[@class='pagination-item pagination-arrow ' and @title='Próxima']/@href"
        r = session.get(self.Clinks[cname])
        html = parser.fromstring(r.text)
        self.parse_links(html, item_url_xpath)
        try:
            next_page = html.xpath(next_page_xpath)[0]
        except IndexError as e:
            next_page = None
        while next_page:
            r = session.get(next_page)
            html = parser.fromstring(r.text)
            self.parse_links(html, item_url_xpath)
            try:
                next_page = html.xpath(next_page_xpath)[0]
            except IndexError as e:
                next_page = None

    def get_items(self,session):
        for link in self.links:
            r = session.get(link)
            try:
                html = parser.fromstring(r.text)
            except:
                print('Skipping invalid XML from URL {}' + link)
            print(str(r) + " : " + link)
            self.items.append(self.extract_item(html, link))
        
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
            CodRef = blank(html.xpath("//div[@class='badge product-code']")[0].text)
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

        Prod_List["JSON"] = self.JSON_CREATE(Prod_List)
        
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


spider = EcommerceSpider("https://www.leroymerlin.com.br/localizacao/store/?local=campinas")

spider.crawl_to_file()

spider.timewarn()
