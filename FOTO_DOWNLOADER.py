import lxml.html as parser
import requests
import csv
from urllib.parse import urlsplit, urljoin
import ftplib
import json
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
# Método simples de limpeza de url


def clean_url(url):
    return urlsplit(urljoin(base_url, url))._replace(query="").geturl()


def percentage(percent, whole):
    return (percent * whole) / 100.0


def sugerido(preco):
    preco = preco.replace("RS ")
    sugerido = percentage(1, preco)
    total = preco - sugerido
    print(total)


def ftp_send(filename, directory):
    session = ftplib.FTP('server.lojasguapore.com.br',
                         'Ricardo', 'r!c4rdã0_2018_v1d4L0ka')
    session.cwd("/"+directory)
    file = open(filename, 'rb')                  # file to send
    session.storbinary('STOR '+filename, file)     # send the file
    file.close()                                    # close file and FTP
    session.quit()


def prepare_url(base, url):
    url = urljoin(base, url)
    return urlsplit(url)._replace(query="").geturl()


def CSVLINKS(lista):
    with open("Lista.csv", 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for x in lista:
            writer.writerow([x])


class Produto(object):
    def __init__(self):
        self.links = {}
        self.new = []
        self.SKU = []
        self.file = "LC.csv"

    def CSVREADER(self):
        with open(self.file, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                self.SKU.append(row["SKU"])
                self.links[row["SKU"]] = row["URL"]


P = Produto()

P.CSVREADER()


pasta = "Tramontina"

for SKU in P.SKU:
    foto = SKU+'.jpg'
    path = "C:\\Temp\\Projetos\\Python\\"+pasta+"\\"+foto

    f = open(path, 'wb')
    f.write(requests.get(P.links[SKU]).content)
    f.close()
