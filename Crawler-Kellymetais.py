import lxml.html as parser
import requests
import csv
import time
import re
import unidecode
import json
from urllib.parse import urlsplit, urljoin
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import ftplib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

driver = webdriver.Chrome()
driver.get

lista = ['http://www.kellymetais.com.br/produtos/banheiro/misturadores ', 'http://www.kellymetais.com.br/produtos/banheiro ', 'http://www.kellymetais.com.br/produtos/banheiro/duchas ', 'http://www.kellymetais.com.br/produtos/banheiro/torneiras ', 'http://www.kellymetais.com.br/produtos/banheiro/acessorios-banheiro ', 'http://www.kellymetais.com.br/produtos/banheiro/kit ', 'http://www.kellymetais.com.br/produtos/acessibilidade ', 'http://www.kellymetais.com.br/produtos/acessibilidade/barras-de-apoio ', 'http://www.kellymetais.com.br/produtos/economizadores ', 'http://www.kellymetais.com.br/produtos/economizadores/economizadores ', 'http://www.kellymetais.com.br/produtos/economizadores/torneiras-automaticas ', 'http://www.kellymetais.com.br/produtos/economizadores/torneiras-eletronicas- ', 'http://www.kellymetais.com.br/produtos/uso-geral ', 'http://www.kellymetais.com.br/produtos/uso-geral/uso-geral- ', 'http://www.kellymetais.com.br/produtos/cozinha ', 'http://www.kellymetais.com.br/produtos/cozinha/cozinha ',
         'http://www.kellymetais.com.br/produtos/cozinha/monocomando ', 'http://www.kellymetais.com.br/produtos/complementos-gerais ', 'http://www.kellymetais.com.br/produtos/complementos-gerais/complementos-gerais ', 'http://www.kellymetais.com.br/produtos/complementos-gerais/registros- ', 'http://www.kellymetais.com.br/produtos/complementos-gerais/boias ', 'http://www.kellymetais.com.br/produtos/complementos-gerais/vedacao ', 'http://www.kellymetais.com.br/produtos/complementos-gerais/tubos-de-ligacao ', 'http://www.kellymetais.com.br/produtos/complementos-gerais/acabamentos ', 'http://www.kellymetais.com.br/produtos/complementos-gerais/sifao ', 'http://www.kellymetais.com.br/produtos/complementos-gerais/valvula ', 'http://www.kellymetais.com.br/produtos/complementos-gerais/reparos ', 'http://www.kellymetais.com.br/produtos/chuveiros ', 'http://www.kellymetais.com.br/produtos/chuveiros/duchas ', 'http://www.kellymetais.com.br/lojas ', 'http://www.kellymetais.com.br/contato']

lista2 = []

next_page = ""

for x in lista:
    driver.get(x)
    produto = driver.find_elements_by_xpath("//div[@class='flex-list']//a")
    for prod in produto:
        lista2.append(prod.get_attribute("href"))

    check = len(driver.find_elements_by_class_name("pagination"))

    if(check > 0):

        while(next_page != None):
            driver.execute_script(
                "document.querySelector('ul.pagination.m0 li:nth-last-child(1) a').click();")

            produto = driver.find_elements_by_xpath(
                "//div[@class='flex-list']//a")

            for prod in produto:
                lista2.append(prod.get_attribute("href"))

            check = driver.find_elements_by_css_selector(
                "ul.pagination.m0 li:nth-last-child(1)")[0].get_attribute("class")

            if("disabled" in check):
                next_page = None
                print(next_page)


print(lista2)
