import lxml.html as parser
import requests
import csv
import time
import re
from urllib.parse import urlsplit, urljoin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime


class Tarkett:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    def __init__(self):
        self.user = ''
        self.password = ''
        self.dataatual = str(datetime.today().strftime('%Y-%m-%d %H:%M'))

    def login(self):
        self.driver.implicitly_wait(5)
        try:
            poup_up = self.driver.find_element(By.CSS_SELECTOR,"body > div > div > a").click()
        except:
            print("Poup up nao localizado")
        
        try:
            usuario = self.driver.find_element(By.ID,"tbUsuario")
            usuario.send_keys('araguaina@hausz.com.br')
        except:
            print("Usuario nao encontrado")
        
        try:
            senha = self.driver.find_element(By.ID,"tbSenha")
            senha.send_keys('hausz')
        except:
            print("Senha nao encontrada")

        try:
            clica = self.driver.find_element(By.ID,"lkbEnviar").click()
        except:
            print("erro confirmar")


    def index(self):
        self.driver.implicitly_wait(5)
        self.driver.get('http://www.tarkettlink.com.br/')
        time.sleep(2)
        self.login()


    def seleciona_empresa(self):
        self.driver.implicitly_wait(15)

        try:
            selecione = self.driver.find_element(By.XPATH,"//li[@class='select2-results__option']")
            selecione.click()
        except:
            print("erro ao selecionar empresa")


    def seleciona_opcao_estoque(self):
        time.sleep(1)

        #Seleciona Tela estoque
        self.driver.get('http://www.tarkettlink.com.br/vendas/Estoque')
        
        try:
            box = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((
                By.CSS_SELECTOR, "#header > div.box1040 > div > div > div.box_01"))).click()
        except:
            print("erro ao selecionar box")

        self.driver.implicitly_wait(7)
        try:
            estoque = self.driver.find_element(By.CSS_SELECTOR,"#wrapper_header_header1_hyEstoque").click()
        except:
            estoque = self.find_element(
                By.XPATH,'/html/body/form[1]/div[3]/div[2]/div/div[1]/div/div/div[2]/div/div[2]/div[1]/ul[1]/li[3]/a')
            estoque.click()
            print("erro campo estoque")


    def extract_itens(self):
        lista_dicts = []
        self.driver.implicitly_wait(10)
        try:

            saldos = []
            saldostarkett = self.driver.find_elements(
                By.XPATH,'/html/body/form[1]/div[3]/div[3]/div/div/div/div[3]/div[2]/table/tbody/tr/td[3]')
            for sd in saldostarkett:

                valores = sd.text.strip()
                if valores !=None:
                    print(valores)

                    saldos.append(valores)
                    
        except:
            saldos.append('nao encontrado')

        try:
            nomes = []
            nomeprodutotarkett = self.driver.find_elements(
                By.XPATH,'/html/body/form[1]/div[3]/div[3]/div/div/div/div[3]/div[2]/table/tbody/tr/td[2]')

            for nomestarkett in nomeprodutotarkett:
                nomestarkett = nomestarkett.text.strip()
                if nomestarkett !=None:
                    print(nomestarkett)
                    nomes.append(nomestarkett)
                    
        except:
            nomes.append('nao encontrado')

        try:
            codigos = []
            referenciastarkett = self.driver.find_elements(
                By.XPATH,'/html/body/form[1]/div[3]/div[3]/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]')
            for refs in referenciastarkett:
                refs = refs.text.strip().split("(")[0].strip()
                print(refs)
                if refs !=None:
                    codigos.append(refs)

        except:
            codigos.append('nao encontrado')

        codigos_esp = [x for x in codigos if x !='' if x !='[]']
        nomesesp = [x for x in nomes if x !='' if x !='[]']
        refs_esp = [x for x in saldos if x !='' if x !='[]']

        for i in range(len(nomesesp)):
            desc = {}
            desc['Nomes'] = nomesesp[i]
            desc['Codigos'] = codigos_esp[i]
            desc['Saldos'] = refs_esp[i]
       
            lista_dicts.append(desc)
            print(desc)

        return lista_dicts

    def seleciona_categorias(self):
        
        self.driver.implicitly_wait(7)
        lista_categorias = ['Acessórios Metal','Acessórios Ps','Acessórios Pvc','Adesivo','Ambienta','Ambienta Click',
            'Artwall','Carpete','Decorflex','Essence','Essence Click','Ferramenta','Imagine','Injoy',
            'Mantas He','Mantas Ho','Omnisports','Paviflex Natural','Square','Tarkomassa','Toro Sc']

        for categorias in lista_categorias:
            time.sleep(3)
            try:
                select = self.driver.find_element(
                    By.XPATH,f"//select[@name='ctl00$wrapper_content$ddlCategorias']//option[@value='{categorias}']").click()
            except:
                print("erro ao selecionar categoria")

            time.sleep(2)

            lista = []
             #Mostra quantidade de sub categorias em cada linha
            try:
                quantidades = self.driver.find_elements(
                    By.XPATH,"//select[@id='wrapper_content_ddlLinhas']//option")
            except:
                print("erro quantidade")

            for quantidade in quantidades:
                lista.append(quantidade)

            valores = range(len(lista)+1)
            for valor in valores:
                time.sleep(3)

                try:
                    clicar = self.driver.find_element(
                        By.XPATH,f"//select[@id='wrapper_content_ddlLinhas']//option[{valor}]").click() # clica nas subcategorias
                except:
                    print("teste")

                time.sleep(3)
     
                try:
                    buscar = self.driver.find_element(By.CSS_SELECTOR,'#wrapper_content_lkbpesquisar').click()
                except:
                    print("erro busca")

                time.sleep(2)

                dicts = self.extract_itens()
                print(dicts)


tarkett = Tarkett()
tarkett.index()
tarkett.seleciona_empresa()
tarkett.seleciona_opcao_estoque()
tarkett.seleciona_categorias()