import lxml.html as parser
import requests
import csv
from urllib.parse import urlsplit, urljoin
import time
import json
import re
from collections import Counter
# Verificador anti-crawler baseado em regiao    : https://stackoverflow.com/questions/35252592/python-library-requests-open-the-wrong-page
# 403 FORBIDDEN                                 : https://stackoverflow.com/questions/38489386/python-requests-403-forbidden


class Product(object):
    def __init__(self):
        self.links = {}
        self.sku = []
        self.items = []
        self.start_url = "https://www.leroymerlin.com.br/"
        self.base_url = "https://www.leroymerlin.com.br/"

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

    def CSVREADER(self):
        with open("foto.csv", newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.sku.append(row["SKU"])
                self.links[row["SKU"]] = row["URL"]


def clear(texto):
    texto = texto.replace("\r", "").replace("\n", "").replace(
        "\t", "").replace("&nbsp;", "").replace("\xa0", "").strip(".").strip(" ")
    return texto


def blank(texto):
    teste = " ".join(texto.split())
    return teste


P = Product()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

session = requests.Session()
P.CSVREADER()
fieldnames = ["Sku", "Foto", "ERROR"]
cont = 1
try:
    for ID in P.sku:
        if cont == 1000:
            print("FOI 1000")
            cont = 1
        print(P.links[ID])
        r = session.get(
            P.links[ID], headers=headers)
        html = parser.fromstring(r.text)

        error = html.xpath("//div[@class='image404']")

        image = html.xpath("//meta[@property='og:image']/@content")
        check = 'https://lojasguapore.fbitsstatic.net/img/p/produto-nao-possui-foto-no-momento/sem-foto.jpg?w=420&h=420&v=no-change'
        if(len(error) == 1):
            bleh = dict(Sku=ID, ERROR=len(error))
        else:
            try:
                if image[0] == check:
                    bleh = dict(Sku=ID, Foto="SEMFOTO")
                else:
                    bleh = dict(Sku=ID, Foto=image[0])
            except IndexError as e:
                bleh = dict(Sku=ID, ERROR="INDEX ERROR")

        cont += 1
        P.items.append(bleh)

    with open("Sem-Foto.csv", 'w') as f:
        dict_writer = csv.DictWriter(
            f, fieldnames=fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(P.items)

except KeyboardInterrupt:
    with open("Sem-Foto.csv", 'w') as f:
        dict_writer = csv.DictWriter(
            f, fieldnames=fieldnames, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(P.items)
