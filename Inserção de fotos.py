from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import time
import lxml.html as parser
import requests
import csv
import random
import ftplib
from urllib.parse import urlsplit, urljoin, urlparse


class Sql(object):
    def __init__(self):
        self.filename = "fotos.csv"
        self.resultado = "Inserts Leandrinho.csv"
        self.items = []

    def InsertCreator(self):
        with open(self.filename, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=";", skipinitialspace=True)
            for row in reader:
                row = list(row.items())
                sku = row[0][1]
                imgcont = 0
                for x in row:
                    if(x[0] == "SKU"):
                        None
                    elif(len(sku) > 0):
                        insert = ""
                        if(x[1] != ""):
                            insert = "INSERT INTO T_ImagensVtexTeste (NomeArquivo, UrlImagem, Numero) VALUES ('" + \
                                sku+"','"+x[1]+"',"+str(imgcont)+")"
                            if(imgcont == 0):
                                imgcont += 2
                            else:
                                imgcont += 1

                        if(insert != ""):
                            self.items.append(insert)
                            print(insert)

    def CreateCsv(self):
        with open(self.resultado, 'w') as f:
            dict_writer = csv.writer(f, delimiter=';')
            for x in self.items:
                dict_writer.writerow([x])


SQL = Sql()

SQL.InsertCreator()
SQL.CreateCsv()
print(SQL.items)
