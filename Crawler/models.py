from django.db import models

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pandas import DataFrame
from random import randint
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Busqueda(models.Model):
	id_busqueda = models.IntegerField() 
	texto = models.CharField(max_length = 100)
	fecha = models.DateField(auto_now=True)
	n_paginas = models.IntegerField()
	sitios = models.CharField(max_length=30)

class Link(models.Model):
	id_busqueda = models.IntegerField()
	id_link = models.IntegerField()
	url= models.CharField(max_length = 200)
	buscador=models.CharField(max_length = 50)

class CrawlerWeb():
    elem = None
    #driver = webdriver.Chrome()

    def newDriver(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
    def setElement(self, by='q', findby=0):

        if(findby==0):
            self.elem = self.driver.find_element_by_name(by)
        elif findby==1:
            self.elem=self.driver.find_element_by_xpath(by)


        self.elem.clear()
    def searchByCSS(self ,keys=[], elementsPath='', urlPath='', namePath='', next_element='',n_result=10):
        df = DataFrame(columns=['titulo','url'])
        next = None
        for key in keys:
            self.elem.send_keys(key)
            self.elem.send_keys(Keys.RETURN)
            while (len(df)<n_result):
                lista = self.driver.find_elements_by_css_selector(elementsPath)
                for elem in lista:
                    title = elem.find_element_by_css_selector(namePath)
                    url = elem.find_element_by_css_selector(urlPath).get_attribute("href")

                    df = df.append({'titulo':title.text, 'url':url},ignore_index=True)
                sleep(randint(5,8))
                try:
                    next=self.driver.find_element_by_xpath(next_element)
                    next.click()
                except NoSuchElementException:
                    break
        self.driver.close()
        return df
    def searchByXPATH(self ,keys=[], elementsPath='', urlPath='', namePath='', next_element='',n_result=10):
        #self.driver = webdriver.Chrome()
        df = DataFrame(columns=['titulo','url'])
        next = None
        for key in keys:
            self.elem.send_keys(key)
            self.elem.send_keys(Keys.RETURN)
            while (len(df)<n_result):
                lista = self.driver.find_elements_by_xpath(elementsPath)
                for elem in lista:
                    title = elem.find_element_by_xpath(namePath)
                    url = elem.find_element_by_xpath(urlPath).get_attribute("href")

                    df = df.append({'titulo':title.text, 'url':url},ignore_index=True)
                sleep(randint(5,8))
                try:
                    next=self.driver.find_element_by_xpath(next_element)
                    next.click()
                except NoSuchElementException:
                    break
        self.driver.close()
        return df

    def setUrl(self,url):
        self.driver.get(url)
    def e_commerceML(self ,keys=[], elementsPath='li.ui-search-layout__item', urlPath='a.ui-search-item__group__element.ui-search-link', namePath='h2.ui-search-item__title', next_element='//a[@title="Siguiente"',n_result=10):
        return self.searchByCSS(keys, elementsPath, urlPath, namePath, next_element,n_result)
    def e_commerceOLX(self, key='', elementsPath='//li[@data-aut-id="itemBox"]', buttonPath='//button[@data-aut-id="btnLoadMore"]', titlePath='.//span[@data-aut-id="itemTitle"]', urlPath='.//a', n_result=1):
        #self.driver = webdriver.Chrome()
        df = DataFrame(columns=['titulo','url'])
        self.driver.get('https://www.olx.com.ec/items/q-'+key)
        for i in range(n_result):
            try:
                #//button[@data-aut-id="btnLoadMore"]
                boton = self.driver.find_element_by_xpath(buttonPath)
                boton.click()
                sleep(randint(5, 6))
                boton = self.driver.find_element_by_xpath(buttonPath)
            except:
                break

        lista = self.driver.find_elements_by_xpath(elementsPath)
        print(len(lista))
        for elem in lista:
            # Por cada anuncio hallo el preico

            try:
                title = elem.find_element_by_xpath(titlePath).text
                url= elem.find_element_by_xpath(urlPath).get_attribute("href")
                df = df.append({'titulo':title, 'url':url},ignore_index=True)
            except StaleElementReferenceException:
                print('error')
        self.driver.close()
        return df
    def e_commerceAmz(self ,keys=[], elementsPath='//div[@data-component-type="s-search-result"]', urlPath='.//a[@class="a-link-normal a-text-normal"]', namePath='.//span[@class="a-size-base-plus a-color-base a-text-normal"]', next_element='//li[@class="a-last"]',n_result=10):
        return self.searchByXPATH(keys, elementsPath, urlPath, namePath, next_element,n_result)

