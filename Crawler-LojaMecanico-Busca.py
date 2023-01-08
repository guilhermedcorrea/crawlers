import lxml.html as parser
import requests
import csv
import time
import re
import unidecode
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


def noblank(texto):
    if(texto != None):
        Noblank = " ".join(texto.split())
        return Noblank


def formatar(texto):
    texto = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ: ]',
                   '', texto)
    texto = texto.strip(" ")
    texto = texto.strip(":: ")
    texto = texto.capitalize()
    unaccented_string = unidecode.unidecode(texto)
    return unaccented_string


class Organizer(object):
    def __init__(self, key):
        self.filename = "Bel lazer-Madeira.csv"
        self.Cods = ['Código', 'Codigo', 'Codigo do fornecedor', 'Codigo do fornecerdor', 'Gerais - Referência', ' • Referência',
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
        self.Clinks = {
            'Wap': 'https://busca.lojadomecanico.com.br/busca?q=wap'}
        self.Cats = ['Wap']
        # Alarmes/ Travas', 'Calhas de chuva', 'Cinto de Segurança', 'Farol', 'Filtro de Ar Condicionado', 'GPS', 'Grade de Para-choque', 'Insulfilm', 'Macaco', 'Maçanetas', 'Palheta', 'Pneus e Câmaras', 'Protetor Solar', 'Sensor de Estacionamento', 'Som e Video Automotivo', 'Tapetes', 'Universal', 'Volante',  'Aditivos P/ Carburador', 'Aditivos P/ Combustível', 'Aditivos p/ Limpeza de Bicos', 'Aditivos P/ Motores', 'Aromatizante e Outros', 'Colas e Vedadores', 'Limpeza Automotiva', 'Limpeza e Removedores', 'Lubrificação', 'Produtos P/ Radiador', 'Tintas Spray',  'Acessórios p/ Auto Elétrica', 'Alicates Amperímetro', 'Alinhador de Farol', 'Analisadores', 'Auxiliar de Partida', 'Bancada de Teste', 'Carregadores até 12V', 'Carregadores até 24V', 'Ferramentas Especiais P/Auto Elétrica', 'Ferro de Solda', 'Fusíveis', 'Passador de Fios', 'Protetor para Bateria', 'Protoboard', 'Retirar Bomba Elétrica', 'Teste de Bateria',  'Desforcímetro', 'Equipamentos Borracharia', 'Ferramentas Borracharia', 'Reparo Para Pneus',  'Acessórios', 'Amassadores de Latas', 'Barracas', 'Bolsa Térmica', 'Churrasqueira', 'Colchões', 'Cutelaria', 'Esporte e Lazer', 'Guarda-Sol', 'Lanternas e Refletores', 'Mergulho', 'Mesas e Cadeiras', 'Mini Geladeira', 'Motor de Popa e Rabetas', 'Pescaria', 'Piscinas', 'Sacos de Dormir', 'Alisadora de Concreto', 'Andaimes', 'Argamasseira', 'Baldes', 'Betoneiras', 'Bombas de Teste', 'Carrinho de Mão', 'Colheres de Pedreiros', 'Compactadores', 'Corta Vergalhão', 'Cortador De Piso e Azulejo', 'Desempenadeiras', 'Desentupidores', 'Dobrador de Ferro', 'Escadas', 'Escala Métrica', 'Espátulas', 'Esquadros', 'Estiletes', 'Ferramentas Manuais p/ Construção Civil', 'Fixação a Pólvora', 'Formão', 'Guinchos', 'Jogo de Brocas', 'Lixadeira de Parede / Teto', 'Materiais Para Marcação', 'Mexedores e Trituradores', 'Multidetector', 'Níveis, Prumos e Linha', 'Pincéis e Rolos', 'Pintura Airless', 'Plainas', 'Ponteiros', 'Régua Vibratória', 'Roldanas', 'Serrotes', 'Talha Elétrica', 'Talha Manual', 'Talhadeira e Saca Pino', 'Tela para Construção', 'Termofusora', 'Torqueses', 'Trenas', 'Trole Manual', 'Vedadores e Espuma Expansiva', 'Vibradores P/ Concreto',  'Acessórios', 'Assento de Suspensão', 'Aventais', 'Bota PVC', 'Botinas', 'Calçado de Segurança Esportivo', 'Capacete de Segurança', 'Capas de Chuva', 'Cinta Ergonômica', 'Colete Refletor', 'Joelheira de Proteção', 'Luvas', 'Máscara de Proteção', 'Óculos Proteção', 'Proteção para Corpo', 'Protetor Auricular', 'Protetor Solar, Cremes de Proteção e Higienização', 'Sinalização', 'Trabalho em Altura',  'Acessórios Para Oficina', 'Alinhamento e Balanceamento', 'Ar Condicionado', 'Banqueta', 'Calibrador de pneus', 'calibrador de pneus manual', 'Desmontadora de  Pneus', 'Elevadores e Rampas', 'Equipamento Hidráulico', 'Lavadora de Peças', 'Lubrificação', 'Morsas e Tornos', 'Móveis Para Oficina', 'Rebitadeira Freios', 'Secadores de Ar', 'Torno Mecânico',  'Controle Torque L. Pesada', 'Equipamento p/ Caminhões', 'Equipamentos P/ Posto de Molas', 'Macaco Câmbio L. Pesada', 'Mercedes Bens Câmbio', 'Mercedes Bens Direção', 'Mercedes Bens Eixo Diant.', 'Mercedes Bens Eixo Tras.', 'Mercedes Bens Motor', 'Motores Maxion Cummins', 'Motores MWM', 'Saca Filtro Linha Pesada', 'Scania Câmbio', 'Scania Motor', 'Scania Suspensão', 'Scanners Linha Pesada', 'Suporte Motor Caminhões', 'Todos P/ VW Ford Iveco', 'Volvo Motor e Câmbio', 'Volvo Suspensão e Freios',  'Cronômetro',  'Alicates Especiais', 'Anéis de Vedação Oring', 'Brunidores', 'Cavalete de Apoio', 'Chave de Vela', 'Chave Soquete Tipo T', 'Cinta Compressora Anéis', 'Encolhedor Mola', 'Extrator de Parafuso', 'Flangeador e Cortador P/ Tubo', 'Freio e Homocinética', 'Kit Correia Dentada', 'Linha Chevrolet', 'Linha Fiat', 'Linha Ford', 'Linha Peugeot', 'Linha Renault', 'Linha Volkswagen', 'Outros Importados', 'Saca Filtro LinhaLeve', 'Saca Polia', 'Saca Rolamento', 'Suporte Motor Câmbio Leve', 'Terminal de Direção', 'Toda Linha- Direção', 'Torquímetro Transferidor', 'Uso Universal Especial', 'Afiador', 'Chave de Impacto', 'Compressores', 'Esmerilhadeira', 'Fresadora/ Frisadeira', 'Furadeira', 'Grampeador/Pinador Elétrico', 'Linha Bateria', 'Lixadeira e Politriz', 'Máquina de Solda', 'Máquinas de Solda Acessórios', 'Máquinas Industriais', 'Marteletes Elétricos', 'Moto Esmeril', 'Motor Elétrico', 'Parafusadeiras Elétricas', 'Retificadeiras Elétricas', 'Rosqueadeiras', 'Serra Elétrica', 'Soprador Térmico', 'Tupias e Plainas', 'Utilidades P/ Máquinas Elétricas',  'Abraçadeiras', 'Abrasivos', 'Aplicadores', 'Balanças','Brocas', 'Discos Serra Circular', 'Discos Serra Mármore', 'Escovas de Aço', 'Fechaduras e Cadeados', 'Fitas Adesivas', 'Grampeador Manual', 'Lâminas Serra Sabre', 'Lâminas Serra Tico-Tico', 'Limpador Ultrassônico', 'Mandril e Chaves', 'Marcadores', 'Parafusos Buchas Gancho Prego', 'Prisma e Capa Protetora', 'Raspador Manual', 'Serra Copo', 'Vira Macho',  'Adaptadores p/ Soquetes', 'Alavancas', 'Alicates', 'Arco de Pua', 'Arco de Serra', 'Bate Prego', 'Bits (Avulso)', 'Cabeça Intercambiável', 'Cabo de Força P/ Soquetes', 'Caixa de Ferramentas', 'Calandra/Guilhotina', 'Catraca Reversível  P/ Soquetes', 'Chave Allen (Avulsa)', 'Chave Allen (Jogo)', 'Chave Biela (L)', 'Chave Canhão', 'Chave Combinada(Avulsa)', 'Chave Combinada (Jogo)', 'Chave Combinada Catraca (Avulsa)', 'Chave Combinada Catraca (Jogo)', 'Chave de Boca (Avulsa)', 'Chave de Boca (Jogo)', 'Chave de Fenda e Philips', 'Chave de Impacto Manual', 'Chave de Precisão', 'Chave de Roda', 'Chave Especial', 'Chave Estrela (Avulsa)', 'Chave Estrela (Jogo)', 'Chave Estrela Catraca (avulsa)', 'Chave Estrela Catraca (Jogo)', 'Chave Extensível', 'Chave Grifo (Cano)', 'Chave Inglesa', 'Chave Multidentada', 'Chave Tork Tipo L', 'Cortadores de Vidro', 'Escariadores e Vazadores', 'Extensão P/ Soquete', 'Ferramentas Isoladas', 'Ferramentas Magnéticas', 'Grampos', 'Jogo de Tork e Ribe', 'Juntas Universal p/ Soquetes', 'Kit de Ferramentas', 'Kit de Pontas (Bits)', 'Lupas', 'Maleta de Ferramentas e Bolsas', 'Manivela para Soquetes', 'Marretas', 'Martelos', 'Pé de Cabra', 'Punções', 'Rebitador Manual', 'Soquete de Impacto (Jogo)','Soquete Tipo Fenda', 'Soquete Tipo Hexagonal', 'Soquete Tipo Multidentada', 'Soquete Tipo Phillips', 'Soquete Tipo Tork', 'Soquetes (Jogos)', 'Soquetes 1 pol. (Avulso)', 'Soquetes 1/4 (Avulso)', 'Soquetes 3/8 (Avulso)', 'Soquetes de 1.1/2 (Avulsa)', 'Soquetes de 1/2 (Avulsa)', 'Soquetes de 3/4 (Avulsa)', 'Tarraxa Manual', 'Tork com Cabo',  'Alinhadores  de Rodas', 'Cavaletes e Suportes', 'Compressores de Mola', 'Desmontadora de Pneus', 'Ferramentas Especiais', 'Injeção Eletrônica', 'Lubrificação', 'Medidores Para Motos', 'Rampa Para Motos', 'Scanners Linha Moto',  'Acessórios Pneumáticos', 'Bases Antideslizantes e Nivelador', 'Bicos de Ar', 'Bombas de Encher', 'Calafetadores', 'Caneta Gravação', 'Chave de Catraca', 'Chave Impacto', 'Desincrustador', 'Despontadeira', 'Esmerilhadeiras', 'Facas Oscilantes', 'Filtro Regulador', 'Furadeira Pneumática', 'Grampeadores', 'Kit Para Compressor', 'Lixadeiras', 'Mangueiras de Ar', 'Marteletes', 'Parafusadeiras', 'Pinadores', 'Politriz', 'Pulverizadores', 'Raspador', 'Rebitadores', 'Retíficas', 'Serras Pneumáticas', 'Tesoura Punção', 'Tornador',  'Alicate Para Solda', 'Alinhador de Monobloco', 'Eletrodo e Arames', 'Equipamentos Funilaria Pintura', 'Ferramentas Especiais', 'Ferramentas Funilaria', 'Martelinho de Ouro', 'Painel de Secagem', 'Pistola Para Pintura', 'Repuxador / Spotter', 'Soldador de Para-choque', 'Suporte Preparação', 'Tasso Funilaria', 'Ventosa',  'Acessórios Diversos', 'Análise de Gases', 'Arrefecimento e Outros', 'Caixa Bi-combustível', 'Caneta de Polaridade', 'Cartões de Liberação', 'Instrumentos P/ Medidas', 'Lâmpada de Ponto', 'Limpeza de Bicos', 'Megômetro', 'Multímetros', 'Osciloscópio Endoscopia', 'Outros Para Injeção', 'Outros Para Motor', 'Sangrador de Freios', 'Scanners Linha Leve', 'Termômetros', 'Teste de Bomba Elétrica', 'Teste de Combustível', 'Teste de Compressão',  'Aparadores de Cerca Viva', 'Aparadores de Grama', 'Aspirador Soprador Folhas', 'Bomba de Água', 'Cortadores de Grama', 'Ferramentas para Jardim', 'Geradores de Energia', 'Irrigação', 'Mangueira Água Acéssorios', 'Mini Trator P/ Cortar Grama', 'Moedores de Cana', 'Motocultivador', 'Motores Estacionários à Combustão', 'Motosserras', 'Perfuradores de Solo', 'Pulverizadores', 'Roçadeira', 'Trituradores e Picadores', 'Utilidades Para Jardinagem',  'Aspirador de Pó', 'Funil', 'Lavadora de Alta Pressão', 'Limpadora a Vapor', 'Posto de Gasolina', 'Transferidor de Líquidos', 'Varredeiras', 'Cursos em Vídeos',  'Adaptadores de Tomada', 'Extensão Elétrica/ Filtros', 'Inversores de Potência', 'Tomadas e Interruptores', 'Transformadores', 'Tubos e Eletrodutos',  'Acessórios de Carga', 'Carrinhos de Carga', 'Empilhadeira Elétrica', 'Empilhadeira Manual Hidráulica', 'Fita Elevação de Carga', 'Reboque', 'Roda e Rodízio', 'Tartarugas Para Movimentação', 'Transpaletes',  'Acessórios para Casa', 'Aquecedor de Água', 'Aquecedores', 'Ar Condicionado', 'Armadilhas Elétricas', 'Áudio e Video', 'Bebê', 'Beleza eSaúde', 'Câmeras de Segurança', 'Chuveiros e Duchas Elétricas', 'Decoração e Organização', 'Eletrônicos', 'Eletroportáteis', 'Enceradeiras', 'Iluminação', 'Informática', 'Segurança', 'Suporte para TV/DVD', 'Tablet', 'Telefone', 'Umidificadores', 'Utensílios de Cozinha', 'Utilidades Domésticas', 'Ventilador']
        self.start_time = time.strftime("%b.%d-%X")
        self.end_time = None

    def timewarn(self):
        self.end_time = time.strftime("%b.%d-%X")
        print("Start : "+self.start_time + " End : "+self.end_time)

    def crawl(self):
        self.get_links()

    def crawl_to_file(self):
        self.crawl()

    def get_links(self):
        item_url_xpath = "//div[@class='nm-product-img-container']/a/@href"
        next_page_xpath = "//li[@class='neemu-pagination-next']/a/@href"
        r = requests.get(self.start_url)
        html = parser.fromstring(r.text)

        for cats in self.Cats:
            self.Clinks[cats] = self.start_url + cats
            print(self.start_url + cats)

        for cats in self.Cats:
            print(self.Clinks[cats])
            print("UAL")
            r = requests.get(self.Clinks[cats])
            html = parser.fromstring(r.text)
            self.parse_links(html, item_url_xpath)
            try:
                next_page = html.xpath(next_page_xpath)[0]
                next_page = "https:"+next_page
                print(next_page)

            except IndexError as e:
                next_page = None

            while next_page:
                r = requests.get(next_page)
                html = parser.fromstring(r.text)
                self.parse_links(html, item_url_xpath)
                try:
                    next_page = html.xpath(next_page_xpath)[0]
                    next_page = "https:"+next_page
                    print(next_page)

                except IndexError as e:
                    next_page = None

            cats = "Mecanico-"+cats+".csv"
            cats = cats.replace("/", " e ")
            self.get_items(cats)

    def get_items(self, catname):
        self.items = []
        self.key = []
        print(self.links)
        for link in self.links:
            r = requests.get(link)
            html = parser.fromstring(r.text)
            print(str(r) + " : "+link)
            self.items.append(self.extract_item(html, link))
        self.save_items(catname)
        self.links = set()

    def create_dict(self):
        for base in self.items:
            for check in base:
                if(check in self.key):
                    self.errors += 1
                else:
                    self.key.append(check)

    def extract_item(self, html, link):
        try:
            Nome = html.xpath("//h1[@class='product-name']")[0].text
        except IndexError as e:
            Nome = "Não Existe"

        try:
            CodRef = html.xpath(
                "//p[contains(text(),'Ref.:')]")[0].text.replace("Ref.: ", "")
        except IndexError as e:
            CodRef = "Não Existe"

        try:
            LMarca = html.xpath(
                "//div[@class='col-xs-12 col-sm-9 colzero']//strong//text()")
            IHA = len(LMarca) - 1
            Marca = LMarca[IHA].replace('\xa0', ' ')
        except IndexError as e:
            Marca = "Não Existe"

        try:
            De = html.xpath("//span[@class='preco-tabela']")[0].text
        except IndexError as e:
            De = "Not Found"

        try:
            Por = html.xpath("//span[@class='price']//text()")
        except:
            Por = "Não Existe"

        if(len(Por) > 3):
            fullPor = Por[0] + Por[1] + Por[2] + "," + Por[3]
        else:
            fullPor = "Nada"
        try:
            Desc = html.xpath(
                "//div[@class='col-xs-12 col-sm-9 colzero']//p[1]")[0].text
            if("• " in Desc or "- " in Desc):
                Desc = "Não Existe"
        except:
            Desc = "Não Existe"

        Prod_list = dict(CodRef=CodRef, Nome=Nome, Marca=Marca,
                         De=De, Por=fullPor, Descrição=Desc)

        Attr = html.xpath(
            "//div[@class='col-xs-12 col-sm-9 colzero']//p//text()")

        attrcont = 1
        CHEGA = 0
        conca = ""
        for check in Attr:
            if CHEGA < 1:
                check = check.strip("• ").strip("- ").strip(":: ").strip(" •")
                if len(check) > 1:
                    if "#" in check:
                        conca = formatar(check) + " , " + conca
                    elif 'Marca' in check:
                        CHEGA = 1
                    elif 'Técnicas' in check:
                        None
                    elif ':' in check:
                        ref, resp = check.split(':', 1)
                        Prod_list[formatar(ref)] = resp.replace(
                            '\xa0', ' ').strip(" ")
                    elif 'Tensão' in check and len(check) < 15:
                        Prod_list["Tensao"] = check.replace("Tensão ", "")
                    elif "Codigo" in check and len(check) < 20:
                        Prod_list["Codigo"] = check.replace(
                            "Codigo", "").replace("\xa0", "")
                    elif "Potência" in check and len(check) < 15:
                        Prod_list["Potencia"] = check.replace(
                            "Potência", "").strip(" ")
                    elif "Veja\n" in check or "*Imagens meramente ilustrativas" in check or "*Todas as informações divulgadas" in check:
                        None
                    else:
                        if(check == Prod_list["Descrição"]):
                            CHEGA = 0
                        else:
                            Prod_list["Atributo " +
                                      str(attrcont)] = check.replace('\xa0', ' ').strip(" ")
                            attrcont += 1

        if not conca == "":
            Prod_list["Atributo "+str(attrcont)] = conca

        IMGS = html.xpath("//ul[@class='img-produto-min']//img/@src")
        imgcont = 1
        for IMG in IMGS:
            Prod_list["Imagem " + str(imgcont)
                      ] = urlsplit(IMG)._replace(query="").geturl()
            imgcont += 1
        return Prod_list

    def parse_links(self, html, item_url_xpath):
        new_links = html.xpath(item_url_xpath)
        print(new_links)
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
        org = Organizer(self.key)
        fieldnames = org.Alinha()

        with open(filename, 'w') as f:
            dict_writer = csv.DictWriter(
                f, fieldnames=fieldnames, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(self.items)


print("TIME TO START")
spider = EcommerceSpider(
    "https://busca.lojadomecanico.com.br/busca?q=")
spider.crawl_to_file()

spider.timewarn()
