from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import lxml.html as parser
import requests
import csv
from urllib.parse import urlsplit, urljoin

# Verificador anti-crawler baseado em regiao    : https://stackoverflow.com/questions/35252592/python-library-requests-open-the-wrong-page
# 403 FORBIDDEN                                 : https://stackoverflow.com/questions/38489386/python-requests-403-forbidden


class Product(object):
    def __init__(self):
        self.vtex = []
        self.items = []
        self.key = []
        self.start_url = "https://www.leroymerlin.com.br/"
        self.base_url = "https://www.leroymerlin.com.br/"
        self.prod = []
        self.order = {}
        self.cat = {}

    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    print("Duplicado")
                else:
                    self.key.append(check)

    def prepare_url(self, complement):
        url = self.base_url + complement
        return url

    def set_base_url(self):
        self.base_url = urlsplit(self.start_url)._replace(
            path="", query="").geturl()


def clear(texto):
    texto = texto.replace("\r", "").replace("\n", "").replace(
        "\t", "").replace("&nbsp;", "").replace("\xa0", "").strip(".").strip(" ")
    return texto


def blank(texto):
    teste = " ".join(texto.split())
    return teste


LINKS = ['https://lojasguapore.vtexcommercestable.com.br/banheiro', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/bacias', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/chuveiros-e-duchas', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/outros', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/caixas-acopladas', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/torneiras-e-misturadores', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/acabamentos-para-registro', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/bides', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/assentos-sanitarios', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/acessorios-para-banheiro', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/cubas-e-lavatorios', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/mictorios', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/caixas-de-descarga', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/registros', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/pressurizador', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/banheiras', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos/pisos-vinilicos', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos/pisos-laminados', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos/acessorios-para-pisos', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos/carpete-em-placa', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos/acabamentos-decorativos', 'https://lojasguapore.vtexcommercestable.com.br/cozinha', 'https://lojasguapore.vtexcommercestable.com.br/cozinha/torneiras-e-misturadores', 'https://lojasguapore.vtexcommercestable.com.br/cozinha/pias-e-cubas-para-cozinha', 'https://lojasguapore.vtexcommercestable.com.br/cozinha/acessorios-para-cozinha', 'https://lojasguapore.vtexcommercestable.com.br/cozinha/aquecedores', 'https://lojasguapore.vtexcommercestable.com.br/cozinha/purificadores', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/luminarias',
         'https://lojasguapore.vtexcommercestable.com.br/iluminacao/plafons', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/pendentes', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/arandelas', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/abajur', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lampadas', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/refletor', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/painel-led', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/cordao-luminoso', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/balizador', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/espeto-para-jardim', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/luminaria-de-teto', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-aramado', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-cimento', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-cristal', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-madeira', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-metal-aluminio', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-policarbonato', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-tecido', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-vidro', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/spot-de-sobrepor', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/spot-de-trilho', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/trilho', 'https://lojasguapore.vtexcommercestable.com.br/decoracao', 'https://lojasguapore.vtexcommercestable.com.br/decoracao/vasos-decorativos', 'https://lojasguapore.vtexcommercestable.com.br/decoracao/cortinas', 'https://lojasguapore.vtexcommercestable.com.br/decoracao/tapete', 'https://lojasguapore.vtexcommercestable.com.br/eletros', 'https://lojasguapore.vtexcommercestable.com.br/eletros/coifas-e-depuradores', 'https://lojasguapore.vtexcommercestable.com.br/eletros/cooktop', 'https://lojasguapore.vtexcommercestable.com.br/eletros/micro-ondas', 'https://lojasguapore.vtexcommercestable.com.br/eletros/forno-eletrico', 'https://lojasguapore.vtexcommercestable.com.br/eletros/fogao', 'https://lojasguapore.vtexcommercestable.com.br/eletros/processador-de-alimentos', 'https://lojasguapore.vtexcommercestable.com.br/eletros/panela-eletrica', 'https://lojasguapore.vtexcommercestable.com.br/eletros/liquidificador', 'https://lojasguapore.vtexcommercestable.com.br/eletros/batedeiras', 'https://lojasguapore.vtexcommercestable.com.br/eletros/ferro-de-passar', 'https://lojasguapore.vtexcommercestable.com.br/eletros/fritadeiras', 'https://lojasguapore.vtexcommercestable.com.br/eletros/climatizador', 'https://lojasguapore.vtexcommercestable.com.br/utilidades-domesticas', 'https://lojasguapore.vtexcommercestable.com.br/utilidades-domesticas/acessorios-para-lazer', 'https://lojasguapore.vtexcommercestable.com.br/utilidades-domesticas/caixa-termica', 'https://lojasguapore.vtexcommercestable.com.br/utilidades-domesticas', 'https://lojasguapore.vtexcommercestable.com.br/brinquedos', 'https://lojasguapore.vtexcommercestable.com.br/brinquedos/triciclo', 'https://lojasguapore.vtexcommercestable.com.br/brinquedos/drone', 'https://lojasguapore.vtexcommercestable.com.br/brinquedos/carrinho-eletrico', 'https://lojasguapore.vtexcommercestable.com.br/brinquedos/outros', 'https://lojasguapore.vtexcommercestable.com.br/materiais-de-construcao', 'https://lojasguapore.vtexcommercestable.com.br/materiais-de-construcao/ralos', 'https://lojasguapore.vtexcommercestable.com.br/materiais-de-construcao', 'https://lojasguapore.vtexcommercestable.com.br/area--externa', 'https://lojasguapore.vtexcommercestable.com.br/area--externa/moveis', 'https://lojasguapore.vtexcommercestable.com.br/area--externa/piscinas', 'https://lojasguapore.vtexcommercestable.com.br/area--externa/camping', 'https://lojasguapore.vtexcommercestable.com.br/area--externa/churrasqueira-e-assador', 'https://lojasguapore.vtexcommercestable.com.br/area--externa/lavadora-de-alta-pressao', 'https://lojasguapore.vtexcommercestable.com.br/portas-e-janelas', 'https://lojasguapore.vtexcommercestable.com.br/portas-e-janelas/acessorios', 'https://lojasguapore.vtexcommercestable.com.br/portas-e-janelas/janelas', 'https://lojasguapore.vtexcommercestable.com.br/portas-e-janelas/portas', 'https://lojasguapore.vtexcommercestable.com.br/ferramentas', 'https://lojasguapore.vtexcommercestable.com.br/ferramentas/ferramenta-eletrica', 'https://lojasguapore.vtexcommercestable.com.br/ferramentas/ferramenta-manual', 'https://lojasguapore.vtexcommercestable.com.br/ferramentas/ferramenta-pneumatica', 'https://lojasguapore.vtexcommercestable.com.br/ferramentas/construcao-civil', 'https://lojasguapore.vtexcommercestable.com.br/ferramentas/outros', 'https://lojasguapore.vtexcommercestable.com.br/banheiro', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/bacias', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/chuveiros-e-duchas', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/outros', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/caixas-acopladas', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/torneiras-e-misturadores', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/acabamentos-para-registro', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/bides', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/assentos-sanitarios', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/acessorios-para-banheiro', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/cubas-e-lavatorios', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/mictorios', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/caixas-de-descarga', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/registros', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/pressurizador', 'https://lojasguapore.vtexcommercestable.com.br/banheiro/banheiras', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos/pisos-vinilicos', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos/pisos-laminados', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos/acessorios-para-pisos', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos/carpete-em-placa', 'https://lojasguapore.vtexcommercestable.com.br/pisos-e-revestimentos/acabamentos-decorativos', 'https://lojasguapore.vtexcommercestable.com.br/cozinha', 'https://lojasguapore.vtexcommercestable.com.br/cozinha/torneiras-e-misturadores', 'https://lojasguapore.vtexcommercestable.com.br/cozinha/pias-e-cubas-para-cozinha', 'https://lojasguapore.vtexcommercestable.com.br/cozinha/acessorios-para-cozinha', 'https://lojasguapore.vtexcommercestable.com.br/cozinha/aquecedores', 'https://lojasguapore.vtexcommercestable.com.br/cozinha/purificadores', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/luminarias', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/plafons', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/pendentes', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/arandelas', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/abajur', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lampadas', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/refletor', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/painel-led', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/cordao-luminoso', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/balizador', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/espeto-para-jardim', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/luminaria-de-teto', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-aramado', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-cimento', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-cristal', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-madeira', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-metal-aluminio', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-policarbonato',
         'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-tecido', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/lustre-e-pendente-de-vidro', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/spot-de-sobrepor', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/spot-de-trilho', 'https://lojasguapore.vtexcommercestable.com.br/iluminacao/trilho', 'https://lojasguapore.vtexcommercestable.com.br/decoracao', 'https://lojasguapore.vtexcommercestable.com.br/decoracao/vasos-decorativos', 'https://lojasguapore.vtexcommercestable.com.br/decoracao/cortinas', 'https://lojasguapore.vtexcommercestable.com.br/decoracao/tapete', 'https://lojasguapore.vtexcommercestable.com.br/eletros', 'https://lojasguapore.vtexcommercestable.com.br/eletros/coifas-e-depuradores', 'https://lojasguapore.vtexcommercestable.com.br/eletros/cooktop', 'https://lojasguapore.vtexcommercestable.com.br/eletros/micro-ondas', 'https://lojasguapore.vtexcommercestable.com.br/eletros/forno-eletrico', 'https://lojasguapore.vtexcommercestable.com.br/eletros/fogao', 'https://lojasguapore.vtexcommercestable.com.br/eletros/processador-de-alimentos', 'https://lojasguapore.vtexcommercestable.com.br/eletros/panela-eletrica', 'https://lojasguapore.vtexcommercestable.com.br/eletros/liquidificador', 'https://lojasguapore.vtexcommercestable.com.br/eletros/batedeiras', 'https://lojasguapore.vtexcommercestable.com.br/eletros/ferro-de-passar', 'https://lojasguapore.vtexcommercestable.com.br/eletros/fritadeiras', 'https://lojasguapore.vtexcommercestable.com.br/eletros/climatizador', 'https://lojasguapore.vtexcommercestable.com.br/utilidades-domesticas', 'https://lojasguapore.vtexcommercestable.com.br/utilidades-domesticas/acessorios-para-lazer', 'https://lojasguapore.vtexcommercestable.com.br/utilidades-domesticas/caixa-termica', 'https://lojasguapore.vtexcommercestable.com.br/utilidades-domesticas', 'https://lojasguapore.vtexcommercestable.com.br/brinquedos', 'https://lojasguapore.vtexcommercestable.com.br/brinquedos/triciclo', 'https://lojasguapore.vtexcommercestable.com.br/brinquedos/drone', 'https://lojasguapore.vtexcommercestable.com.br/brinquedos/carrinho-eletrico', 'https://lojasguapore.vtexcommercestable.com.br/brinquedos/outros']
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

session = requests.Session()

r = session.get(
    "https://lojasguapore.vtexcommercestable.com.br/")
html = parser.fromstring(r.text)
links = html.xpath("//div[@class='menu-departamento']")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument("user-agent=Googlebot-Image")

driver = webdriver.Chrome(
    'C:\Temp\Projetos\Python\ChromeDriver\chromedriver.exe', chrome_options=chrome_options)
driver.get("https://lojasguapore.vtexcommercestable.com.br/")
time.sleep(25)
P = Product()

for link in LINKS:
    cont = 1
    next_cont = 1
    print(link)
    driver.get(link)

    while next_cont <= 2:
        Nomes = driver.find_elements_by_xpath(
            "//div[@class='product-title']/a")
        for x in Nomes:
            P.prod.append(x.text)
            P.cat[x.text] = link
            P.order[x.text] = cont
            cont += 1

        next_page = driver.find_element_by_css_selector(
            "div.pager.bottom li.next")
        driver.execute_script(
            "document.querySelector('div.pager.bottom li.next').click();")
        next_cont += 1
        time.sleep(5)


for x in P.prod:
    bleh = dict(Produto=x, Categoria=P.cat[x], Posição=P.order[x])
    P.items.append(bleh)

with open("SCORE.csv", 'w') as f:
    dict_writer = csv.DictWriter(
        f, fieldnames=bleh.keys(), delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(P.items)
print(P.cat)
print(P.order)
