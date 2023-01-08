import lxml.html as parser
import requests
import csv
import time
import re
import unidecode
from urllib.parse import urlsplit, urljoin
import http.client

http.client._MAXHEADERS = 1000


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


brands = ["bLACK dECKER"]

START_ULR = "https://www.tigre.com.br/produtos"
FILENAME = "Tigre.csv"


def blank(texto):
    if(texto != None):
        Noblank = " ".join(texto.split())
        return Noblank

def formatar(texto):
    texto = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]',
                   '', texto)
    texto = texto.replace("\n", "").replace("\xa0","")
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
        self.links = set()
        self.items = []
        self.start_url = start_url
        self.set_base_url()
        self.key = []
        self.errors = 0
        self.start_time = time.time()
        self.testerror = []
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None
        self.CatLinks = ['https://www.tigre.com.br/metais-para-banheiro/acessorios-para-banheiro' , 'https://www.tigre.com.br/registros/registros-de-gaveta' , 'https://www.tigre.com.br/complementos/engates-flexiveis' , 'https://www.tigre.com.br/obras-e-reformas/tanques-lavatorios/sifao' , 'https://www.tigre.com.br/claris/portas' , 'https://www.tigre.com.br/complementos/adaptadores' , 'https://www.tigre.com.br/industrial/tubos-e-conexoes-para-agua/tubos-pead-tubulacao-de-recalque' , 'https://www.tigre.com.br/esgoto/serie-reforcada' , 'https://www.tigre.com.br/complementos/ligacao-vaso-sanitario' , 'https://www.tigre.com.br/esgoto/complementos-hidraulicos/sifoes-ajustaveis' , 'https://www.tigre.com.br/tigre-metais/metais-para-banheiro/base-misturador' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/kits/multiuso' , 'https://www.tigre.com.br/ferramentas-para-pintura/pinceis-artisticos-e-escolares/kits' , 'https://www.tigre.com.br/esgoto/complementos-hidraulicos/tubos-de-descarga' , 'https://www.tigre.com.br/obras-e-reformas/torneiras/torneiras-para-banheiro' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/escovas/escovas' , 'https://www.tigre.com.br/ferramentas-para-pintura/artistica/pinceis-artisticos-escolares/auto-servico' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/abrasivos/paredes' , 'https://www.tigre.com.br/agua-fria/pbs-soldaveis-grandes-diametros' , 'https://www.tigre.com.br/industrial/agua/rede-distribuicao' , 'https://www.tigre.com.br/complementos/sifao','https://www.tigre.com.br/metais-para-cozinha/torneira-monobloco' , 'https://www.tigre.com.br/valvulas-de-succao' , 'https://www.tigre.com.br/metais-para-banheiro/ducha-para-box' , 'https://www.tigre.com.br/infraestrutura/ligacao-predial/conexoes-compressao' , 'https://www.tigre.com.br/drenagem/caixas-de-inspecao' , 'https://www.tigre.com.br/eletrodutos-caixas-luz/caixas-de-luz-alvenaria' , 'https://www.tigre.com.br/obras-e-reformas/agua/ducha-agua-fria' , 'https://www.tigre.com.br/industrial/processos/valvulas-industriais' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/trinchas/metais' , 'https://www.tigre.com.br/ferramentas-para-pintura/pinceis-artisticos-e-escolares/linha-sintetico-dourado-brilhante' , 'https://www.tigre.com.br/esgoto/complementos-hidraulicos/sifoes' , 'https://www.tigre.com.br/agua-fria/colas-pvc' , 'https://www.tigre.com.br/claris/quadro-fixo' , 'https://www.tigre.com.br/agua-fria/tubos-conexoes-roscaveis' , 'https://www.tigre.com.br/ligacao-predial/registros' , 'https://www.tigre.com.br/industrial/agua/cpvc-sch-80' , 'https://www.tigre.com.br/infraestrutura/drenagem/tigre-ads' , 'https://www.tigre.com.br/irrigacao/sistemas-fixos/registros-irrigacao' , 'https://www.tigre.com.br/obras-e-reformas/assentos-sanitarios' , 'https://www.tigre.com.br/metais-basicos' , 'https://www.tigre.com.br/obras-e-reformas/torneiras/torneiras-para-area-de-servicos' , 'https://www.tigre.com.br/agua-quente/ppr-termofusao' , 'https://www.tigre.com.br/industrial/solda/adesivo-primer' , 'https://www.tigre.com.br/infraestrutura/agua/tubo-pead' , 'https://www.tigre.com.br/obras-e-reformas/sistemas-de-descarga/ligacao-vaso-sanitario','https://www.tigre.com.br/obras-e-reformas/tubos-e-conexoes-para-agua-fria/tubo-soldavel-para-alta-pressao-prumadas-cpvc-pn-12' , 'https://www.tigre.com.br/irrigacao/drenagem/tubos-para-drenagem' , 'https://www.tigre.com.br/infraestrutura/esgoto/coletor-corrugado' , 'https://www.tigre.com.br/esgoto/caixas-sifonadas' , 'https://www.tigre.com.br/ferramentas-para-pintura/artistica/pinceis-artisticos/cerda-gris' , 'https://www.tigre.com.br/infraestrutura/agua/conexoes-pead-compressao' , 'https://www.tigre.com.br/drenagem/calhas-de-piso' , 'https://www.tigre.com.br/eletrodutos-caixas-luz/condulete-top' , 'https://www.tigre.com.br/agua-quente/sistema-flexivel-pex' , 'https://www.tigre.com.br/ferramentas-para-pintura/linha-artistica/acessorios' , 'https://www.tigre.com.br/infraestrutura/esgoto/conexoes-coletora' , 'https://www.tigre.com.br/obras-e-reformas/areas-externas/ducha-agua-fria' , 'https://www.tigre.com.br/esgoto/ralo-linear' , 'https://www.tigre.com.br/esgoto/aneis-pasta-lubrificante' , 'https://www.tigre.com.br/area-de-servico/torneiras' , 'https://www.tigre.com.br/ferramentas-para-pintura/pinceis-artisticos-e-escolares/linha-marta-tropical' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/trinchas/paredes' , 'https://www.tigre.com.br/obras-e-reformas/tanques-lavatorios/bacias' , 'https://www.tigre.com.br/isolamento/fita-isolante' , 'https://www.tigre.com.br/irrigacao/sistemas-fixos/colas-pvc' , 'https://www.tigre.com.br/metais-para-banheiro/torneiras-para-banheiro' , 'https://www.tigre.com.br/irrigacao/sistemas-portateis/engate-sela' , 'https://www.tigre.com.br/quadros-caixas/caixa-de-passagem-eletrica' , 'https://www.tigre.com.br/tubos-conexoes-gas/tigregas' , 'https://www.tigre.com.br/metais-para-banheiro/chuveiros' , 'https://www.tigre.com.br/ferramentas-para-pintura/pinceis-artisticos-e-escolares/linha-sintetico-dourado-acetinado' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/abrasivos/metais' , 'https://www.tigre.com.br/reservatorios-agua/torneira-boia' , 'https://www.tigre.com.br/ferramentas-para-pintura/pinceis-artisticos-e-escolares/linha-escolar-ponei' , 'https://www.tigre.com.br/complementos/tubos-de-descarga' , 'https://www.tigre.com.br/eletrodutos-caixas-luz/caixas-de-luz-drywall' , 'https://www.tigre.com.br/infraestrutura/ligacao-predial/registros' , 'https://www.tigre.com.br/claris/janelas' , 'https://www.tigre.com.br/metais-para-cozinha/torneira-monocomando' , 'https://www.tigre.com.br/claris/janela-porta' , 'https://www.tigre.com.br/agua-fria/sistema-flexivel-pex' , 'https://www.tigre.com.br/registros/registros-de-esfera' , 'https://www.tigre.com.br/ferramentas-para-pintura/pinceis-artisticos-e-escolares/linha-orelha-de-boi' , 'https://www.tigre.com.br/ligacao-predial/hidrometro' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/trinchas/madeiras' , 'https://www.tigre.com.br/ferramentas-para-pintura/artistica/pinceis-artisticos-escolares/trinchas' , 'https://www.tigre.com.br/metais-para-banheiro/acabamento-para-banheiro' , 'https://www.tigre.com.br/obras-e-reformas/tanques-lavatorios/lavatorios' , 'https://www.tigre.com.br/drenagem/caixas-de-areia' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/rolos/multiuso' , 'https://www.tigre.com.br/ferramentas-para-pintura/pinceis-artisticos-e-escolares/linha-ponei' , 'https://www.tigre.com.br/ferramentas-para-pintura/pinceis-artisticos-e-escolares/linha-sintetico-mesclado' , 'https://www.tigre.com.br/obras-e-reformas/sistemas-de-descarga/tubos-de-descarga' , 'https://www.tigre.com.br/irrigacao/sistemas-portateis/engate-plastico' , 'https://www.tigre.com.br/metais-para-banheiro/ducha-higienica' , 'https://www.tigre.com.br/metais-para-banheiro/torneira-com-misturador' , 'https://www.tigre.com.br/industrial/processos/conducao-fluidos-cpvc-sch-80' , 'https://www.tigre.com.br/metais-para-cozinha/torneiras-para-cozinha' , 'https://www.tigre.com.br/quadros-caixas/quadros-distribuicao' , 'https://www.tigre.com.br/reservatorios-agua/caixas-dagua' , 'https://www.tigre.com.br/industrial/processos/pvcu-industrial-sch-80' , 'https://www.tigre.com.br/metais-para-banheiro/base-para-banheiro' , 'https://www.tigre.com.br/esgoto/caixas-de-inspecao' , 'https://www.tigre.com.br/infraestrutura/drenagem/drenoflex' , 'https://www.tigre.com.br/infraestrutura/gas/tubulacao-pead' , 'https://www.tigre.com.br/infraestrutura/ligacao-predial/tubo' , 'https://www.tigre.com.br/reservatorios-agua/registros-adaptadores' , 'https://www.tigre.com.br/metais-para-banheiro/torneira-monocomando' , 'https://www.tigre.com.br/metais-para-banheiro/valvula-de-descarga' , 'https://www.tigre.com.br/industrial/tubos-conexoes-ventilacao-linha-leve' , 'https://www.tigre.com.br/esgoto/conexoes-drywall' , 'https://www.tigre.com.br/agua-quente/aquatherm' , 'https://www.tigre.com.br/quadros-caixas/quadros-vdi' , 'https://www.tigre.com.br/industrial/agua/valvulas-industriais' , 'https://www.tigre.com.br/infraestrutura/ligacao-predial/hidrometro' , 'https://www.tigre.com.br/obras-e-reformas/tanques-lavatorios/tanques' , 'https://www.tigre.com.br/ferramentas-para-pintura/pinceis-artisticos-e-escolares/linha-marta' , 'https://www.tigre.com.br/metais-para-banheiro/regulador-de-vazao' , 'https://www.tigre.com.br/esgoto/grelhas-para-ralos' , 'https://www.tigre.com.br/obras-e-reformas/tubos-e-conexoes-para-agua-fria/conexoes-para-drywall-conexoes-para-gesso' , 'https://www.tigre.com.br/esgoto/serie-normal' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/rolos/decorativos' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/kits/paredes' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/acessorios/decorativos' , 'https://www.tigre.com.br/irrigacao/agropecuaria/tubos-pvc' , 'https://www.tigre.com.br/obras-e-reformas/torneiras/torneiras-para-cozinha' , 'https://www.tigre.com.br/industrial/ar-comprimido/ppr-industrial' , 'https://www.tigre.com.br/irrigacao/sistemas-fixos/irriga-lf-defofo' , 'https://www.tigre.com.br/complementos/valvulas' , 'https://www.tigre.com.br/industrial/solda/vareta' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/rolos/madeiras' , 'https://www.tigre.com.br/ligacao-predial/conexoes-derivacao' , 'https://www.tigre.com.br/valvulas-de-retencao' , 'https://www.tigre.com.br/ferramentas-para-pintura/artistica/pinceis-artisticos/cerda-sintetica-bege' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/abrasivos/madeiras' , 'https://www.tigre.com.br/industrial/agua/pbs-soldaveis-grandes-diametros' , 'https://www.tigre.com.br/metais-para-banheiro/sifao-para-banheiro' , 'https://www.tigre.com.br/agua-quente/colas-pvc' , 'https://www.tigre.com.br/infraestrutura/esgoto/coletor-liso' , 'https://www.tigre.com.br/infraestrutura/agua/rede-adutora' , 'https://www.tigre.com.br/metais-para-cozinha/torneira-com-misturador' , 'https://www.tigre.com.br/esgoto/complementos-hidraulicos/ligacao-vaso-sanitario' , 'https://www.tigre.com.br/esgoto/colas-pvc' , 'https://www.tigre.com.br/irrigacao/aspersores/aspersores-de-impacto' , 'https://www.tigre.com.br/obras-e-reformas/torneiras/reparo-para-torneiras' , 'https://www.tigre.com.br/ligacao-predial/tubo-de-ligacao' , 'https://www.tigre.com.br/industrial/adesivos-primer' , 'https://www.tigre.com.br/metais-para-banheiro/registros-e-valvulas' , 'https://www.tigre.com.br/metais-economizadores/chuveiros-economizadores' , 'https://www.tigre.com.br/claris/guarda-corpo' , 'https://www.tigre.com.br/tubos-conexoes-ventilacao/linha-leve' , 'https://www.tigre.com.br/tubulacao-de-incendio/tigre-fire' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/trinchas/multiuso' , 'https://www.tigre.com.br/metais-economizadores/torneiras-economizadoras' , 'https://www.tigre.com.br/irrigacao/sistemas-portateis/registros' , 'https://www.tigre.com.br/complementos/valvulas-de-escoamento' , 'https://www.tigre.com.br/eletrodutos-caixas-luz/soldavel' , 'https://www.tigre.com.br/infraestrutura/agua/rede-distribuicao' , 'https://www.tigre.com.br/ferramentas-para-pintura/linha-imobiliaria/decorativos' , 'https://www.tigre.com.br/obras-e-reformas/tanques-lavatorios/valvulas-escoamento' , 'https://www.tigre.com.br/obras-e-reformas/sistemas-de-descarga/caixa-de-descarga' , 'https://www.tigre.com.br/ligacao-predial/conexoes-compressao' , 'https://www.tigre.com.br/claris/portas-pivotantes' , 'https://www.tigre.com.br/ferramentas-para-pintura/artistica/pinceis-artisticos/cerda-alvejada' , 'https://www.tigre.com.br/infraestrutura/ligacao-predial/conexoes-derivacao' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/acessorios/acessorios' , 'https://www.tigre.com.br/irrigacao/pocos-artesianos/pocos-geotigre' , 'https://www.tigre.com.br/ferramentas-para-pintura/artistica/pinceis-artisticos/cerda-natural' , 'https://www.tigre.com.br/irrigacao/agropecuaria/registros' , 'https://www.tigre.com.br/area-de-servico/sifao' , 'https://www.tigre.com.br/drenagem/tubos-para-drenagem' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/abrasivos/multiuso' , 'https://www.tigre.com.br/eletrodutos-caixas-luz/roscavel' , 'https://www.tigre.com.br/eletrodutos-caixas-luz/corrugado-tigreflex' , 'https://www.tigre.com.br/infraestrutura/pocos-artesianos-pocos-geotigre' , 'https://www.tigre.com.br/metais-economizadores/valvulas' , 'https://www.tigre.com.br/esgoto/caixas-de-gordura' , 'https://www.tigre.com.br/obras-e-reformas/tubos-e-conexoes-para-esgoto/tigre-redux' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/rolos/paredes' , 'https://www.tigre.com.br/complementos/grelhas-para-ralos' , 'https://www.tigre.com.br/agua-fria/tubos-conexoes-soldaveis' , 'https://www.tigre.com.br/registros/registros-de-chuveiro' , 'https://www.tigre.com.br/irrigacao/sistemas-fixos/irriga-lf' , 'https://www.tigre.com.br/ferramentas-para-pintura/imobiliaria/rolos/metais' , 'https://www.tigre.com.br/agua-quente/conexoes-drywall' , 'https://www.tigre.com.br/drenagem/calhas-para-telhado-aquapluv-style' , 'https://www.tigre.com.br/drenagem/calhas-para-telhado-aquapluv']

    def timewarn(self):
        self.end_time = time.strftime("%b.%d-%X")
        print("Start : "+self.start_time + " End : "+self.end_time)

    def crawl(self):
        session = requests.Session()
        self.get_links(session)
        self.get_items(session)

    def crawl_to_file(self, filename):
        self.crawl()
        self.save_items(filename)

    def get_links(self,session):
        print("GET LINKS")
        item_url_xpath = "//div[@class='list-products products-category products-grid']/div/a/@href"
        for link in self.CatLinks:  
            print(link)
            
            r = session.get(link)
            r.encoding = 'utf-8'
            html = parser.fromstring(r.text)
            self.parse_links(html, item_url_xpath)

    def get_items(self,session):
        print("GET_ITEM")
        with open("CORRIGIR.csv", 'w', encoding="utf-8") as f:
            dict_writer = csv.writer(f, delimiter=';')
            dict_writer.writerows(self.testerror)

        for link in self.links:
            r = session.get(link)
            r.encoding = 'utf-8'
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

    def extract_item(self, html, link):
        EspList = {}
        try:
            name = html.xpath(
                "//h1[@class='title']")[0]
            name = blank(name.text)
        except IndexError as e:
        # print("name not found at page %s" % link)
            name = "Not found"

        try:
            CodRef = html.xpath("//p[@class='desc-sku']/small")[0].text
        except IndexError as e:
            CodRef = "Not Found"

        try:
            Desc = html.xpath("//h2[@class='tag-description']")[0].text
        except IndexError as e:
            Desc = "Not Found"

        try:
            Categorias = html.xpath(
                "//ol[@class='breadcrumb']//span[@itemprop='name']")
            fullCat = ""
            for cat in Categorias:
                fullCat += cat.text + " > "
            fullCat = fullCat.strip(" > ")
        except IndexError as e:
            Categorias = "Not Found"

        EspList = dict(Nome=name, CodRef=CodRef, Descrição=Desc, Categoria=fullCat)

        try:
            Attr = html.xpath(
                "//ul[@class='list-unstyled list-inline list-product-icons']/li")
            for atribute in Attr:
                EspList[formatar(atribute[1].text)] = atribute[2].text.replace("•","")
        except IndexError as e:
            Attr = "Not Found"

        try:
            Attr2 = html.xpath(
                "//div[@class='tab-content']//div[contains(@class,'col-xs-12')]//text()")
            cont = 1
            atual = ""
            iha = 0
            tipo = 0
            for x in Attr2:
                if "mso-data-placement" in x:
                    None
                elif ":" in x:
                    a, b = x.split(":",1)
                    if len(b) > 0:
                        tipo = 1
                if tipo == 1:
                    if '\n\n' in x:
                        None
                    elif ":" in x:
                        a, b = x.split(':', 1)
                        EspList[formatar(a)] = b.replace("\n", "").strip(" ").replace("•","")
                    else:
                        EspList["Atributo " +
                                str(cont)] = x.replace("\n", "").strip(" ").strip("- ").replace("•","")
                        cont += 1
                else:
                    if not "\n" in x:
                        if "mso-data-placement" in x:
                            None
                        elif ":" in x:
                            atual = x
                        elif 'BENEFÍCIOS' in x:
                            None
                        elif 'INSTRUÇÕES' in x:
                            iha = "INSTRUÇÕES"
                        elif iha == "INSTRUÇÕES":
                            EspList[formatar(iha)] = x.strip(" ").replace("•","")
                            iha = ""
                        elif atual == "":
                            EspList["Atributo "+str(cont)] = x.strip(" ").strip("- ").replace("•","")
                            cont += 1
                        else:
                            EspList[formatar(atual.strip(":"))] = x.strip(" ").replace("•","")
                            atual = ""

        except IndexError as e:
            Attr2 = "Not Found"

        try:
            Infos = html.xpath(
                "//div[@class='field field--name-field-texto-tecnico field--type-text-long field--label-hidden field--item']//text()")
            for info in Infos:
                if not "\n" in info:
                    if "-" in info.strip("\xa0").strip(" ").strip("-").strip(" "):
                        x, y = info.replace("\xa0", "").replace(
                            ";", "").strip("- ").rsplit("-", 1)
                        EspList[formatar(x)] = y.replace("•","")
                    else:
                        EspList["Attributo " + str(cont)] = info.strip("- ").replace("•","")
                        cont += 1

        except IndexError as e:
            Infos = "Not Found"


        try:
            drawcont = 1
            DesenhoTec = html.xpath(
                "//div[@class='field field--name-field-desenho-tecnico field--type-image field--label-hidden field--item']/img/@src")
            for url in DesenhoTec:
                teste = url.split("?")[0]
                fullurl = self.prepare_url(url)
                EspList["Desenho Técnico "+str(drawcont)] = fullurl
                drawcont += 1
        except IndexError as e:
            DesenhoTec = "Not Found"


        try:
            Img = html.xpath("//div[@id='carousel-dp']//img/@src")
            imgcont = 1
            for img in Img:
                EspList["Imagem " + str(imgcont)] = img
        except IndexError as e:
            Img = "Not Found"

        try:
            ficha = html.xpath("//a[@class='lk-download']/@href")[0]
            ficha = self.prepare_url(ficha)
            EspList["Ficha Técnica"] = ficha
        except IndexError as e:
            ficha = "Not Found"
        return EspList

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
        print(self.key)
        org = Organizer(self.key)
        fieldnames = org.Alinha()
        with open(filename, 'w',encoding="utf-8") as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


print("LETS GET IT STARTED")

spider = EcommerceSpider(START_ULR)

spider.crawl_to_file(FILENAME)

spider.timewarn()
