from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from lxml import etree

class NuuvemScrapper():
    def __init__(self, driverName, data):
        self.driverName = driverName
        self.plataforma = data["P"]
        self.loja = data["L"]
        self.game_items_nuuvem = {}
        self.game_items_list_nuuvem = []
        self.total_paginas = 0
        self.page = 1

    def ReabrirDriver1(self, link, offset):
        try:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(link + str(offset))
            driver.maximize_window()
            html = driver.page_source
            web = BeautifulSoup(html, 'html.parser')
            driver.quit()
            return web
        except:
            pass

    def ReabrirDriver2(self, link):
        try:
            options = Options()
            options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.set_page_load_timeout(15)
            driver.get(link)
            driver.maximize_window()
            html = driver.page_source
            web = BeautifulSoup(html, 'html.parser')
            driver.quit()
            return web
        except TimeoutException:
            driver.quit()
            return None
        except:
            pass

    def converter_preco_para_float(self, preco):
        try:
            preco = preco.replace('R$', '')
            preco = preco.replace(',', '.')
            return float(preco)
        except:
            return None

    def manager(self):
        try:
            while True:
                if self.page == self.total_paginas or self.page == 50:
                    break
                else:
                    try:
                        site1 = self.ReabrirDriver1('https://www.nuuvem.com/br-pt/catalog/price/promo/sort/bestselling/sort-mode/desc/page/', self.page)
                        dom1 = etree.HTML(str(site1))
                        self.total_paginas = dom1.xpath("//a[contains(@class, 'pagination--item')]")[-1].text
                        games = dom1.xpath("//div[contains(@class, 'product-card--grid')]")
                    except:
                        break

                    for count, game in enumerate(games):
                        try:
                            link = game.xpath(".//a")[0].get('href')
                            site2 = self.ReabrirDriver2(link)
                            dom2 = etree.HTML(str(site2))
                        except:
                            break

                        if len(dom2.xpath("//span[contains(@class, 'integer')]")[0].text + dom2.xpath("//span[contains(@class, 'decimal')]")[0].text) < 1:
                            continue
                        self.game_items_nuuvem.update({'nome': dom2.xpath("//h1[contains(@class, 'product-title')]")[0].get('title')})
                        self.game_items_nuuvem.update({'precoDesconto': self.converter_preco_para_float(dom2.xpath("//span[contains(@class, 'integer')]")[0].text + dom2.xpath("//span[contains(@class, 'decimal')]")[0].text)})
                        if len(dom2.xpath("//span[contains(@class, 'product-price--old')]")[0].text) >= 1:
                            self.game_items_nuuvem.update({'precoTotal': self.converter_preco_para_float(dom2.xpath("//span[contains(@class, 'product-price--old')]")[0].text)})
                        else:
                            self.game_items_nuuvem.update({'precoTotal': self.converter_preco_para_float(dom2.xpath("//span[contains(@class, 'integer')]")[0].text + dom2.xpath("//span[contains(@class, 'decimal')]")[0].text)})
                        self.game_items_nuuvem.update({'plataforma': next(p["id"] for p in self.plataforma if p["nome"] == 'Computador')})
                        self.game_items_nuuvem.update({'midia': 0})
                        self.game_items_nuuvem.update({'link': link})
                        self.game_items_nuuvem.update({'loja': self.loja})
                        self.game_items_nuuvem.update({'linkImagem': game.xpath(".//img")[0].get('src')})
                        self.game_items_list_nuuvem.append(self.game_items_nuuvem.copy())

                    self.page += 1
        except:
            pass
        finally:
            return self.game_items_list_nuuvem
